from tomd import Tomd, convert


def md(html: str) -> str:
    return Tomd(html).markdown.strip()


# ---------- basic / smoke ----------


def test_h1_through_h6():
    html = "<h1>h1</h1><h2>h2</h2><h3>h3</h3><h4>h4</h4><h5>h5</h5><h6>h6</h6>"
    out = md(html)
    assert "# h1" in out
    assert "## h2" in out
    assert "### h3" in out
    assert "#### h4" in out
    assert "##### h5" in out
    assert "###### h6" in out


def test_inline_emphasis():
    out = md("<p><b>bold</b> <i>italic</i> <del>strike</del> <code>code</code></p>")
    assert "**bold**" in out
    assert "*italic*" in out
    assert "~~strike~~" in out
    assert "`code`" in out


def test_link():
    out = md('<p><a href="https://example.com">click</a></p>')
    assert "[click](https://example.com)" in out


def test_link_without_http_scheme_is_left_alone():
    out = md('<p><a href="/local">click</a></p>')
    assert "click" in out


def test_image():
    out = md('<p><img src="https://example.com/a.png" alt="alt"/></p>')
    assert "![alt](https://example.com/a.png)" in out


def test_unordered_list():
    out = md("<ul><li>one</li><li>two</li></ul>")
    assert "- one" in out
    assert "- two" in out


def test_blockquote():
    out = md("<blockquote>quoted</blockquote>")
    assert "> quoted" in out


def test_horizontal_rule():
    out = md("<p>before</p><hr/><p>after</p>")
    assert "---" in out


def test_module_level_convert_callable():
    result = convert("<h1>title</h1>")
    assert "# title" in result


# ---------- empty / whitespace ----------


def test_empty_string_returns_empty():
    assert convert("") == ""
    assert convert("   ") == ""


def test_none_input_returns_empty():
    assert convert(None) == ""


def test_only_skipped_tags_returns_empty():
    assert convert("<script>alert(1)</script><style>p{color:red}</style>") == ""


def test_whitespace_collapsed_in_paragraph():
    out = md("<p>hello\n    world\n    again</p>")
    assert "hello world again" in out


def test_repeated_identical_paragraphs_each_present():
    # Original string-replace impl collapsed duplicates; this guards against regression.
    out = convert("<p>same</p><p>same</p>")
    assert out.count("same") == 2


# ---------- headings ----------


def test_heading_with_inline_formatting():
    out = md("<h2>Hello <strong>World</strong></h2>")
    assert "## Hello **World**" in out


def test_empty_heading_is_dropped():
    out = md("<h1></h1><p>after</p>")
    assert "#" not in out
    assert "after" in out


# ---------- emphasis / inline ----------


def test_nested_emphasis():
    out = md("<p>This is <strong>bold <em>and italic</em></strong></p>")
    assert "**bold *and italic***" in out


def test_strong_alias_for_b():
    assert "**x**" in md("<p><strong>x</strong></p>")
    assert "**x**" in md("<p><b>x</b></p>")


def test_em_alias_for_i():
    assert "*x*" in md("<p><em>x</em></p>")
    assert "*x*" in md("<p><i>x</i></p>")


def test_strikethrough_variants():
    assert "~~a~~" in md("<p><del>a</del></p>")
    assert "~~b~~" in md("<p><s>b</s></p>")
    assert "~~c~~" in md("<p><strike>c</strike></p>")


def test_kbd_renders_as_inline_code():
    out = md("<p>Press <kbd>Ctrl</kbd>+<kbd>C</kbd></p>")
    assert "`Ctrl`" in out
    assert "`C`" in out


# ---------- links ----------


def test_link_mailto():
    out = md('<a href="mailto:test@example.com">test</a>')
    assert "[test](mailto:test@example.com)" in out


def test_link_relative_path_preserved():
    out = md('<a href="/docs/intro">click</a>')
    assert "[click](/docs/intro)" in out


def test_link_fragment_preserved():
    out = md('<a href="#section-2">go</a>')
    assert "[go](#section-2)" in out


def test_link_with_title():
    out = md('<a href="https://example.com" title="Example">link</a>')
    assert '[link](https://example.com "Example")' in out


def test_link_with_no_text_uses_href():
    out = md('<a href="https://example.com"></a>')
    assert "https://example.com" in out


def test_link_with_url_containing_spaces_wrapped_in_brackets():
    out = md('<a href="https://example.com/path with space">x</a>')
    assert "<https://example.com/path with space>" in out


