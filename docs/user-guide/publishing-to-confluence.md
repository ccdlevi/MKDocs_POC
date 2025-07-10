# Publishing to Confluence

This documentation system includes a **production-ready Confluence publisher plugin** that seamlessly integrates with the MkDocs build process. The plugin handles authentication, SSL issues, content conversion, and maintains proper page hierarchy.

## ✅ Current Status

**✅ Confluence Publisher Plugin**: Production-ready and fully functional  
**✅ Corporate Environment Support**: SSL bypass and Bearer token authentication  
**✅ Automatic Publishing**: Integrated with `mkdocs build` command  
**✅ Robust Error Handling**: Graceful failure recovery and detailed logging  
**✅ Content Conversion**: Professional Markdown → Confluence format conversion

## 🚀 Quick Start

### 1. Environment Setup

Create a `.env` file with your Confluence credentials:

```bash
# Copy the example and customize
cp .env.example .env
```

Edit `.env` with your details:
```env
# Your Confluence instance URL (without trailing slash)
CONFLUENCE_URL=https://your-confluence-instance.com

# Your Confluence username (email address)
CONFLUENCE_USERNAME=your-email@company.com

# Your Confluence API token (generate from Profile → Personal Access Tokens)
CONFLUENCE_API_TOKEN=your-api-token-here
```

!!! tip "API Token Generation"
    Generate your API token from Confluence: **Profile** → **Personal Access Tokens** → **Create Token**

### 2. Plugin Configuration

Configure the plugin in `mkdocs.yml`:

```yaml
plugins:
  - confluence_publisher:
      confluence_prefix: "MkDocs - "     # Prefix for page titles
      space_key: "DOCS"                 # Your Confluence space key
      parent_page_id: 123456789          # Parent page ID for organization
      dry_run: false                    # Set to true for testing
      verify_ssl: false                 # Set to false for corporate environments
      upload_attachments: false         # Disable if permission issues
```

### 3. Publish Documentation

**Simple One-Command Publishing:**
```bash
mkdocs build  # Automatically builds AND publishes to Confluence
```

**Development Workflow:**
```bash
# 1. Develop with live preview
mkdocs serve

# 2. Test publishing without changes
# Set dry_run: true in mkdocs.yml, then:
mkdocs build

# 3. Publish for real
# Set dry_run: false in mkdocs.yml, then:
mkdocs build
```

## 🔧 Plugin Features

### Seamless Integration
- **✅ MkDocs Plugin**: Fully integrated with the MkDocs build process
- **✅ Automatic Publishing**: No separate commands needed
- **✅ VS Code Tasks**: Pre-configured tasks for common operations

### Corporate Environment Support
- **✅ SSL Bypass**: Handles corporate certificate issues automatically
- **✅ Bearer Token Auth**: Modern OAuth-style authentication (preferred)
- **✅ Basic Auth Fallback**: Traditional username/password if needed
- **✅ Proxy Support**: Works through corporate proxies

### Content Processing
- **✅ Page Hierarchy**: Maintains proper parent-child relationships
- **✅ Format Conversion**: Markdown → Confluence storage format
- **✅ Code Blocks**: Syntax highlighting preserved
- **✅ Tables**: Professional table formatting
- **✅ Admonitions**: Note/Warning/Tip boxes converted properly
- **✅ Links**: Internal links updated to Confluence page references

### Error Handling
- **✅ Robust Recovery**: Continues processing even if individual pages fail
- **✅ Detailed Logging**: Clear error messages and debugging information
- **✅ Graceful Degradation**: Warns about issues without breaking the build
- **✅ Content Sanitization**: Prevents API errors from malformed content

## 📋 Configuration Reference

