from tomd import Tomd, convert


def md(html: str) -> str:
    return Tomd(html).markdown.strip()


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
