# tomd

[![CI](https://img.shields.io/github/actions/workflow/status/elliotgao2/tomd/ci.yml?branch=master&style=for-the-badge&logo=githubactions&logoColor=white&label=CI)](https://github.com/elliotgao2/tomd/actions/workflows/ci.yml)
[![PyPI](https://img.shields.io/pypi/v/tomd?style=for-the-badge&logo=pypi&logoColor=white&label=PyPI&color=3775A9)](https://pypi.org/project/tomd/)
[![Python](https://img.shields.io/pypi/pyversions/tomd?style=for-the-badge&logo=python&logoColor=white&color=3776AB)](https://pypi.org/project/tomd/)
[![License](https://img.shields.io/pypi/l/tomd?style=for-the-badge&color=A31F34)](https://pypi.org/project/tomd/)
[![Downloads](https://img.shields.io/pypi/dm/tomd?style=for-the-badge&logo=pypi&logoColor=white&label=Downloads&color=5C7CFA)](https://pypi.org/project/tomd/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json&style=for-the-badge)](https://github.com/astral-sh/ruff)
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json&style=for-the-badge)](https://github.com/astral-sh/uv)

> Convert HTML to Markdown.

`tomd` is a small Python library that takes an HTML string and returns the
Markdown that produced it (or an approximation, when the HTML wasn't
originally Markdown). Handy for archiving articles, scraped blog posts, or
anything else where you'd rather work with plain text than DOM trees.

## Install

```bash
pip install tomd
```

Requires Python 3.10+.

## Quickstart

```python
import tomd

tomd.convert("<h1>Hello, world!</h1>")
# => '\n# Hello, world!\n'
```

Or via the class:

```python
from tomd import Tomd

Tomd("<h1>Hello, world!</h1>").markdown
```

## What it supports

| Markdown        | HTML                                  |
| --------------- | ------------------------------------- |
| Headings        | `<h1>`–`<h6>`                         |
| Bold / italic   | `<b>`, `<strong>`, `<i>`, `<em>`      |
| Inline code     | `<code>`                              |
| Strikethrough   | `<del>`                               |
| Links           | `<a href="https://...">`              |
| Images          | `<img src="..." alt="..."/>`          |
| Unordered lists | `<ul><li>...</li></ul>`               |
| Ordered lists   | `<ol><li>...</li></ol>`               |
| Blockquotes     | `<blockquote>...</blockquote>`        |
| Horizontal rule | `<hr/>`                               |
| Code blocks     | `<pre><code>...</code></pre>`         |
| Tables          | `<table><thead>...<tbody>...</table>` |

If your HTML can't be cleanly expressed in Markdown (nested layouts,
floating divs, etc.), the output will lose some structure — `tomd` aims at
the round-trip Markdown → HTML → Markdown case, not arbitrary HTML.

## Example

```python
from tomd import Tomd

html = """
<h1>Heading</h1>
<p><b>bold</b> and <i>italic</i> and <a href="https://example.com">a link</a></p>
<ul>
  <li>one</li>
  <li>two</li>
</ul>
<blockquote>a quote</blockquote>
"""

print(Tomd(html).markdown)
```

```
# Heading

**bold** and *italic* and [a link](https://example.com)

- one
- two

> a quote
```

## Development

```bash
git clone https://github.com/elliotgao2/tomd.git
cd tomd
uv sync             # install deps into .venv
uv run pytest       # run tests
uv run ruff check . # lint
```

We use [uv](https://github.com/astral-sh/uv) for packaging and
[ruff](https://github.com/astral-sh/ruff) for lint + format. Install the
pre-commit hooks:

```bash
uv run pre-commit install
```

## Roadmap

- [x] Headings, emphasis, links, images, lists, blockquotes, tables, HR,
      code blocks
- [ ] Nested lists
- [ ] CLI (`tomd < input.html > output.md`)

## Contributing

Pull requests are welcome. For non-trivial changes, please open an issue
first to discuss. Make sure `uv run pytest` and `uv run ruff check .` pass
before submitting.

## License

[MIT](LICENSE) © Elliot Gao