### Plugin Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `confluence_prefix` | string | `""` | Prefix added to all page titles |
| `space_key` | string | **required** | Confluence space key (e.g., "DOCS") |
| `parent_page_id` | integer | **required** | Parent page ID for organization |
| `dry_run` | boolean | `false` | Test mode - no actual changes made |
| `verify_ssl` | boolean | `false` | SSL certificate verification |
| `upload_attachments` | boolean | `true` | Enable/disable file attachments |

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `CONFLUENCE_URL` | ✅ | Your Confluence instance URL |
| `CONFLUENCE_USERNAME` | ⚠️ | Username (usually email) |
| `CONFLUENCE_API_TOKEN` | ✅ | API token for authentication |

!!! note "Authentication Priority"
    The plugin prioritizes Bearer token authentication over Basic auth, as it works better in corporate environments.

## 🎯 Content Conversion

### Supported Elements

The plugin converts MkDocs content to professional Confluence format:

| MkDocs Element | Confluence Output | Status |
|----------------|------------------|--------|
| **Headers** | Native Confluence headers | ✅ Full support |
| **Code Blocks** | Confluence code macros with syntax highlighting | ✅ Full support |
| **Tables** | Confluence table format | ✅ Full support |
| **Admonitions** | Info/Warning/Error macros | ✅ Full support |
| **Links** | Confluence page links | ✅ Full support |
| **Images** | Confluence attachments | ⚠️ Optional |
| **Mermaid Diagrams** | PNG images with source code | ✅ Enhanced |
| **PlantUML Diagrams** | PNG images from SVG | ✅ Enhanced |
| **Math Expressions** | LaTeX format preserved | ✅ Preserved |

### Conversion Examples

**Admonitions:**
```markdown
!!! note "Important"
    This becomes a Confluence info macro.
```
→ Confluence Info macro with proper styling

**Code Blocks:**
````markdown
```python
def hello_world():
    print("Hello!")
```
````
→ Confluence code macro with Python syntax highlighting

**Tables:**
```markdown
| Feature | Status |
|---------|--------|
| Publishing | ✅ Working |
```
→ Professional Confluence table with proper formatting

**Enhanced Diagram Support:**
Our publisher now provides enhanced diagram handling for Confluence:

- **Mermaid Diagrams**: Converted to PNG images with source code for reference
  - Supports two rendering options:
    - `markdown-mermaid-cli`: Python package (recommended)
    - `mermaid-cli`: Node.js package (alternative)
  - Falls back to code display when neither tool is available
- **PlantUML Diagrams**: Converted to PNG images automatically
  - Uses CairoSVG for high-quality conversion
  - Falls back to placeholders when SVG conversion fails
- **Draw.io Diagrams**: May render with limitations

PNG images are automatically attached to the Confluence page, providing a much better viewing experience than before. For the best interactive experience, users can still refer to the web version.

## 🔍 Finding Your Configuration Values

### Space Key
1. Go to your Confluence space
2. Look in the URL: `https://yoursite.com/spaces/DOCS/` → Space key is `DOCS`
3. Or check the space settings page

### Parent Page ID
1. Navigate to the page you want as the parent
2. Look at the URL: `...pageId=123456789` → Page ID is `123456789`
3. Or view page source and search for `content-id`

### API Token
1. Go to Confluence → **Profile** → **Personal Access Tokens**
2. Click **Create Token**
3. Give it a descriptive name (e.g., "MkDocs Publisher")
4. Copy the generated token (save it securely!)

## 🔧 VS Code Integration

The project includes pre-configured VS Code tasks for easy development:

**Available Tasks:**
- **Serve MkDocs Site**: Start development server with live reload
- **Build MkDocs Site**: Build static site and publish to Confluence
- **Publish to Confluence**: Legacy task (now integrated with build)

**Access Tasks:**
`Ctrl+Shift+P` → "Tasks: Run Task" → Select desired task

## 🚨 Troubleshooting

### Common Issues

**🔴 Plugin Not Found Error**
```
ERROR: The "confluence_publisher" plugin is not installed
```
**Solution:**
```bash
pip install -e .  # Reinstall the local plugin
```

