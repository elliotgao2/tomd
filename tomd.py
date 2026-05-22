"""Convert HTML to Markdown.

Tree-walking converter built on lxml. The public API stays small:

    >>> import tomd
    >>> tomd.convert("<h1>Hi</h1>")
    '# Hi\n'

    >>> from tomd import Tomd
    >>> Tomd("<p><b>bold</b></p>").markdown
    '**bold**\n'
"""

from __future__ import annotations

import re

from lxml import etree
from lxml import html as lh

__all__ = ["Tomd", "convert"]


# Tags whose subtree should never appear in the output.
_SKIP_TAGS = frozenset(
    {
        "head",
        "meta",
        "link",
        "title",
        "script",
        "style",
        "noscript",
        "iframe",
        "object",
        "embed",
        "svg",
        "canvas",
        "template",
        "input",
        "button",
        "select",
        "textarea",
    }
)

# Block-level containers without a dedicated handler — they emit their
# children separated from surrounding content by a blank line.
_BLOCK_PASS_TAGS = frozenset(
    {
        "div",
        "section",
        "article",
        "main",
        "header",
        "footer",
        "aside",
        "nav",
        "figure",
        "figcaption",
        "details",
        "summary",
        "form",
        "fieldset",
        "address",
        "dialog",
    }
)


_WS_RE = re.compile(r"[ \t\n\r\f\v]+")


