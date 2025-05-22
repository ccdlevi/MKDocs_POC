# Versioning Documentation

This guide explains how to manage multiple versions of your documentation using MkDocs.

## Why Version Documentation?

Versioning documentation is important for several reasons:

1. **Historical Reference**: Users can access documentation for previous versions of your software
2. **Release Management**: You can prepare documentation for upcoming releases
3. **User Experience**: Users can easily switch between documentation versions
4. **Stability**: Changes to newer versions don't affect documentation for stable releases

## Using mike for Versioning

The recommended way to version MkDocs documentation is using [mike](https://github.com/jimporter/mike), a tool designed specifically for managing multiple versions of MkDocs sites.

### Installing mike

```bash
pip install mike
```

### Configuring mkdocs.yml for Versioning

Add the following to your mkdocs.yml:

```yaml
extra:
  version:
    provider: mike
    default: latest
```

### Basic Versioning Workflow

1. Build and deploy version 1.0.0 with the alias "latest":

```bash
mike deploy --push 1.0.0 latest
```

2. Set the default version:

```bash
mike set-default --push latest
```

3. When you release version 1.1.0, deploy it as the new "latest":

```bash
mike deploy --push 1.1.0 latest
```

4. For a major version 2.0.0, you might want to keep 1.x as "stable":

```bash
mike deploy --push 1.1.0 stable
mike deploy --push 2.0.0 latest
```

### Using the Version Manager Script

We've included a version manager script in the examples folder that simplifies the versioning process. You can use it like this:

```bash
# Deploy a new version with alias "latest"
python docs/examples/version_docs.py deploy --version 1.0.0 --alias latest

# List all versions
python docs/examples/version_docs.py list

# Delete a version
python docs/examples/version_docs.py delete --version 0.9.0
```

## GitHub Actions Workflow for Versioning

Here's an example GitHub Actions workflow that handles versioning:

```yaml
name: publish-versioned-docs

on:
  push:
    tags:
      - 'v*'
  workflow_dispatch:
    inputs:
      version:
        description: 'Version to deploy (format: X.Y.Z)'
        required: true
      alias:
        description: 'Alias for the version (e.g., latest, stable)'
        required: true

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.10'
          
      - name: Install dependencies
        run: pip install -r requirements.txt mike
      
      - name: Configure Git
        run: |
          git config --global user.name "GitHub Actions"
          git config --global user.email "actions@github.com"
      
      - name: Deploy manual version
        if: github.event_name == 'workflow_dispatch'
        run: |
          mike deploy --push ${{ github.event.inputs.version }} ${{ github.event.inputs.alias }}
      
      - name: Deploy tagged version
        if: github.event_name == 'push' && startsWith(github.ref, 'refs/tags/v')
        run: |
          VERSION=${GITHUB_REF#refs/tags/v}
          mike deploy --push $VERSION latest
          mike set-default --push latest
```

## Best Practices for Documentation Versioning

1. **Version Semantics**: Use semantic versioning (X.Y.Z) for your documentation versions
2. **Consistent Aliases**: Use consistent aliases like "latest" and "stable"
3. **Clear Navigation**: Ensure the version selector is visible and easy to use
4. **Documentation for Features**: Clearly mark features that are only available in specific versions
5. **Maintenance Strategy**: Decide which old versions to maintain and for how long
