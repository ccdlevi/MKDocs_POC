# MkDocs Documentation Site

This repository contains a documentation site built with MkDocs and the Material theme. It supports various diagram types and can publish content to Confluence.

## Features

- **Material Design**: Beautiful responsive design
- **Diagram Support**:
  - Mermaid for flowcharts and sequence diagrams
  - PlantUML for UML diagrams
  - Draw.io for complex diagrams
- **Confluence Publishing**: Automatically publish your docs to Confluence

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
