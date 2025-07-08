"""
MkDocs Confluence Publisher Plugin

A robust MkDocs plugin that publishes documentation to Confluence while maintaining
proper structure and formatting. Based on the mkdocs-confluence-publisher approach
but with SSL handling and Bearer token support for corporate environments.
"""

import logging
import os
import re
import urllib3
from typing import Dict, List, Tuple, Optional
from dotenv import load_dotenv

import markdown
import requests
from requests.auth import HTTPBasicAuth

from mkdocs.config import config_options
from mkdocs.plugins import BasePlugin
from mkdocs.structure.nav import Page, Section


# Suppress SSL warnings for corporate environments
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Setup logging
logger = logging.getLogger('mkdocs.plugins.confluence_publisher')


class ConfluencePage:
    """Represents a Confluence page with ID and title."""
    
    def __init__(self, id: int, title: str):
        self.id: int = id
        self.title: str = title

    def __repr__(self) -> str:
        return f"ConfluencePage(id={self.id}, title='{self.title}')"


class ConfluenceClient:
    """Custom Confluence client with SSL bypass and Bearer/Basic auth support."""
    
    def __init__(self, base_url: str, username: str, token: str, verify_ssl: bool = False):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.session.verify = verify_ssl
        
        # Prioritize Bearer token authentication (works in corporate environments)
        if token:
            self.session.headers.update({'Authorization': f'Bearer {token}'})
            logger.debug("Using Bearer token authentication")
        elif username and token:
            self.session.auth = HTTPBasicAuth(username, token)
            logger.debug("Using Basic authentication")
        else:
            raise ValueError("Token must be provided for authentication")
    
    def _make_request(self, method: str, endpoint: str, **kwargs) -> requests.Response:
        """Make an authenticated request to Confluence API."""
        url = f"{self.base_url}/rest/api{endpoint}"
        response = self.session.request(method, url, **kwargs)
        response.raise_for_status()
        return response
    
    def get_page_by_title(self, space_key: str, title: str) -> Optional[dict]:
        """Get a page by title in a space."""
        try:
            response = self._make_request(
                'GET', 
                '/content',
                params={
                    'spaceKey': space_key,
                    'title': title,
                    'expand': 'version'
                }
            )
            results = response.json().get('results', [])
            return results[0] if results else None
        except requests.exceptions.RequestException:
            return None
    
    def create_page(self, space_key: str, title: str, body: str, parent_id: Optional[int] = None) -> dict:
        """Create a new page in Confluence."""
        data = {
            'type': 'page',
            'title': title,
            'space': {'key': space_key},
            'body': {
                'storage': {
                    'value': body,
                    'representation': 'storage'
                }
            }
        }
        
        if parent_id:
            data['ancestors'] = [{'id': str(parent_id)}]
        
        response = self._make_request('POST', '/content', json=data)
        return response.json()
    
    def update_page(self, page_id: int, title: str, body: str, version: int) -> dict:
        """Update an existing page in Confluence."""
        data = {
            'version': {'number': version + 1},
            'title': title,
            'type': 'page',
            'body': {
                'storage': {
                    'value': body,
                    'representation': 'storage'
                }
            }
        }
        
        response = self._make_request('PUT', f'/content/{page_id}', json=data)
        return response.json()
    
    def get_attachments(self, page_id: int) -> List[dict]:
        """Get attachments for a page."""
        response = self._make_request('GET', f'/content/{page_id}/child/attachment')
        return response.json().get('results', [])
    
    def upload_attachment(self, page_id: int, file_path: str, comment: str = '') -> dict:
        """Upload an attachment to a page."""
        filename = os.path.basename(file_path)
        
        with open(file_path, 'rb') as f:
            files = {'file': (filename, f, 'application/octet-stream')}
            data = {'comment': comment}
            
            response = self._make_request(
                'POST', 
                f'/content/{page_id}/child/attachment',
                files=files,
                data=data
            )
        
        return response.json()


