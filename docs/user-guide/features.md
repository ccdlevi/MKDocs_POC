# Features

This page describes the key features of our documentation system based on MkDocs with the Material theme.

## Material Design Theme

Our documentation uses the [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/) theme which provides:

- Responsive design that works well on both desktop and mobile
- Multiple color schemes and dark mode support
- Built-in search functionality
- Automatic light/dark mode switching based on user preferences

## Markdown Extensions

We've enabled several Markdown extensions to enhance your writing experience:

### Admonitions

Create highlighted note boxes to draw attention to important information:

```markdown
!!! note "Custom Title"
    This is a note admonition with a custom title.

!!! warning
    This is a warning admonition.

!!! tip
    This is a tip admonition.
```

Which renders as:

!!! note "Custom Title"
    This is a note admonition with a custom title.

!!! warning
    This is a warning admonition.

!!! tip
    This is a tip admonition.

### Code Blocks with Syntax Highlighting

```python
def hello_world():
    print("Hello, world!")
```

### Task Lists

- [x] Completed task
- [ ] Incomplete task

### Tabbed Content

=== "Tab 1"
    Content for tab 1

=== "Tab 2"
    Content for tab 2

## Diagrams

Our documentation system supports multiple diagramming tools:

- [Mermaid](../diagrams/mermaid.md) for flow charts, sequence diagrams, and more
- [PlantUML](../diagrams/plantuml.md) for UML diagrams
- [Draw.io](../diagrams/drawio.md) for complex diagrams

## Math Equations

Use LaTeX syntax to insert mathematical formulas:

$$
f(x) = \int_{-\infty}^{\infty} \hat{f}(\xi) e^{2 \pi i \xi x} d\xi
$$

## Confluence Publishing

Automatically publish your documentation to Confluence with the [MkDocs Confluence Publisher](https://github.com/ml-tooling/mkdocs-confluence-publisher) plugin. This ensures your documentation stays in sync between your code repository and Confluence.

!!! confluence "Confluence Publishing Tips"
    When publishing to Confluence, remember these best practices:
    
    1. Use descriptive page titles that are unique across your space
    2. Add appropriate labels to make your content discoverable 
    3. Consider creating a dedicated space for your documentation
    4. Keep image sizes reasonable for better Confluence performance
    5. Test with a small section before publishing your entire documentation

This is an example of a custom admonition style specifically designed for Confluence-related tips.
