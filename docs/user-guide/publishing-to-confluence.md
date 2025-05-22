# Publishing to Confluence

This guide provides detailed instructions on how to publish your MkDocs documentation to Confluence using the MkDocs Confluence Publisher plugin.

## Prerequisites

Before you can publish to Confluence, you'll need:

1. A Confluence instance where you have write access
2. A Space Key for the Confluence space where you want to publish
3. The parent page ID under which your documentation will be published
4. API token or credentials for authentication

## Configuration

### Step 1: Set Up Environment Variables

Create a `.env` file in your project root by copying the example file:

```bash
cp .env.example .env
```

Then edit the `.env` file with your Confluence details:

```
CONFLUENCE_URL=https://your-instance.atlassian.net
CONFLUENCE_SPACE_KEY=DOCS
CONFLUENCE_PARENT_PAGE_ID=123456
CONFLUENCE_USERNAME=your.email@example.com
CONFLUENCE_PASSWORD=your_api_token_here
```

### Step 2: Update MkDocs Configuration

Uncomment and configure the Confluence section in your `mkdocs.yml` file:

```yaml
extra:
  confluence:
    url: https://your-confluence-instance.atlassian.net
    space_key: DOCS
    parent_page_id: 123456
    username: your_username
    password: your_api_token  # Use API token, not your actual password
```

## Publishing Process

### Using the Helper Script

The simplest way to publish is using the included helper script:

```bash
python publish.py --publish
```

This script will:
1. Build the MkDocs site
2. Load your Confluence credentials from the `.env` file
3. Publish the content to Confluence

### Manual Publishing

If you prefer to publish manually:

1. Build the MkDocs site:
   ```bash
   mkdocs build
   ```

2. Run the Confluence publisher:
   ```bash
   python -m mkdocs_confluence_publisher
   ```

## Finding Your Confluence Page ID

To find the ID of a Confluence page to use as the parent page:

1. Navigate to the page in Confluence
2. Look at the URL, which should contain something like: `pageId=123456`
3. The number after `pageId=` is your page ID

## Troubleshooting

### Authentication Issues

If you encounter authentication issues:

1. Verify that your username and API token are correct
2. Ensure you're using an API token, not your actual password
3. Check that you have the necessary permissions in Confluence

### Missing Pages

If some pages don't appear in Confluence:

1. Check the console output for errors
2. Verify that the pages are included in the MkDocs navigation
3. Ensure there are no formatting issues in the Markdown files

### Formatting Issues

If the formatting in Confluence doesn't match the MkDocs output:

1. Note that not all Markdown features are supported in Confluence
2. Complex elements like tabs may not render correctly
3. Consider simplifying problematic sections for better Confluence compatibility

## Best Practices

1. **Use Clear Titles**: Confluence uses page titles for navigation
2. **Keep it Simple**: Complex formatting may not translate well to Confluence
3. **Use Labels**: Configure labels to make your documentation easier to find
4. **Test First**: Test publishing with a small subset of pages before publishing everything
5. **Version Control**: Document which version was published to Confluence
