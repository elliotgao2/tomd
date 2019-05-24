from pyquery import PyQuery as pq

__all__ = ['Tomd', 'convert']

MARKDOWN = {
    'h1': "#",
    'h2': "##",
    'h3': "###",
    'h4': "####",
    'h5': "#####",
    'h6': "######",
    "blockquote": ">",
    "li": "-",
    "hr": "---",
    "p": "\n"
}

INLINE = {
    'em': ('*', '*'),
    'strong': ('**', '**'),
    'b': ('**', '**'),
    'i': ('*', '*'),
    'del': ('~~', '~~'),
    "code": ('`', '`')
}

split_str = "++++++++++++++++++"


class Tomd:
    def __init__(self, html=''):
        self.html = html
        self._markdown = ""

    def convert(self, html=""):

        d = pq(html)
        d('head').remove()
        html = d.html()

        d = pq(html)
        for e in d('span'):
            inline_mark = pq(e).text()
            html = html.replace(str(pq(e)), inline_mark)

        d = pq(html)
        for e in d('a'):
            if "http" in pq(e).attr('href'):
                inline_mark = f"[{pq(e).text()}]({pq(e).attr('href')})"
                html = html.replace(str(pq(e)), inline_mark)

        d = pq(html)
        for e in d('img'):
            inline_mark = f"![{pq(e).attr('alt')}]({pq(e).attr('src')})"
            html = html.replace(str(pq(e)), inline_mark)

        d = pq(html)
        for e in d('thead'):
            inline_mark = pq(e).outer_html() + '|------' * (pq(e)('th').length - 1)
            html = html.replace(str(pq(e)), inline_mark)

        d = pq(html)
        for e in d('th,td'):
            inline_mark = "|" + pq(e).text()
            html = html.replace(str(pq(e)), inline_mark)

        d = pq(html)
        for e in d('pre'):
            inline_mark = "```" + split_str + pq(e).html() + split_str + "```" + split_str
            html = html.replace(str(pq(e)), inline_mark)

        d = pq(html)
        selectors = ','.join(INLINE.keys())
        for e in d(selectors):
            inline_mark = INLINE.get(e.tag)[0] + pq(e).text() + INLINE.get(e.tag)[1]
            html = html.replace(str(pq(e)), inline_mark)

        d = pq(html)
        selectors = ','.join(MARKDOWN.keys())
        for e in d(selectors):
            inline_mark = split_str + MARKDOWN.get(e.tag) + " " + pq(e).text() + split_str
            html = html.replace(str(pq(e)), inline_mark)

        self._markdown = pq(html).text().replace(split_str, '\n')

        print(self._markdown)
        return self._markdown

    @property
    def markdown(self):
        self.convert(self.html)
        return self._markdown


_inst = Tomd()
convert = _inst.convert
