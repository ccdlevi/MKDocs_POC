# Getting Started

Welcome to the Getting Started guide for our documentation system. This page will walk you through setting up and using the MkDocs documentation system with integrated Confluence publishing.

## Prerequisites

Before you start, make sure you have the following installed:

- Python 3.8 or higher
- pip (Python package manager)
- Git (for version control)

## Quick Setup

This project includes all necessary packages and a custom Confluence publisher plugin. Getting started is simple:

### 1. Clone and Setup

```bash
git clone https://github.com/yourusername/mkdocs-site.git
cd mkdocs-site
```

### 2. Install Dependencies

All required packages are included locally. Simply run:

```bash
pip install -r requirements.txt
pip install -e .  # Install the custom Confluence publisher plugin
```

This will install:
- MkDocs with Material theme
- Mermaid diagram support
- PlantUML diagram support  
- Draw.io diagram support
- Custom Confluence publisher plugin
- All other necessary dependencies

### 3. Configure Environment (Optional)

If you plan to publish to Confluence, create a `.env` file with your credentials:

```bash
# Copy the example and edit with your details
cp .env.example .env
```

Edit `.env` with your Confluence details:
```
CONFLUENCE_URL=https://your-confluence-instance.com
CONFLUENCE_USERNAME=your-username
CONFLUENCE_API_TOKEN=your-api-token
```

!!! tip "API Token"
    Generate an API token from your Confluence profile settings for secure authentication.

## Running the Documentation Locally

To preview the documentation locally:

```bash
mkdocs serve
```

Or use the configured VS Code task: **Ctrl+Shift+P** → "Tasks: Run Task" → "Serve MkDocs Site"

This starts a local server at `http://127.0.0.1:8000/` with live reloading.

## Adding New Content

### Creating New Pages

1. **Create a Markdown file** in the appropriate directory under `docs/`:
   ```bash
   # Example: Create a new user guide page
   touch docs/user-guide/new-feature.md
   ```

2. **Add to navigation** in `mkdocs.yml` under the `nav` section:
   ```yaml
   nav:
     - User Guide:
       - New Feature: user-guide/new-feature.md
   ```

3. **Write content** using Markdown syntax with support for:
   - Tables, code blocks, admonitions
   - Mermaid diagrams
   - PlantUML diagrams  
   - Draw.io diagrams
   - Math expressions

### Supported Diagram Types

This documentation system supports multiple diagram formats:

**Mermaid** (for flowcharts, sequence diagrams):
````mermaid
graph TD
    A[Start] --> B[Process]
    B --> C[End]
````

**PlantUML** (for UML diagrams):
```
![System Architecture](../assets/diagrams/system-architecture.puml)
```

**Draw.io** (for complex diagrams):
```
![Architecture](../assets/diagrams/architecture.drawio)
```

## Building for Production

### Local Build

Build the static site:

```bash
mkdocs build
```

Or use VS Code task: **Ctrl+Shift+P** → "Tasks: Run Task" → "Build MkDocs Site"

### Publishing to Confluence

The integrated Confluence publisher automatically publishes during build when configured:

1. **Configure credentials** in `.env` file (see setup above)

2. **Configure publishing** in `mkdocs.yml`:
   ```yaml
   plugins:
     - confluence_publisher:
         confluence_prefix: "MkDocs - "
         space_key: "YOUR_SPACE"
         parent_page_id: 123456789
         dry_run: false  # Set to true for testing
         verify_ssl: false  # For corporate environments
         upload_attachments: false  # Disable if permission issues
   ```

3. **Publish documentation**:
   ```bash
   mkdocs build  # Automatically publishes to Confluence
   ```

The plugin will:
- ✅ Create/update pages with proper hierarchy
- ✅ Convert Markdown to Confluence format
- ✅ Handle code blocks, tables, and admonitions  
- ✅ Work in corporate environments (SSL bypass, Bearer auth)
- ✅ Provide detailed logging and error handling

!!! success "Confluence Publishing"
    The custom Confluence publisher plugin is production-ready and handles common corporate environment challenges like SSL certificates and authentication.

## Troubleshooting

### Common Issues

**Plugin not found error:**
```bash
pip install -e .  # Reinstall the local plugin
```

**Confluence 400/403 errors:**
- Check API token permissions
- Set `upload_attachments: false` if attachment issues
- Verify space key and parent page ID

**Diagram rendering issues:**
- Ensure diagram files exist at referenced paths
- Check PlantUML server is running (if using local server)
- Verify Draw.io desktop app is installed

**SSL/Certificate issues:**
- Set `verify_ssl: false` in plugin config
- Use Bearer token authentication instead of Basic auth

### Getting Help

- Check the [Features](features.md) page for advanced usage
- See [Publishing to Confluence](publishing-to-confluence.md) for detailed publishing setup
- Review the plugin logs for detailed error information

## Next Steps

- **Learn Features**: Visit the [Features](features.md) page to explore advanced capabilities
- **Setup Publishing**: Configure [Confluence Publishing](publishing-to-confluence.md) for your team
- **Create Diagrams**: Learn about supported [diagram formats](../diagrams/mermaid.md)
- **Customize**: Modify themes and styling in `mkdocs.yml`