# ---------- images ----------


def test_image_with_title():
    out = md('<img src="https://example.com/a.png" alt="alt" title="Photo"/>')
    assert '![alt](https://example.com/a.png "Photo")' in out


def test_image_without_alt():
    out = md('<img src="https://example.com/a.png"/>')
    assert "![](https://example.com/a.png)" in out


def test_image_inside_link():
    out = md('<a href="https://example.com"><img src="/i.png" alt="logo"/></a>')
    assert "[![logo](/i.png)](https://example.com)" in out


# ---------- lists ----------


def test_ordered_list():
    out = md("<ol><li>first</li><li>second</li><li>third</li></ol>")
    assert "1. first" in out
    assert "2. second" in out
    assert "3. third" in out


def test_ordered_list_with_start_attr():
    out = md('<ol start="5"><li>five</li><li>six</li></ol>')
    assert "5. five" in out
    assert "6. six" in out


def test_nested_unordered_lists():
    html = "<ul><li>one<ul><li>nested</li><li>deeper</li></ul></li><li>two</li></ul>"
    out = md(html)
    assert "- one" in out
    assert "  - nested" in out
    assert "  - deeper" in out
    assert "- two" in out


def test_mixed_ordered_and_unordered_lists():
    html = "<ol><li>one<ul><li>a</li><li>b</li></ul></li><li>two</li></ol>"
    out = md(html)
    assert "1. one" in out
    assert "   - a" in out  # 3-space indent under "1. " marker
    assert "   - b" in out
    assert "2. two" in out


def test_list_item_containing_inline_formatting():
    out = md("<ul><li><strong>bold item</strong> with <em>style</em></li></ul>")
    assert "- **bold item** with *style*" in out


def test_three_levels_of_nesting():
    html = "<ul><li>a<ul><li>b<ul><li>c</li></ul></li></ul></li></ul>"
    out = md(html)
    assert "- a" in out
    assert "  - b" in out
    assert "    - c" in out


# ---------- code ----------


def test_code_block_plain():
    out = md("<pre><code>def foo():\n    return 42</code></pre>")
    assert "```" in out
    assert "def foo():" in out
    assert "    return 42" in out


def test_code_block_with_language_class():
    out = md('<pre><code class="language-python">x = 1</code></pre>')
    assert "```python" in out
    assert "x = 1" in out


def test_code_block_with_lang_class():
    out = md('<pre><code class="lang-go">package main</code></pre>')
    assert "```go" in out


def test_code_block_preserves_internal_whitespace():
    out = md("<pre>line1\n    indented\n        deeper</pre>")
    assert "line1\n    indented\n        deeper" in out


def test_inline_code_with_backtick_uses_longer_fence():
    out = md("<p>use <code>`x`</code> here</p>")
    assert "`` `x` ``" in out


def test_inline_code_collapses_whitespace():
    out = md("<p><code>foo   bar</code></p>")
    assert "`foo bar`" in out


def test_pre_without_inner_code_tag():
    out = md("<pre>raw\ntext</pre>")
    assert "```" in out
    assert "raw\ntext" in out


# ---------- tables ----------


def test_table_with_thead_tbody():
    html = """
    <table>
      <thead><tr><th>Name</th><th>Age</th></tr></thead>
      <tbody>
        <tr><td>Alice</td><td>30</td></tr>
        <tr><td>Bob</td><td>25</td></tr>
      </tbody>
    </table>
    """
    out = md(html)
    assert "| Name | Age |" in out
    assert "| --- | --- |" in out
    assert "| Alice | 30 |" in out
    assert "| Bob | 25 |" in out


def test_table_without_thead_first_row_th():
    html = "<table><tr><th>X</th><th>Y</th></tr><tr><td>a</td><td>b</td></tr></table>"
    out = md(html)
    assert "| X | Y |" in out
    assert "| --- | --- |" in out
    assert "| a | b |" in out


def test_table_all_td_synthesizes_empty_header():
    html = "<table><tr><td>1</td><td>2</td></tr><tr><td>3</td><td>4</td></tr></table>"
    out = md(html)
    assert "| --- | --- |" in out
    assert "| 1 | 2 |" in out
    assert "| 3 | 4 |" in out


def test_table_with_pipe_in_cell_escaped():
    html = "<table><tr><th>H</th></tr><tr><td>a|b</td></tr></table>"
    out = md(html)
    assert "a\\|b" in out


