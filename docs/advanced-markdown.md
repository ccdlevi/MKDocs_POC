# Advanced Markdown Features

This page demonstrates advanced Markdown features available with the Material theme for MkDocs.

## Content Tabs

=== "Tab 1"
    This is the content of the first tab.

    ```python
    def hello_world():
        print("Hello from Tab 1!")
    ```

=== "Tab 2"
    This is the content of the second tab.

    ```javascript
    function helloWorld() {
        console.log("Hello from Tab 2!");
    }
    ```

=== "Tab 3"
    This is the content of the third tab.

    ```json
    {
        "message": "Hello from Tab 3!",
        "timestamp": "2025-05-22T12:00:00Z"
    }
    ```

## Annotations

```python
def bubble_sort(arr):
    n = len(arr) # (1)!
    
    for i in range(n):
        for j in range(0, n - i - 1): # (2)!
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j] # (3)!
    
    return arr
```

1. Get the length of the array
2. For each element, compare it with the rest of the unsorted array
3. Swap if the element is greater than the next element

## Admonitions

!!! note "Custom Note"
    This is a note admonition with a custom title.

!!! tip
    This is a tip admonition.

!!! warning "Important Warning"
    This is a warning admonition with a custom title.

!!! danger
    This is a danger admonition.

!!! info inline end
    This is an inline admonition that appears on the right side of the content.

This text will wrap around the inline admonition. Inline admonitions are useful for providing additional information without disrupting the flow of the main content. They can be positioned at the end of a paragraph or section.

## Keyboard Keys

Press ++ctrl+alt+delete++ to restart your computer.

Press ++ctrl+c++ to copy and ++ctrl+v++ to paste.

## Task Lists

- [x] Create project structure
- [x] Configure MkDocs
- [x] Add documentation pages
- [ ] Add custom theme
- [ ] Deploy to production

## Footnotes

Here is a text with a footnote reference[^1] and another[^2].

[^1]: This is the first footnote.
[^2]: This is the second footnote.

## Definition Lists

Term 1
:   Definition 1

Term 2
:   Definition 2
:   Another definition for term 2

## MathJax Integration

Inline math: $E = mc^2$

Block math:

$$
\frac{n!}{k!(n-k)!} = \binom{n}{k}
$$

## Icon Integration

:material-clock-time-three-outline: 3:00

:material-check: Task completed

:material-close: Task failed

:material-arrow-right: Next step
