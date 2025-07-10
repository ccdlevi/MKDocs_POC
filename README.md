# MkDocs Documentation Site with Confluence Publishing

A professional documentation site built with MkDocs, Material theme, and integrated Confluence publishing. Designed for corporate environments with offline package support and robust SSL/authentication handling.

## ✅ Current Status

- **✅ MkDocs Build**: Fully functional
- **✅ Local Development**: Ready for use  
- **✅ Static Site Generation**: Working perfectly
- **✅ All Plugins**: Mermaid, PlantUML, Draw.io, Search, Minify
- **✅ Confluence Publishing**: Production-ready with custom plugin
- **✅ Corporate Environment**: SSL bypass, Bearer token auth support

## 🚀 Quick Start

```bash
# 1. Clone the repository
git clone <repository-url>
cd MKDocs_POC

# 2. Install all dependencies (includes local packages)
pip install -r requirements.txt

# 3. Install the custom Confluence publisher plugin
pip install -e .

# 4. Configure Confluence (optional)
cp .env.example .env
# Edit .env with your Confluence credentials

# 5. Start local development server
mkdocs serve

# 6. Build and publish to Confluence
mkdocs build
```

That's it! The documentation site is ready to use.

## Features

- **Material Design**: Beautiful responsive design with dark/light mode
- **Diagram Support**:
  - Mermaid for flowcharts and sequence diagrams
  - PlantUML for UML diagrams  
  - Draw.io for complex diagrams
- **Confluence Publishing**: Automated publishing with proper formatting
- **Offline Installation**: All dependencies available as local wheel files
- **Corporate Ready**: SSL bypass, Bearer token authentication
- **Corporate Network Ready**: Designed for environments with SSL inspection
- **Confluence Publishing**: Available but currently disabled due to SSL issues

## Requirements

- Python 3.7+
- pip

## Installation

1. Clone this repository:

```bash
git clone https://github.com/yourusername/mkdocs-site.git
cd mkdocs-site
```

2. Create and activate a virtual environment:

```bash
# Windows
python -m venv venv
.\venv\Scripts\Activate.ps1

# MacOS/Linux
python -m venv venv
source venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### Local Development

Run the local development server:

```bash
mkdocs serve
```

Then visit http://127.0.0.1:8000 in your browser.

### Building the Site

Build the static site:

```bash
mkdocs build
```

The site will be generated in the `site` directory.

### Docker Deployment

You can also run the documentation site using Docker:

1. Build and start the container:

```bash
docker-compose up -d
```

2. Visit http://localhost:8080 in your browser.

3. To stop the container:

```bash
docker-compose down
```

### Publishing to Confluence

1. Copy `.env.example` to `.env` and fill in your Confluence credentials:

```bash
cp .env.example .env
```

2. Edit the `.env` file with your Confluence details

3. Run the Confluence publisher:

```bash
python -m mkdocs_confluence_publisher
```

## Project Structure

```
.
├── docs/                 # Documentation files
│   ├── index.md          # Home page
│   ├── assets/           # CSS, JS, and media files
│   ├── diagrams/         # Diagram examples
│   └── user-guide/       # User guides
├── mkdocs.yml            # MkDocs configuration
├── .env.example          # Example environment variables
└── README.md             # This file
```

## Contributing

1. Fork the repository
2. Create a new branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License.

# Documentation Site

This project uses MkDocs with the Material theme to generate beautiful, feature-rich documentation. It supports advanced Markdown, Mermaid, PlantUML, and Draw.io diagrams, and can publish directly to Confluence.

## Prerequisites

- Python 3.8+
- pip
- Docker (for PlantUML rendering)

## Setup

1. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

2. **Run a local PlantUML server (required for PlantUML diagram rendering):**
   The PlantUML plugin is configured to use a local PlantUML server at `http://127.0.0.1:8080`.
   Start the server using Docker:
   ```sh
   docker run -d -p 8080:8080 plantuml/plantuml-server:jetty
   ```
   This is required for PlantUML diagrams to render in your documentation.

3. **Serve the documentation locally:**
   ```sh
   mkdocs serve
   ```
   Open your browser to [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

4. **Build the documentation:**
   ```sh
   mkdocs build
   ```

5. **Publish to Confluence:**
   The project uses the `confluence-publisher` plugin. Make sure your `mkdocs.yml` includes:
   ```yaml
   plugins:
     # ...existing plugins...
     - confluence-publisher:
         space_key: "MKDocs"     # Required: Confluence space key
         parent_page_id: 327683   # Required: ID of the parent page in Confluence
   ```
   Then run:
   ```sh
   python publish.py --publish
   ```

   Configure your Confluence credentials and settings in `.env` or `mkdocs.yml` as needed.

## Features
- Material theme with advanced navigation
- Mermaid, PlantUML, and Draw.io diagram support
- Confluence publishing
- Custom admonitions, tabs, and more

See the documentation for details on advanced Markdown features and diagram usage.