def test_table_with_inline_formatting_in_cells():
    html = (
        "<table><thead><tr><th>Col</th></tr></thead>"
        "<tbody><tr><td><strong>bold</strong></td></tr></tbody></table>"
    )
    out = md(html)
    assert "**bold**" in out


# ---------- blockquotes ----------


def test_blockquote_with_paragraphs():
    out = md("<blockquote><p>first</p><p>second</p></blockquote>")
    assert "> first" in out
    assert "> second" in out


def test_blockquote_nested():
    out = md("<blockquote><blockquote>deep</blockquote></blockquote>")
    # Either single or double prefix is acceptable, but content must be quoted.
    assert "> > deep" in out or "> deep" in out


def test_blockquote_with_list():
    out = md("<blockquote><ul><li>a</li><li>b</li></ul></blockquote>")
    assert "> - a" in out
    assert "> - b" in out


# ---------- breaks / paragraphs ----------


def test_br_creates_markdown_hard_break():
    out = md("<p>line one<br/>line two</p>")
    assert "line one  \nline two" in out


def test_multiple_paragraphs_separated_by_blank_line():
    out = md("<p>one</p><p>two</p><p>three</p>")
    assert "one\n\ntwo" in out
    assert "two\n\nthree" in out


def test_div_and_section_as_block_separators():
    out = md("<div>one</div><div>two</div>")
    assert "one" in out
    assert "two" in out


# ---------- entities / unicode ----------


def test_html_entities_decoded():
    out = md("<p>foo &amp; bar &lt;tag&gt; &quot;q&quot;</p>")
    assert "foo & bar <tag>" in out
    assert '"q"' in out


def test_numeric_entities_decoded():
    out = md("<p>&#8212; &#x2014;</p>")
    assert "—" in out


def test_unicode_preserved():
    out = md("<p>café — naïve résumé 中文 🎉</p>")
    assert "café — naïve résumé 中文 🎉" in out


# ---------- definition lists ----------


def test_definition_list():
    out = md("<dl><dt>Term</dt><dd>Definition</dd></dl>")
    assert "**Term**" in out
    assert ": Definition" in out


# ---------- skip / unknown / safety ----------


def test_script_and_style_skipped():
    out = md("<p>hello</p><script>alert(1)</script><style>p{color:red}</style>")
    assert "alert" not in out
    assert "color:red" not in out
    assert "hello" in out


def test_iframe_skipped():
    out = md('<p>before</p><iframe src="x"></iframe><p>after</p>')
    assert "before" in out
    assert "after" in out
    assert "iframe" not in out


def test_unknown_tag_passes_through_content():
    out = md("<custom-tag>hello</custom-tag>")
    assert "hello" in out


def test_malformed_html_doesnt_crash():
    # Garbled tags shouldn't raise.
    out = convert("<p>foo</bad><div>bar")
    assert "foo" in out
    assert "bar" in out


# ---------- real-world snippets ----------


def test_real_world_blog_post():
    html = """<article>
<h1>How to Use Python</h1>
<p>Python is a <strong>powerful</strong> language. Visit <a href="https://python.org">python.org</a>.</p>
<h2>Getting Started</h2>
<p>Install Python via:</p>
<pre><code class="language-bash">brew install python</code></pre>
<p>Then check:</p>
<ol>
  <li>Open terminal</li>
  <li>Run <code>python --version</code></li>
  <li>Verify output</li>
</ol>
<blockquote>
<p>Programming is fun &mdash; <em>Anonymous</em></p>
</blockquote>
</article>"""
    out = md(html)
    assert "# How to Use Python" in out
    assert "**powerful**" in out
    assert "[python.org](https://python.org)" in out
    assert "## Getting Started" in out
    assert "```bash" in out
    assert "brew install python" in out
    assert "1. Open terminal" in out
    assert "2. Run `python --version`" in out
    assert "3. Verify output" in out
    assert "> Programming is fun" in out
    assert "*Anonymous*" in out


def test_real_world_documentation_with_table():
    html = """
    <div class="docs">
      <h2>API Reference</h2>
      <p>The <code>foo()</code> function returns a <strong>bar</strong>.</p>
      <h3>Parameters</h3>
      <table>
        <thead><tr><th>Name</th><th>Type</th><th>Description</th></tr></thead>
        <tbody>
          <tr><td>x</td><td>int</td><td>The first arg</td></tr>
          <tr><td>y</td><td>str</td><td>The second arg</td></tr>
        </tbody>
      </table>
    </div>
    """
    out = md(html)
    assert "## API Reference" in out
    assert "`foo()`" in out
    assert "**bar**" in out
    assert "### Parameters" in out
    assert "| Name | Type | Description |" in out
    assert "| x | int | The first arg |" in out
    assert "| y | str | The second arg |" in out