**🔴 Authentication Failed (401)**
```
ERROR: 401 Client Error: Unauthorized
```
**Solutions:**
1. Check your API token is correct and active
2. Verify username is your email address
3. Ensure you have access to the specified space
4. Test with Bearer token authentication (preferred)

**🔴 SSL Certificate Issues**
```
ERROR: SSL: CERTIFICATE_VERIFY_FAILED
```
**Solutions:**
1. Set `verify_ssl: false` in plugin configuration (recommended for corporate environments)
2. The plugin automatically handles corporate SSL issues
3. Contact IT if problems persist

**🔴 Page Creation Failed (400/403)**
```
ERROR: Failed to update page content: 400/403 Client Error
```
**Solutions:**
1. Verify you have write permissions in the space
2. Check parent page ID exists and is accessible
3. Set `upload_attachments: false` if attachment permission issues
4. Use `dry_run: true` to test without making changes

**🔴 Content Formatting Issues**
```
ERROR: Failed to update page content for diagrams\drawio.md
```
**Solutions:**
1. Check if Draw.io exporter is causing issues (known issue)
2. Temporarily disable problematic plugins
3. Use simpler content for testing
4. Check logs for specific formatting problems

### Performance Issues

**Slow Publishing:**
- Use `dry_run: true` to test without actual publishing
- Disable `upload_attachments` if not needed
- Check network connectivity to Confluence instance

**Build Failures:**
- Check MkDocs builds successfully first: `mkdocs build`
- Verify all referenced files exist
- Review error logs for specific issues

## 📋 Best Practices

### Content Guidelines
1. **📝 Clear Titles**: Use descriptive, unique page titles
2. **📁 Hierarchy**: Organize content under appropriate parent pages
3. **🔗 Simple Links**: Use relative links for better conversion
4. **📊 Standard Formatting**: Stick to common Markdown for best results

### Development Workflow
1. **🔧 Develop Locally**: Use `mkdocs serve` for live preview
2. **🧪 Test First**: Use `dry_run: true` to preview changes
3. **📋 Incremental Publishing**: Test with small changes first
4. **🔄 Regular Builds**: Publish frequently to catch issues early

### Security & Maintenance
1. **🔐 Secure Credentials**: Never commit API tokens to version control
2. **🔄 Token Rotation**: Update API tokens per company policy
3. **🛡️ Minimal Permissions**: Only grant necessary space access
4. **📊 Monitor Logs**: Review build logs for issues

## 🚀 Advanced Usage

### Custom Configuration Example

```yaml
# mkdocs.yml - Production configuration
plugins:
  - confluence_publisher:
      confluence_prefix: "[TEAM-DOCS] "
      space_key: "TEAMDOCS"
      parent_page_id: 987654321
      dry_run: false
      verify_ssl: false
      upload_attachments: false
```

### CI/CD Integration

Add to your pipeline (GitHub Actions example):

```yaml
- name: Build and Publish Documentation
  run: |
    pip install -r requirements.txt
    pip install -e .
    mkdocs build
  env:
    CONFLUENCE_URL: ${{ secrets.CONFLUENCE_URL }}
    CONFLUENCE_USERNAME: ${{ secrets.CONFLUENCE_USERNAME }}
    CONFLUENCE_API_TOKEN: ${{ secrets.CONFLUENCE_API_TOKEN }}
```

### Multiple Environment Setup

```bash
# Development
cp .env.example .env.dev
# Edit .env.dev with dev Confluence settings

# Production  
cp .env.example .env.prod
# Edit .env.prod with production settings

# Use specific environment
cp .env.dev .env  # For development
mkdocs build
```

!!! success "Production Ready"
    The Confluence publisher plugin is production-ready and handles all common corporate environment challenges. It provides seamless integration between your MkDocs documentation and Confluence, maintaining professional formatting and proper page hierarchy.