class _Converter:
    def __init__(self) -> None:
        self._list_stack: list[tuple[str, int]] = []
        self._in_pre = 0

    # ----- entry point -----

    def convert(self, html: str) -> str:
        if html is None:
            return ""
        s = str(html)
        if not s.strip():
            return ""
        try:
            root = lh.fragment_fromstring(s, create_parent="div")
        except (etree.ParserError, etree.XMLSyntaxError, ValueError):
            return ""
        rendered = self._render(root)
        return self._cleanup(rendered)

    @staticmethod
    def _cleanup(text: str) -> str:
        text = text.replace("\r\n", "\n").replace("\r", "\n")
        # Strip trailing whitespace per line, but keep the markdown
        # hard-break sentinel ("  " at end of line).
        out_lines = []
        for line in text.split("\n"):
            if line.endswith("  ") and line.strip():
                out_lines.append(line.rstrip(" \t") + "  ")
            else:
                out_lines.append(line.rstrip())
        text = "\n".join(out_lines)
        text = re.sub(r"\n{3,}", "\n\n", text)
        return text.strip("\n") + "\n" if text.strip() else ""

    # ----- generic dispatch -----

    def _render(self, node) -> str:
        tag = node.tag
        if not isinstance(tag, str):
            # Comment, ProcessingInstruction, etc.
            return ""
        tag = tag.lower()
        if tag in _SKIP_TAGS:
            return ""
        handler = getattr(self, f"_h_{tag}", None)
        if handler is None:
            if tag in _BLOCK_PASS_TAGS:
                inner = self._render_children(node).strip()
                return f"\n\n{inner}\n\n" if inner else ""
            return self._render_children(node)
        return handler(node)

    def _render_children(self, node) -> str:
        parts: list[str] = []
        if node.text:
            parts.append(self._text(node.text))
        for child in node:
            parts.append(self._render(child))
            if child.tail:
                parts.append(self._text(child.tail))
        return "".join(parts)

    def _text(self, s: str) -> str:
        if self._in_pre:
            return s
        return _WS_RE.sub(" ", s)

    def _inline(self, node) -> str:
        return self._render_children(node).strip()

    def _text_content(self, node) -> str:
        """Plain text of a subtree, with <br> rendered as newline."""
        parts: list[str] = []
        if node.text:
            parts.append(node.text)
        for child in node:
            tag = child.tag if isinstance(child.tag, str) else ""
            if tag.lower() == "br":
                parts.append("\n")
            elif tag.lower() in _SKIP_TAGS:
                pass
            else:
                parts.append(self._text_content(child))
            if child.tail:
                parts.append(child.tail)
        return "".join(parts)

    # ----- headings -----

    def _heading(self, node, level: int) -> str:
        content = self._inline(node)
        return f"\n\n{'#' * level} {content}\n\n" if content else ""

    def _h_h1(self, n):
        return self._heading(n, 1)

    def _h_h2(self, n):
        return self._heading(n, 2)

    def _h_h3(self, n):
        return self._heading(n, 3)

    def _h_h4(self, n):
        return self._heading(n, 4)

    def _h_h5(self, n):
        return self._heading(n, 5)

    def _h_h6(self, n):
        return self._heading(n, 6)

    # ----- block elements -----

    def _h_p(self, node) -> str:
        content = self._render_children(node).strip()
        return f"\n\n{content}\n\n" if content else ""

    def _h_hr(self, node) -> str:
        return "\n\n---\n\n"

    def _h_br(self, node) -> str:
        if self._in_pre:
            return "\n"
        return "  \n"

    def _h_blockquote(self, node) -> str:
        inner = self._render_children(node)
        inner = "\n".join(line.rstrip() for line in inner.split("\n"))
        inner = re.sub(r"\n{3,}", "\n\n", inner).strip("\n")
        if not inner:
            return ""
        lines = inner.split("\n")
        quoted = "\n".join(f"> {ln}" if ln else ">" for ln in lines)
        return f"\n\n{quoted}\n\n"

    # ----- inline emphasis -----

    def _h_b(self, n):
        c = self._inline(n)
        return f"**{c}**" if c else ""

    _h_strong = _h_b

    def _h_i(self, n):
        c = self._inline(n)
        return f"*{c}*" if c else ""

    _h_em = _h_i
    _h_cite = _h_i
    _h_dfn = _h_i
    _h_var = _h_i

    def _h_del(self, n):
        c = self._inline(n)
        return f"~~{c}~~" if c else ""

    _h_s = _h_del
    _h_strike = _h_del

    def _h_u(self, n):
        return self._inline(n)

    _h_small = _h_u
    _h_abbr = _h_u
    _h_time = _h_u
    _h_q = _h_u

    def _h_mark(self, n):
        c = self._inline(n)
        return f"=={c}==" if c else ""

    def _h_sub(self, n):
        c = self._inline(n)
        return f"~{c}~" if c else ""

    def _h_sup(self, n):
        c = self._inline(n)
        return f"^{c}^" if c else ""

    def _h_kbd(self, n):
        c = self._inline(n)
        return f"`{c}`" if c else ""

    _h_samp = _h_kbd
    _h_tt = _h_kbd

    def _h_code(self, node) -> str:
        if self._in_pre:
            return self._render_children(node)
        content = self._text_content(node)
        content = _WS_RE.sub(" ", content).strip()
        if not content:
            return ""
        # If content contains backticks, pad fence to escape them.
        if "`" in content:
            runs = re.findall(r"`+", content)
            n = max(len(r) for r in runs) + 1
            fence = "`" * n
            pad = " " if content.startswith("`") or content.endswith("`") else ""
            return f"{fence}{pad}{content}{pad}{fence}"
        return f"`{content}`"

    # ----- links and images -----

    def _h_a(self, node) -> str:
        href = (node.get("href") or "").strip()
        title = node.get("title")
        text = self._render_children(node).strip()
        if not href:
            return text
        if not text:
            text = href
        url = self._format_url(href)
        if title:
            esc = title.replace('"', '\\"')
            return f'[{text}]({url} "{esc}")'
        return f"[{text}]({url})"

    def _h_img(self, node) -> str:
        src = (node.get("src") or "").strip()
        alt = (node.get("alt") or "").replace("\n", " ").strip()
        title = node.get("title")
        url = self._format_url(src)
        if title:
            esc = title.replace('"', '\\"')
            return f'![{alt}]({url} "{esc}")'
        return f"![{alt}]({url})"

    @staticmethod
    def _format_url(url: str) -> str:
        if not url:
            return ""
        # Wrap URLs with spaces or unbalanced parens in <...>.
        if " " in url or "\t" in url:
            return f"<{url}>"
        if url.count("(") != url.count(")"):
            return f"<{url}>"
        return url

    def _h_span(self, node) -> str:
        return self._render_children(node)

    # ----- lists -----

    def _h_ul(self, node) -> str:
        return self._render_list(node, ordered=False)

    def _h_ol(self, node) -> str:
        try:
            start = int(node.get("start") or "1")
        except ValueError:
            start = 1
        return self._render_list(node, ordered=True, start=start)

    def _render_list(self, node, *, ordered: bool, start: int = 1) -> str:
        kind = "ol" if ordered else "ul"
        self._list_stack.append((kind, start - 1))
        try:
            items: list[str] = []
            for child in node:
                if isinstance(child.tag, str) and child.tag.lower() == "li":
                    items.append(self._render_li(child))
            inner = "\n".join(items)
            if not inner:
                return ""
            if len(self._list_stack) > 1:
                return "\n" + inner + "\n"
            return f"\n\n{inner}\n\n"
        finally:
            self._list_stack.pop()

    def _render_li(self, node) -> str:
        kind, idx = self._list_stack[-1]
        if kind == "ol":
            idx += 1
            self._list_stack[-1] = (kind, idx)
            marker = f"{idx}."
        else:
            marker = "-"

        body = self._render_children(node)
        body = "\n".join(line.rstrip() for line in body.split("\n"))
        body = re.sub(r"\n{3,}", "\n\n", body).strip("\n")
        if not body:
            return marker
        lines = body.split("\n")
        cont = " " * (len(marker) + 1)
        out: list[str] = []
        for i, ln in enumerate(lines):
            if i == 0:
                out.append(f"{marker} {ln}")
            else:
                out.append(f"{cont}{ln}" if ln else "")
        return "\n".join(out)

    # ----- preformatted -----

    def _h_pre(self, node) -> str:
        self._in_pre += 1
        try:
            lang = ""
            code_child = None
            for child in node:
                if isinstance(child.tag, str) and child.tag.lower() == "code":
                    code_child = child
                    break
            class_source = code_child if code_child is not None else node
            for cls in (class_source.get("class") or "").split():
                for prefix in ("language-", "lang-", "highlight-source-", "brush:"):
                    if cls.startswith(prefix):
                        lang = cls[len(prefix) :]
                        break
                if lang:
                    break
            content = self._text_content(node).strip("\n")
            # Choose a fence longer than any internal run of backticks.
            n = 3
            for run in re.findall(r"`+", content):
                n = max(n, len(run) + 1)
            fence = "`" * n
            return f"\n\n{fence}{lang}\n{content}\n{fence}\n\n"
        finally:
            self._in_pre -= 1

    # ----- tables -----

    def _h_table(self, node) -> str:
        thead_rows = self._rows_in(node, "thead")
        tbody_rows = self._rows_in(node, "tbody")
        tfoot_rows = self._rows_in(node, "tfoot")
        direct_rows: list[list[str]] = []
        for child in node:
            if isinstance(child.tag, str) and child.tag.lower() == "tr":
                direct_rows.append(self._row_cells(child))

        header_row: list[str] | None = None
        body_rows: list[list[str]] = []

        if thead_rows:
            header_row = thead_rows[0]
            body_rows = thead_rows[1:] + tbody_rows + direct_rows + tfoot_rows
        else:
            combined = tbody_rows + direct_rows
            first_tr = self._first_row_node(node)
            has_th_header = first_tr is not None and any(
                isinstance(c.tag, str) and c.tag.lower() == "th" for c in first_tr
            )
            if has_th_header and combined:
                header_row = combined[0]
                body_rows = combined[1:] + tfoot_rows
            elif combined:
                cols = max(len(r) for r in combined)
                header_row = [""] * cols
                body_rows = combined + tfoot_rows

        if not header_row:
            return ""

        cols = (
            max([len(header_row), *(len(r) for r in body_rows)]) if body_rows else len(header_row)
        )
        header_row = header_row + [""] * (cols - len(header_row))
        lines = ["| " + " | ".join(header_row) + " |"]
        lines.append("| " + " | ".join(["---"] * cols) + " |")
        for row in body_rows:
            row = row + [""] * (cols - len(row))
            lines.append("| " + " | ".join(row) + " |")
        return "\n\n" + "\n".join(lines) + "\n\n"

    def _rows_in(self, table_node, section_tag) -> list[list[str]]:
        rows: list[list[str]] = []
        for child in table_node:
            if isinstance(child.tag, str) and child.tag.lower() == section_tag:
                for tr in child:
                    if isinstance(tr.tag, str) and tr.tag.lower() == "tr":
                        rows.append(self._row_cells(tr))
        return rows

    @staticmethod
    def _first_row_node(table_node):
        for el in table_node.iter():
            if isinstance(el.tag, str) and el.tag.lower() == "tr":
                return el
        return None

    def _row_cells(self, tr) -> list[str]:
        cells: list[str] = []
        for child in tr:
            if isinstance(child.tag, str) and child.tag.lower() in ("th", "td"):
                cells.append(self._cell_text(child))
        return cells

    def _cell_text(self, cell) -> str:
        text = self._render_children(cell).strip()
        text = text.replace("\n", " ")
        text = _WS_RE.sub(" ", text)
        return text.replace("|", "\\|")

    # ----- definition lists -----

    def _h_dl(self, node) -> str:
        out: list[str] = []
        for child in node:
            if not isinstance(child.tag, str):
                continue
            tag = child.tag.lower()
            inner = self._render_children(child).strip()
            if not inner:
                continue
            if tag == "dt":
                out.append(f"**{inner}**")
            elif tag == "dd":
                out.append(f": {inner}")
        if not out:
            return ""
        return "\n\n" + "\n".join(out) + "\n\n"


class Tomd:
    def __init__(self, html: str = "") -> None:
        self.html = html
        self._markdown = ""

    def convert(self, html: str = "") -> str:
        self._markdown = _Converter().convert(html)
        return self._markdown

    @property
    def markdown(self) -> str:
        self.convert(self.html)
        return self._markdown


_inst = Tomd()
convert = _inst.convert
