# Draw.io DiagTo include a Draw.io diagram in your Markdown file, use the following syntax:

```markdown
![Diagram Title](../assets/diagrams/architecture.drawio)
```

For example, if you have a file named `architecture.drawio` in a folder named `assets`, you would include it like this:

```markdown
![System Architecture](../assets/diagrams/architecture.drawio)
```aw.io](https://www.draw.io/) (also known as diagrams.net) is a powerful diagramming tool that allows you to create complex diagrams with a user-friendly interface. The MkDocs Draw.io Exporter plugin enables you to embed Draw.io diagrams in your documentation.

## Getting Started with Draw.io

To include Draw.io diagrams in your documentation:

1. Create your diagram using Draw.io
2. Save the diagram as an `.drawio` or `.dio` file in your documentation project
3. Reference the diagram in your Markdown file

## Including Draw.io Diagrams

To include a Draw.io diagram in your Markdown file, use the following syntax:

```markdown
![Diagram Title](../assets/diagrams/architecture.drawio)
```

For example, if you have a file named `architecture.drawio` in a folder named `assets`, you would include it like this:

```markdown
![System Architecture](../assets/diagrams/architecture.drawio)
```

## Example Diagram

Here's an example of a Draw.io diagram showing the architecture of our documentation system:

![Architecture Diagram](../assets/diagrams/architecture.drawio)

This diagram shows how the browser interacts with the MkDocs server, which reads Markdown files and can publish content to Confluence.

## Creating Diagrams

To create Draw.io diagrams for your documentation:

1. Visit [Draw.io](https://app.diagrams.net/) or use the desktop application
2. Create your diagram using the extensive library of shapes and connectors
3. Save the diagram as a `.drawio` file
4. Add the file to your documentation project
5. Reference it in your Markdown

## Configuration

The Draw.io exporter plugin is configured in `mkdocs.yml`:

```yaml
plugins:
  - drawio-exporter:
      cache_dir: .drawio-exporter
      format: svg
```

This configuration:
- Caches generated images for performance
- Uses SVG format for high-quality, scalable diagrams

## Diagram Types You Can Create

Draw.io supports creating many types of diagrams, including:

- Flowcharts
- Network diagrams
- Organization charts
- UML diagrams
- Entity-relationship diagrams
- Floor plans
- Mind maps
- Infrastructure diagrams
- Wireframes
- And many more!

## Best Practices

1. **Use descriptive filenames** for your diagram files
2. **Keep diagrams focused** on a single concept or view
3. **Use consistent styling** across your diagram components
4. **Leverage layers** for complex diagrams to separate concerns
5. **Add text labels** to clarify diagram elements
6. **Use colors meaningfully** to group related components
7. **Export in SVG format** for best quality

## Version Control Considerations

Since Draw.io files are XML-based, they work well with version control systems. This allows you to track changes to your diagrams over time.

## Converting Existing Images

If you have existing diagrams as image files, you can import them into Draw.io:

1. Open Draw.io
2. Select File > Import From
3. Choose your image file
4. The image will be placed on the canvas for you to enhance or modify

## Troubleshooting

If your diagram doesn't render correctly:

1. Check that the path to the diagram file is correct
2. Verify that the drawio-exporter plugin is correctly installed and configured
3. Check for syntax errors in your diagram reference
4. Try clearing the cache directory (.drawio-exporter) if you've updated a diagram that isn't showing changes
