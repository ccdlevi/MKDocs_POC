# Getting Started

Welcome to the Getting Started guide for our documentation system. This page will walk you through the basics of using and contributing to our documentation.

## Prerequisites

Before you start, make sure you have the following installed:

- Python 3.7 or higher
- pip (Python package manager)
- Git (optional, for version control)

## Installation

1. First, create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install MkDocs and all required plugins:

```bash
pip install mkdocs-material mkdocs-mermaid2-plugin mkdocs-plantuml mkdocs-drawio-exporter mkdocs-confluence-publisher
```

3. Clone the documentation repository:

```bash
git clone https://github.com/yourusername/mkdocs-site.git
cd mkdocs-site
```

## Running the Documentation Locally

To preview the documentation locally, run:

```bash
mkdocs serve
```

This will start a local server at `http://127.0.0.1:8000/` where you can view your documentation as you edit it.

## Adding New Content

1. Create a new Markdown file in the appropriate directory under `docs/`
2. Add the file to the navigation in `mkdocs.yml` under the `nav` section
3. Write your content using Markdown syntax

## Building for Production

To build the static site for production, run:

```bash
mkdocs build
```

This creates a `site` directory with the compiled HTML files that you can deploy to any web server.

## Publishing to Confluence

To publish your documentation to Confluence, you need to configure your Confluence credentials in the `mkdocs.yml` file:

1. Uncomment the `extra.confluence` section in `mkdocs.yml`
2. Fill in your Confluence URL, space key, and credentials
3. Run the following command:

```bash
mkdocs build
python -m mkdocs_confluence_publisher
```

!!! note "API Token"
    For security reasons, use an API token instead of your actual password.

## Next Steps

Learn about the features available in our documentation system by visiting the [Features](features.md) page.
