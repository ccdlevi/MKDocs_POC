# Publishing to Confluence

This document explains how to publish your MkDocs documentation to Confluence using our custom REST API publisher. The project includes a robust Python script that handles authentication, content conversion, and publishing via the Confluence REST API.

## Current Status

**✅ MkDocs Build**: Fully functional  
**✅ Documentation Development**: Ready for use  
**✅ Confluence Publishing**: Custom REST API publisher available

## Quick Start

### 1. Configure Environment Variables

The `.env` file in your project root contains your Confluence configuration:

```env
# Confluence instance URL
CONFLUENCE_URL=https://your-instance.atlassian.net

# Space key where content should be published
CONFLUENCE_SPACE_KEY=DOCS

# Parent page ID under which content will be published
CONFLUENCE_PARENT_PAGE_ID=123456

# Confluence username (email address)
CONFLUENCE_USERNAME=your.email@example.com

# Confluence API token (never use your actual password)
CONFLUENCE_API_TOKEN=your_api_token_here

# Optional: Delete pages in Confluence that don't exist in docs
# CONFLUENCE_DELETE_MISSING=true

# Optional: Add labels to published pages
# CONFLUENCE_LABELS=documentation,mkdocs

# Optional: Specify a custom title prefix
# CONFLUENCE_TITLE_PREFIX=[DOCS] 
```

### 2. Test Your Connection

Before publishing, test your Confluence connection:

```bash
python test_confluence.py
```

This will verify your credentials and configuration.

### 3. Publish Your Documentation

#### Quick Publish (Build + Publish)
```bash
python publish.py --build --publish
```

#### Step-by-Step Publishing
```bash
# Build the site first
python -m mkdocs build

# Publish to Confluence
python publish.py --publish
```

#### Dry Run (Preview Changes)
```bash
python publish.py --dry-run
```

## Publishing Options

### Available Commands

| Command | Description |
|---------|-------------|
| `--publish` | Publish the built site to Confluence |
| `--dry-run` | Show what would be published without actually doing it |
| `--clean` | Remove orphaned pages from Confluence |
| `--build` | Build the MkDocs site before publishing |
| `--site-dir DIR` | Specify the site directory (default: site) |

### Examples

```bash
# Dry run to see what will be published
python publish.py --dry-run

# Build and publish in one command
python publish.py --build --publish

# Publish with custom site directory
python publish.py --publish --site-dir custom_site

# Clean up orphaned pages
python publish.py --clean
```

## Content Conversion Features

### Supported Elements

The custom publisher converts MkDocs/Material content to Confluence format:

| Element | MkDocs/HTML | Confluence |
|---------|-------------|------------|
| Headers | `<h1>` - `<h6>` | Native headers |
| Code blocks | Syntax highlighted | Confluence code macro |
| Admonitions | Material admonitions | Info/Warning/Error macros |
| Tables | HTML tables | Confluence tables |
| Links | Markdown/HTML links | Confluence links |
| Images | HTML images | Confluence attachments |
| Mermaid diagrams | Interactive diagrams | Code blocks (for reference) |

### Content Processing

The publisher automatically:
- Extracts main content from HTML pages
- Removes navigation, headers, and footers
- Converts Material Design components
- Handles special characters and encoding
- Preserves document structure

## Configuration Reference

### Environment Variables

| Variable | Required | Description | Example |
|----------|----------|-------------|---------|
| `CONFLUENCE_URL` | ✅ | Confluence instance URL | `https://company.atlassian.net` |
| `CONFLUENCE_SPACE_KEY` | ✅ | Target space key | `DOCS` |
| `CONFLUENCE_PARENT_PAGE_ID` | ⚠️ | Parent page for organization | `123456` |
| `CONFLUENCE_USERNAME` | ✅ | Your Confluence username | `user@company.com` |
| `CONFLUENCE_API_TOKEN` | ✅ | API token (not password) | `abc123...` |
| `CONFLUENCE_DELETE_MISSING` | ❌ | Clean up orphaned pages | `true` |
| `CONFLUENCE_LABELS` | ❌ | Comma-separated labels | `docs,mkdocs` |
| `CONFLUENCE_TITLE_PREFIX` | ❌ | Prefix for page titles | `[DOCS] ` |