class ConfluencePublisherPlugin(BasePlugin):
    """MkDocs plugin for publishing to Confluence."""
    
    config_scheme = (
        ('confluence_prefix', config_options.Type(str, default='')),
        ('space_key', config_options.Type(str, required=True)),
        ('parent_page_id', config_options.Type(int, required=True)),
        ('dry_run', config_options.Type(bool, default=False)),
        ('verify_ssl', config_options.Type(bool, default=False)),
        ('upload_attachments', config_options.Type(bool, default=True)),
    )

    def __init__(self):
        load_dotenv()
        self.confluence: Optional[ConfluenceClient] = None
        self.md_to_page: Dict[str, ConfluencePage] = {}
        self.page_attachments: Dict[str, List[str]] = {}
        
        # Setup Markdown processor with useful extensions
        self.markdown_processor = markdown.Markdown(extensions=[
            'markdown.extensions.tables',
            'markdown.extensions.fenced_code',
            'markdown.extensions.codehilite',
            'markdown.extensions.toc',
            'markdown.extensions.admonition',
            'markdown.extensions.attr_list',
            'markdown.extensions.def_list'
        ])

    def on_config(self, config):
        """Initialize Confluence connection on config load."""
        logger.info("Initializing Confluence Publisher Plugin")
        
        # Get configuration from environment
        confluence_url = os.getenv('CONFLUENCE_URL')
        confluence_username = os.getenv('CONFLUENCE_USERNAME')
        confluence_token = os.getenv('CONFLUENCE_API_TOKEN')
        
        if not confluence_url:
            logger.error("CONFLUENCE_URL environment variable not set")
            return config
        
        if not confluence_token:
            logger.error("CONFLUENCE_API_TOKEN environment variable not set")
            return config
        
        try:
            self.confluence = ConfluenceClient(
                base_url=confluence_url,
                username=confluence_username,
                token=confluence_token,
                verify_ssl=self.config['verify_ssl']
            )
            logger.info("Confluence connection initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Confluence connection: {e}")
        
        return config

    def on_nav(self, nav, config, files):
        """Create page structure in Confluence based on navigation."""
        if not self.confluence or self.config['dry_run']:
            return nav
        
        prefix = self.config['confluence_prefix']
        space_key = self.config['space_key']
        parent_page_id = self.config['parent_page_id']
        
        logger.info(f"Creating page structure in Confluence space '{space_key}' with prefix '{prefix}'")
        
        try:
            self.md_to_page = self._create_pages(
                nav.items, prefix, space_key, parent_page_id
            )
            logger.info(f"Created {len(self.md_to_page)} page mappings")
        except Exception as e:
            logger.error(f"Failed to create page structure: {e}")
        
        return nav

    def on_page_markdown(self, markdown: str, page: Page, config, files):
        """Process page markdown and update Confluence content."""
        if not self.confluence or self.config['dry_run']:
            return markdown
        
        logger.debug(f"Processing page: {page.file.src_path}")
        
        try:
            attachments = self._update_page_content(markdown, page)
            self.page_attachments[page.file.src_path] = attachments
            logger.debug(f"Updated page content, found {len(attachments)} attachments")
        except Exception as e:
            logger.error(f"Failed to update page content for {page.file.src_path}: {e}")
        
        return markdown

    def on_post_page(self, output: str, page: Page, config):
        """Upload attachments after page processing."""
        if not self.confluence or self.config['dry_run']:
            return output
        
        # Check if attachment upload is enabled
        if not self.config['upload_attachments']:
            return output
        
        confluence_page = self.md_to_page.get(page.file.src_path)
        attachments = self.page_attachments.get(page.file.src_path, [])
        
        if confluence_page and attachments:
            logger.debug(f"Uploading {len(attachments)} attachments for page: {confluence_page.title}")
            try:
                self._upload_attachments(confluence_page.id, attachments)
            except Exception as e:
                logger.error(f"Failed to upload attachments for {page.file.src_path}: {e}")
        
        return output

    def on_post_build(self, config):
        """Log completion of publishing process."""
        if self.config['dry_run']:
            logger.info("Dry run completed - no changes made to Confluence")
        else:
            logger.info("Successfully published documentation to Confluence")

    def _create_pages(self, items, prefix: str, space_key: str, parent_id: int) -> Dict[str, ConfluencePage]:
        """Recursively create pages in Confluence based on navigation structure."""
        md_to_page = {}
        
        for item in items:
            page_title = f"{prefix}{item.title}"
            logger.debug(f"Processing item: {page_title}")
            
            # Check if page already exists
            existing_page = self.confluence.get_page_by_title(space_key, page_title)
            
            if existing_page:
                page_id = int(existing_page['id'])
                logger.debug(f"Page already exists: {page_title} (ID: {page_id})")
            else:
                # Create new page
                if isinstance(item, Section):
                    # Section page with children macro
                    body = '<ac:structured-macro ac:name="children" />'
                    logger.info(f"Creating section page: {page_title}")
                else:
                    # Regular page
                    body = '<p>This page will be updated with content from MkDocs.</p>'
                    logger.info(f"Creating page: {page_title}")
                
                try:
                    new_page = self.confluence.create_page(
                        space_key=space_key,
                        title=page_title,
                        body=body,
                        parent_id=parent_id
                    )
                    page_id = int(new_page['id'])
                    logger.info(f"Created page: {page_title} (ID: {page_id})")
                except Exception as e:
                    logger.error(f"Failed to create page {page_title}: {e}")
                    continue
            
            # Map Page objects to Confluence pages
            if isinstance(item, Page):
                md_to_page[item.file.src_path] = ConfluencePage(id=page_id, title=page_title)
                logger.debug(f"Mapped {item.file.src_path} to page ID {page_id}")
            
            # Recursively process children for sections
            if isinstance(item, Section) and item.children:
                child_mappings = self._create_pages(
                    item.children, prefix, space_key, page_id
                )
                md_to_page.update(child_mappings)
        
        return md_to_page

    def _update_page_content(self, markdown: str, page: Page) -> List[str]:
        """Convert markdown to Confluence format and update page."""
        confluence_page = self.md_to_page.get(page.file.src_path)
        if not confluence_page:
            logger.warning(f"No Confluence page mapping found for {page.file.src_path}")
            return []
        
        try:
            # Convert markdown to Confluence storage format
            confluence_content, attachments = self._convert_markdown_to_confluence(markdown, page)
            
            # Validate content before sending
            if not confluence_content or confluence_content.strip() == '':
                logger.warning(f"Empty content generated for {page.file.src_path}, skipping update")
                return attachments
            
            # Get current page info for version
            current_page = self.confluence.get_page_by_title(
                self.config['space_key'], 
                confluence_page.title
            )
            
            if current_page:
                current_version = current_page['version']['number']
                
                # Update page content
                self.confluence.update_page(
                    page_id=confluence_page.id,
                    title=confluence_page.title,
                    body=confluence_content,
                    version=current_version
                )
                logger.info(f"Updated Confluence page: {confluence_page.title}")
            else:
                logger.error(f"Could not find current page info for {confluence_page.title}")
            
            return attachments
            
        except Exception as e:
            logger.error(f"Failed to update page content for {confluence_page.title}: {e}")
            # Log the content that caused the error for debugging
            logger.debug(f"Problematic content length: {len(markdown)} characters")
            return []

    def _sanitize_content(self, content: str) -> str:
        """Sanitize content to prevent API errors."""
        # Remove or replace potentially problematic characters/tags
        
        # Remove malformed HTML comments
        content = re.sub(r'<!--.*?-->', '', content, flags=re.DOTALL)
        
        # Clean up malformed or nested image tags that might be generated by drawio-exporter
        content = re.sub(r'<img[^>]*src=""[^>]*>', '', content)  # Remove empty src images
        content = re.sub(r'<img[^>]*>\s*</img>', '', content)    # Remove self-closed image tags
        
        # Remove any draw.io specific elements that might cause issues
        content = re.sub(r'<mxfile.*?</mxfile>', '', content, flags=re.DOTALL)
        
        # Clean up multiple consecutive newlines
        content = re.sub(r'\n\s*\n\s*\n+', '\n\n', content)
        
        # Ensure content is not empty
        if not content.strip():
            content = '<p>Content could not be processed.</p>'
        
        return content

    def _convert_markdown_to_confluence(self, markdown_content: str, page: Page) -> Tuple[str, List[str]]:
        """Convert markdown to Confluence storage format and extract attachments."""
        # Find image attachments
        attachments = []
        image_pattern = r'!\[.*?\]\((.*?)\)'
        
        for match in re.finditer(image_pattern, markdown_content):
            image_path = match.group(1)
            if not image_path.startswith('http'):
                # Convert relative path to absolute
                full_path = os.path.join(os.path.dirname(page.file.abs_src_path), image_path)
                full_path = os.path.normpath(full_path)
                if os.path.exists(full_path):
                    attachments.append(full_path)
                else:
                    logger.warning(f"Referenced image not found: {full_path}")
        
        # Convert markdown to HTML
        html = markdown.markdown(
            markdown_content,
            extensions=['codehilite', 'tables', 'toc', 'admonition']
        )
        
        # Sanitize content before converting to Confluence format
        html = self._sanitize_content(html)
        
        # Convert to Confluence format
        confluence_content = self._convert_html_to_confluence(html)
        
        return confluence_content, attachments

    def _convert_html_to_confluence(self, html: str) -> str:
        """Convert HTML to Confluence storage format."""
        
        # Convert code blocks with codehilite class (from fenced_code extension)
        def clean_code_content(content):
            # Strip all HTML tags to get plain text
            content = re.sub(r'<[^>]+>', '', content)
            # Decode HTML entities
            content = content.replace('&quot;', '"').replace('&lt;', '<').replace('&gt;', '>').replace('&amp;', '&')
            return content.strip()
        
        # Handle codehilite code blocks (with language detection)
        def replace_codehilite_with_lang(match):
            language = match.group(1)
            code_content = clean_code_content(match.group(2))
            return f'<ac:structured-macro ac:name="code"><ac:parameter ac:name="language">{language}</ac:parameter><ac:plain-text-body><![CDATA[{code_content}]]></ac:plain-text-body></ac:structured-macro>'
        
        def replace_codehilite_no_lang(match):
            code_content = clean_code_content(match.group(1))
            return f'<ac:structured-macro ac:name="code"><ac:plain-text-body><![CDATA[{code_content}]]></ac:plain-text-body></ac:structured-macro>'
        
        # Replace codehilite blocks with language
        html = re.sub(
            r'<div class="codehilite"><pre><span></span><code class="language-(\w+)">(.*?)</code></pre></div>',
            replace_codehilite_with_lang,
            html,
            flags=re.DOTALL
        )
        
        # Replace codehilite blocks without language
        html = re.sub(
            r'<div class="codehilite"><pre><span></span><code>(.*?)</code></pre></div>',
            replace_codehilite_no_lang,
            html,
            flags=re.DOTALL
        )
        
        # Convert simple code blocks with language
        html = re.sub(
            r'<pre><code class="language-(\w+)">(.*?)</code></pre>',
            replace_codehilite_with_lang,
            html,
            flags=re.DOTALL
        )
        
        # Convert generic code blocks
        html = re.sub(
            r'<pre><code>(.*?)</code></pre>',
            replace_codehilite_no_lang,
            html,
            flags=re.DOTALL
        )
        
        # Convert inline code
        html = re.sub(r'<code>(.*?)</code>', r'<code>\1</code>', html)
        
        # Convert tables to Confluence format
        html = re.sub(r'<table>', '<table class="wrapped">', html)
        
        # Convert admonitions to info/warning macros
        html = re.sub(
            r'<div class="admonition note">\s*<p class="admonition-title">Note</p>\s*<p>(.*?)</p>\s*</div>',
            r'<ac:structured-macro ac:name="info"><ac:rich-text-body>\1</ac:rich-text-body></ac:structured-macro>',
            html,
            flags=re.DOTALL
        )
        
        html = re.sub(
            r'<div class="admonition warning">\s*<p class="admonition-title">Warning</p>\s*<p>(.*?)</p>\s*</div>',
            r'<ac:structured-macro ac:name="warning"><ac:rich-text-body>\1</ac:rich-text-body></ac:structured-macro>',
            html,
            flags=re.DOTALL
        )
        
        # Handle images - convert to Confluence attachment format
        html = re.sub(
            r'<img src="([^"]+)" alt="([^"]*)"',
            r'<ac:image><ri:attachment ri:filename="\1" /></ac:image>',
            html
        )
        
        # Replace incompatible code language macros
        html = self._fix_code_macros(html)
        
        return html

    def _fix_internal_links(self, content: str) -> str:
        """Fix internal markdown links to point to Confluence pages."""
        def replace_link(match):
            href = match.group(2)
            if href.endswith('.md') and href in self.md_to_page:
                confluence_page = self.md_to_page[href]
                logger.debug(f"Fixed link to {href} -> {confluence_page.title}")
                return f'<ac:link><ri:page ri:content-title="{confluence_page.title}" /></ac:link>'
            return match.group(0)
        
        return re.sub(r'<a (.*?)href="(.*?)"(.*?)>(.*?)</a>', replace_link, content)

    def _fix_code_macros(self, content: str) -> str:
        """Replace incompatible code language macros."""
        # Map of incompatible languages to compatible ones
        replacements = {
            'json': 'yaml',
            'dockerfile': 'bash',
            'powershell': 'bash',
        }
        
        for incompatible, compatible in replacements.items():
            pattern = f'<ac:parameter ac:name="language">{incompatible}</ac:parameter>'
            replacement = f'<ac:parameter ac:name="language">{compatible}</ac:parameter>'
            content = content.replace(pattern, replacement)
        
        return content

    def _upload_attachments(self, page_id: int, attachments: List[str]):
        """Upload attachments to a Confluence page."""
        if not attachments:
            return
        
        try:
            # Get existing attachments
            existing_attachments = self.confluence.get_attachments(page_id)
            existing_names = {att['title'] for att in existing_attachments}
        except Exception as e:
            logger.warning(f"Could not retrieve existing attachments: {e}")
            existing_names = set()
        
        for attachment_path in attachments:
            filename = os.path.basename(attachment_path)
            
            if filename in existing_names:
                logger.debug(f"Attachment already exists, skipping: {filename}")
                continue
            
            # Check if file exists before trying to upload
            if not os.path.exists(attachment_path):
                logger.warning(f"Attachment file not found: {attachment_path}")
                continue
            
            try:
                self.confluence.upload_attachment(
                    page_id=page_id,
                    file_path=attachment_path,
                    comment='Uploaded by MkDocs Confluence Publisher'
                )
                logger.info(f"Uploaded attachment: {filename}")
            except Exception as e:
                # Log warning instead of error to not fail the entire build
                logger.warning(f"Could not upload attachment {filename}: {e}")
                logger.warning("This may be due to insufficient permissions or file size limits")
