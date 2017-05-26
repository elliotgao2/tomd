import re

MARKDOWN = {
    'h1': ('\n# ', '\n'),
    'h2': ('\n## ', '\n'),
    'h3': ('\n### ', '\n'),
    'h4': ('\n#### ', '\n'),
    'h5': ('\n##### ', '\n'),
    'h6': ('\n###### ', '\n'),
    'p': ('\n', '\n'),
    'p_with_out_class': ('\n', '\n'),
    'code': ('`', '`'),
    'ul': ('\n', '\n'),
    'ol': ('\n', '\n'),
    'li': ('*. ', ''),
    'blockquote': ('> ', '\n'),
    'em': ('**', '**'),
    'a': ('[](', ')'),
    'img': ('![](', ')'),
    'block_code': ('\n```\n', '\n```\n'),
    'span': ('', '')
}

BlOCK_ELEMENTS = {
    'h1': '<h1.*?>(.*?)</h1>',
    'h2': '<h2.*?>(.*?)</h2>',
    'h3': '<h3.*?>(.*?)</h3>',
    'h4': '<h4.*?>(.*?)</h4>',
    'h5': '<h5.*?>(.*?)</h5>',
    'h6': '<h6.*?>(.*?)</h6>',
    'p': '<p\s.*?>(.*?)</p>',
    'p_with_out_class': '<p>(.*?)</p>',
    'blockquote': '<blockquote.*?>(.*?)</blockquote>',
    'ul': '<ul.*?>(.*?)</ul>',
    'block_code': '<pre.*?><code.*?>(.*?)</code></pre>',
}

INLINE_ELEMENTS = {
    'code': '<code.*?>(.*?)</code>',
    'span': '<span.*?>(.*?)</span>',
    'ol': '<ol.*?>(.*?)</ol>',
    'li': '<li.*?>(.*?)</li>',
    'img': '<img.*?>(.*?)</img>',
    'a': '<a.*?>(.*?)</a>',
    'em': '<em.*?>(.*?)</em>',
    # 'pre': '<pre.*><code.*>(.*)</code></pre>',
}


class Element:
    def __init__(self, pos, content, tag):
        self.pos = pos
        self.content = content
        self._elements = []
        self.tag = tag
        self._result = None

        if tag in BlOCK_ELEMENTS:
            self.parse_inline()

    def __str__(self):
        wrapper = MARKDOWN.get(self.tag)
        self._result = '{}{}{}'.format(wrapper[0], self.content, wrapper[1])
        return self._result

    def parse_inline(self):
        for tag, pattern in INLINE_ELEMENTS.items():
            wrapper = MARKDOWN.get(tag)
            self.content = re.sub(pattern, '{}\g<1>{}'.format(wrapper[0], wrapper[1]), self.content)


class Tomd:
    def __init__(self, html):
        self.html = html
        self._elements = []
        self._markdown = None
        self.parse_block()
        print(self._markdown)
        for element in self._elements:
            if len(element._result) > 1000:
                print(element.__dict__)

    def parse_block(self):
        for tag, pattern in BlOCK_ELEMENTS.items():
            for m in re.finditer(pattern, self.html, re.I | re.S | re.M):
                element = Element(pos=m.start(), content=''.join(m.groups()), tag=tag)
                self._elements.append(element)
        self._elements.sort(key=lambda element: element.pos)
        self._markdown = ''.join([str(e) for e in self._elements])

    @property
    def markdown(self):
        return self._markdown