def test_real_world_github_readme_snippet():
    html = """
    <div align="center">
      <h1>my-project</h1>
      <p>A <em>tiny</em> tool for parsing things.</p>
    </div>
    <h2>Install</h2>
    <pre><code class="language-bash">pip install my-project</code></pre>
    <h2>Usage</h2>
    <pre><code class="language-python">import my_project
my_project.do_thing()</code></pre>
    """
    out = md(html)
    assert "# my-project" in out
    assert "*tiny*" in out
    assert "## Install" in out
    assert "```bash" in out
    assert "pip install my-project" in out
    assert "```python" in out
    assert "import my_project\nmy_project.do_thing()" in out


def test_real_world_wikipedia_excerpt():
    html = """
    <p><b>Python</b> is a high-level programming language. It was created by
    <a href="https://en.wikipedia.org/wiki/Guido_van_Rossum">Guido van Rossum</a>
    and first released in <a href="/wiki/1991">1991</a>.</p>
    <h2>Features</h2>
    <ul>
      <li>Dynamic typing</li>
      <li>Automatic memory management</li>
      <li>A <i>large</i> standard library</li>
    </ul>
    """
    out = md(html)
    assert "**Python**" in out
    assert "[Guido van Rossum](https://en.wikipedia.org/wiki/Guido_van_Rossum)" in out
    assert "[1991](/wiki/1991)" in out
    assert "## Features" in out
    assert "- Dynamic typing" in out
    assert "- Automatic memory management" in out
    assert "- A *large* standard library" in out


def test_real_world_stackoverflow_answer():
    html = """
    <p>You can do this with <code>list comprehensions</code>:</p>
    <pre><code class="language-python">squares = [x*x for x in range(10)]
print(squares)</code></pre>
    <p>This produces:</p>
    <pre><code>[0, 1, 4, 9, 16, 25, 36, 49, 64, 81]</code></pre>
    <p>See the <a href="https://docs.python.org/3/tutorial/datastructures.html#list-comprehensions">docs</a> for more.</p>
    """
    out = md(html)
    assert "`list comprehensions`" in out
    assert "```python" in out
    assert "squares = [x*x for x in range(10)]" in out
    assert "print(squares)" in out
    assert "[0, 1, 4, 9, 16, 25, 36, 49, 64, 81]" in out
    assert "[docs](https://docs.python.org/3/tutorial/datastructures.html#list-comprehensions)" in out


def test_real_world_news_article():
    html = """
    <article>
      <header>
        <h1>Headline Goes Here</h1>
        <p><em>By Reporter Name &middot; January 1, 2026</em></p>
      </header>
      <p>This is the lead paragraph with some <strong>important</strong> news.</p>
      <p>A second paragraph follows. It contains a <a href="https://example.com">source link</a>.</p>
      <figure>
        <img src="/image.jpg" alt="A photo"/>
        <figcaption>A photo of something.</figcaption>
      </figure>
      <p>Final paragraph.</p>
    </article>
    """
    out = md(html)
    assert "# Headline Goes Here" in out
    assert "*By Reporter Name" in out
    assert "**important**" in out
    assert "[source link](https://example.com)" in out
    assert "![A photo](/image.jpg)" in out
    assert "A photo of something." in out
    assert "Final paragraph." in out


def test_html_doc_with_head_and_body():
    """Full HTML doc, head must be dropped."""
    html = """
    <html>
      <head><title>Page</title><meta charset="utf-8"/></head>
      <body>
        <h1>Content</h1>
        <p>Body text.</p>
      </body>
    </html>
    """
    out = md(html)
    assert "Page" not in out
    assert "# Content" in out
    assert "Body text." in out


# ---------- regressions ----------


def test_tomd_instance_markdown_property():
    t = Tomd("<h1>x</h1>")
    assert "# x" in t.markdown


def test_tomd_convert_method_reusable():
    t = Tomd()
    assert "# a" in t.convert("<h1>a</h1>")
    assert "# b" in t.convert("<h1>b</h1>")


def test_output_ends_with_single_newline():
    out = convert("<h1>x</h1>")
    assert out.endswith("\n")
    assert not out.endswith("\n\n")