### VS Code Tasks

The project includes pre-configured VS Code tasks:

- **Serve MkDocs Site**: Start development server
- **Build MkDocs Site**: Build the documentation
- **Publish to Confluence**: Run the publisher script

Access these via `Ctrl+Shift+P` → "Tasks: Run Task"
## Finding Your Confluence Page ID

To find the ID of a Confluence page to use as the parent page:

1. Navigate to the page in Confluence
2. Look at the URL, which should contain something like: `pageId=123456`
3. The number after `pageId=` is your page ID
4. Alternatively, view the page source and search for `content-id`

## Troubleshooting

### Connection Issues

**Problem**: Cannot connect to Confluence
```bash
❌ HTTP 401: Unauthorized
```

**Solutions**:
1. Verify your API token is correct and active
2. Check that your username is your email address
3. Ensure you have access to the specified space
4. Test connection: `python test_confluence.py`

**Problem**: SSL Certificate errors
```bash
❌ SSL: CERTIFICATE_VERIFY_FAILED
```

**Solutions**:
- The publisher handles corporate SSL certificates automatically
- If issues persist, check your corporate proxy settings
- Contact your IT department about certificate requirements

### Publishing Issues

**Problem**: Pages not appearing in Confluence
```bash
❌ Failed to create page: Page Title
```

**Solutions**:
1. Check the console output for specific errors
2. Verify you have write permissions in the space
3. Ensure the parent page ID exists and is accessible
4. Try publishing a single page first with `--dry-run`

**Problem**: Content formatting issues

**Solutions**:
1. Check that complex Markdown renders correctly in MkDocs first
2. Material Design components may not translate perfectly
3. Use simpler formatting for better Confluence compatibility
4. Test with basic content first

### Performance Issues

**Problem**: Publishing is slow

**Solutions**:
1. Use `--dry-run` to test without actual publishing
2. Consider publishing smaller sections at a time
3. Clean up orphaned pages periodically with `--clean`

## Best Practices

### Content Organization
1. **Use Clear Titles**: Confluence uses page titles for navigation
2. **Organize Hierarchically**: Use the parent page ID for proper structure
3. **Keep it Simple**: Complex formatting may not translate well
4. **Test Regularly**: Use dry runs to verify content before publishing

### Workflow Recommendations
1. **Development**: Write and test in MkDocs first
2. **Staging**: Use `--dry-run` to preview changes
3. **Production**: Publish incrementally
4. **Maintenance**: Clean orphaned pages regularly

### Security
1. **Never commit API tokens** to version control
2. **Use .env files** for sensitive configuration
3. **Rotate tokens regularly** per company policy
4. **Limit permissions** to only necessary spaces

## Advanced Usage

### Custom Content Processing

To modify how content is converted, edit the `html_to_confluence_storage()` method in `publish.py`:

```python
def html_to_confluence_storage(self, html_content: str) -> str:
    # Add your custom conversion logic here
    content = html_content
    # ... existing conversions ...
    return content
```

### Batch Operations

```bash
# Process multiple builds
for site in site1 site2 site3; do
    python publish.py --site-dir "$site" --publish
done

# Clean and republish
python publish.py --clean --dry-run  # Preview cleanup
python publish.py --clean            # Actually clean
python publish.py --build --publish  # Rebuild and publish
```

### Integration with CI/CD

Add to your pipeline:

```yaml
- name: Build and Publish Documentation
  run: |
    python -m mkdocs build
    python publish.py --publish
  env:
    CONFLUENCE_URL: ${{ secrets.CONFLUENCE_URL }}
    CONFLUENCE_USERNAME: ${{ secrets.CONFLUENCE_USERNAME }}
    CONFLUENCE_API_TOKEN: ${{ secrets.CONFLUENCE_API_TOKEN }}
```
