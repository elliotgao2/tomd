# tomd

[![CI](https://img.shields.io/github/actions/workflow/status/elliotgao2/tomd/ci.yml?branch=master&style=for-the-badge&logo=githubactions&logoColor=white&label=CI)](https://github.com/elliotgao2/tomd/actions/workflows/ci.yml)
[![PyPI](https://img.shields.io/pypi/v/tomd?style=for-the-badge&logo=pypi&logoColor=white&label=PyPI&color=3775A9)](https://pypi.org/project/tomd/)
[![Python](https://img.shields.io/pypi/pyversions/tomd?style=for-the-badge&logo=python&logoColor=white&color=3776AB)](https://pypi.org/project/tomd/)
[![License](https://img.shields.io/pypi/l/tomd?style=for-the-badge&color=A31F34)](https://pypi.org/project/tomd/)
[![Downloads](https://img.shields.io/pypi/dm/tomd?style=for-the-badge&logo=pypi&logoColor=white&label=Downloads&color=5C7CFA)](https://pypi.org/project/tomd/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json&style=for-the-badge)](https://github.com/astral-sh/ruff)
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json&style=for-the-badge)](https://github.com/astral-sh/uv)

> Convert real-world HTML to clean Markdown.

`tomd` is a small, fast Python library that turns an HTML string into
Markdown — handy for archiving articles, normalising scraped content,
piping rendered pages into LLM context, or anywhere you'd rather work
with plain text than a DOM.

It walks the parsed tree with `lxml`, so it handles nested lists,
formatted table cells, fenced code blocks with language hints, HTML
entities, hard line breaks, and the messy markup you actually find in
the wild.

## Install

```bash
pip install tomd
# or
uv add tomd
```

Requires Python 3.10+.

## Quickstart

```python
import tomd

tomd.convert("<h1>Hello, world!</h1>")
# => '# Hello, world!\n'
```

Or via the class:

```python
from tomd import Tomd

Tomd("<p><b>bold</b> and <i>italic</i></p>").markdown
# => '**bold** and *italic*\n'
```

## What it converts

| Markdown               | HTML                                              |
| ---------------------- | ------------------------------------------------- |
| Headings               | `<h1>`–`<h6>`                                     |
| Bold / italic          | `<b>`, `<strong>`, `<i>`, `<em>`                  |
| Strikethrough          | `<del>`, `<s>`, `<strike>`                        |
| Inline code            | `<code>`, `<kbd>`, `<samp>`                       |
| Links                  | `<a href="...">` incl. relative, `mailto:`, title |
| Images                 | `<img src="..." alt="..." title="..."/>`          |
| Lists (nested, mixed)  | `<ul>`, `<ol start="N">`, `<li>`                  |
| Blockquotes            | `<blockquote>` (incl. nested, multi-paragraph)    |
| Horizontal rule        | `<hr/>`                                           |
| Fenced code blocks     | `<pre><code class="language-X">`                  |
| Tables                 | `<table>` with or without `<thead>`/`<tbody>`     |
| Hard line breaks       | `<br/>` → `  \n`                                  |
| Definition lists       | `<dl>` / `<dt>` / `<dd>`                          |

`<script>`, `<style>`, `<iframe>`, `<head>`, and friends are stripped.
HTML entities (`&amp;`, `&#8212;`, `&lt;`) are decoded. Unknown tags
fall through to their text content.

## Example

```python
from tomd import Tomd

html = """
<article>
  <h1>Heading</h1>
  <p><b>bold</b>, <i>italic</i>, and a <a href="https://example.com">link</a>.</p>
  <ul>
    <li>one</li>
    <li>two
      <ul><li>nested</li></ul>
    </li>
  </ul>
  <pre><code class="language-python">print("hi")</code></pre>
</article>
"""

print(Tomd(html).markdown)
```

````
# Heading

**bold**, *italic*, and a [link](https://example.com).

- one
- two
  - nested

```python
print("hi")
```
````

## Development

```bash
git clone https://github.com/elliotgao2/tomd.git
cd tomd
uv sync                       # install deps into .venv
uv run pytest                 # run tests
uv run ruff check .           # lint
uv run ruff format --check .  # format check
```

Install the pre-commit hooks:

```bash
uv run pre-commit install
```

## Contributing

Pull requests are welcome. For non-trivial changes, please open an issue
first. Make sure `uv run pytest`, `uv run ruff check .`, and
`uv run ruff format --check .` all pass before submitting.

## License

[MIT](LICENSE) © Elliot Gao
