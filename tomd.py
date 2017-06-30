import re

__all__ = ['Tomd', 'convert']

MARKDOWN = {
    'h1': ('\n# ', '\n'),
    'h2': ('\n## ', '\n'),
    'h3': ('\n### ', '\n'),
    'h4': ('\n#### ', '\n'),
    'h5': ('\n##### ', '\n'),
    'h6': ('\n###### ', '\n'),
    'code': ('`', '`'),
    'ul': ('', ''),
    'ol': ('', ''),
    'li': ('- ', ''),
    'blockquote': ('\n> ', '\n'),
    'em': ('**', '**'),
    'strong': ('**', '**'),
    'block_code': ('\n```\n', '\n```\n'),
    'span': ('', ''),
    'p': ('\n', '\n'),
    'p_with_out_class': ('\n', '\n'),
    'inline_p': ('', ''),
    'inline_p_with_out_class': ('', ''),
    'b': ('**', '**'),
    'i': ('*', '*'),
    'del': ('~~', '~~'),
    'hr': ('\n---', '\n\n'),
    'thead': ('\n', '|------\n'),
    'tbody': ('\n', '\n'),
    'td': ('|', ''),
    'th': ('|', ''),
    'tr': ('', '\n'),
    'table': ('', '\n')
}

BlOCK_ELEMENTS = {
    'h1': '<h1.*?>(.*?)</h1>',
    'h2': '<h2.*?>(.*?)</h2>',
    'h3': '<h3.*?>(.*?)</h3>',
    'h4': '<h4.*?>(.*?)</h4>',
    'h5': '<h5.*?>(.*?)</h5>',
    'h6': '<h6.*?>(.*?)</h6>',
    'hr': '<hr/>',
    'blockquote': '<blockquote.*?>(.*?)</blockquote>',
    'ul': '<ul.*?>(.*?)</ul>',
    'ol': '<ol.*?>(.*?)</ol>',
    'block_code': '<pre.*?><code.*?>(.*?)</code></pre>',
    'p': '<p\s.*?>(.*?)</p>',
    'p_with_out_class': '<p>(.*?)</p>',
    'thead': '<thead.*?>(.*?)</thead>',
    # 'tr': '<tr>(.*?)</tr>',
    'table': '<table.*?>(.*?)</table>' #assume that table must be around tr
}

INLINE_ELEMENTS = {
    'td': '<td.*?>((.|\n)*?)</td>', #td element may span lines
    'tr': '<tr>((.|\n)*?)</tr>',
    'th': '<th>(.*?)</th>',
    'b': '<b>(.*?)</b>',
    'i': '<i>(.*?)</i>',
    'del': '<del>(.*?)</del>',
    'inline_p': '<p\s.*?>(.*?)</p>',
    'inline_p_with_out_class': '<p>(.*?)</p>',
    'code': '<code.*?>(.*?)</code>',
    'span': '<span.*?>(.*?)</span>',
    'ul': '<ul.*?>(.*?)</ul>',
    'ol': '<ol.*?>(.*?)</ol>',
    'li': '<li.*?>(.*?)</li>',
    'img': '<img.*?src="(.*?)".*?>(.*?)</img>',
    'a': '<a.*?href="(.*?)".*?>(.*?)</a>',
    'em': '<em.*?>(.*?)</em>',
    'strong': '<strong.*?>(.*?)</strong>',
    'tbody': '<tbody.*?>((.|\n)*)</tbody>'
}

DELETE_ELEMENTS = ['<span.*?>', '</span>', '<div.*?>', '</div>']


class Element:
    def __init__(self, start_pos, end_pos, content, tag, is_block=False):
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.content = content
        self._elements = []
        self.is_block = is_block
        self.tag = tag
        self._result = None

        if self.is_block:
            # print "parsing tag:", self.tag, ", content: ", self.content
            self.parse_inline()

    def __str__(self):
        wrapper = MARKDOWN.get(self.tag)
        self._result = '{}{}{}'.format(wrapper[0], self.content, wrapper[1])
        return self._result

    def parse_inline(self):
        self.content = self.content.replace('\r', '') #windows \r character
        if self.tag == "table": #for removing tbody
            self.content = re.sub(INLINE_ELEMENTS['tbody'], '\g<1>', self.content)

        for tag, pattern in INLINE_ELEMENTS.items():
            # print "---now looking at", tag, pattern

            if tag == 'a':
                self.content = re.sub(pattern, '[\g<2>](\g<1>)', self.content)
            elif tag == 'img':
                self.content = re.sub(pattern, '![\g<2>](\g<1>)', self.content)
            elif self.tag == 'ul' and tag == 'li':
                self.content = re.sub(pattern, '- \g<1>', self.content)
            elif self.tag == 'ol' and tag == 'li':
                self.content = re.sub(pattern, '1. \g<1>', self.content)
            elif self.tag == 'thead' and tag == 'tr':
                self.content = re.sub(pattern, '\g<1>\n', self.content.replace('\n', ''))
            elif self.tag == 'tr' and tag == 'th':
                self.content = re.sub(pattern, '|\g<1>', self.content.replace('\n', ''))
            elif self.tag == 'tr' and tag == 'td':
                self.content = re.sub(pattern, '|\g<1>|', self.content.replace('\n', ''))
                self.content = self.content.replace("||","|") #end of column also needs a pipe
                # print "---converting, td remove duplicate:", tag, self.content
            elif self.tag == 'table' and tag == 'td':
                self.content = re.sub(pattern, '|\g<1>|', self.content)
                self.content = self.content.replace("||","|") #end of column also needs a pipe
                self.content = self.content.replace('|\n\n', '|\n') #replace double new line
                # print "---converting, td remove duplicate:", tag, self.content
                self.construct_table()
            else:
                wrapper = MARKDOWN.get(tag)
                self.content = re.sub(pattern, '{}\g<1>{}'.format(wrapper[0], wrapper[1]), self.content)
    def construct_table(self):
        # this function, after self.content has gained | for table entries,
        # adds the |---| in markdown to create a proper table

        temp = self.content.split('\n',3)
        for elt in temp:
            if elt != "":
                count = elt.count("|") #count number of pipes
                break
        pipe = "|"
        for i in xrange(count-1):
            pipe += "---|"
        pipe += "\n"
        self.content = pipe + pipe + self.content #TODO: column titles?
        self.content = self.content.replace('|\n\n', '|\n') #replace double new line
        self.content = self.content.replace("<br/>\n","<br/>") #end of column also needs a pipe


class Tomd:
    def __init__(self, html='', options=None):
        self.html = html #actual data
        self.options = options # haven't been implemented yet
        self._markdown = ''

    def convert(self, html, options=None):
        #main function here
        elements = []
        for tag, pattern in BlOCK_ELEMENTS.items():
            # print "pattern is", pattern, "tag", tag
            for m in re.finditer(pattern, html, re.I | re.S | re.M):
                # now m contains the pattern without the tag
                # print "found", tag, m.groups(), "start", m.start(), "end", m.end()
                element = Element(start_pos=m.start(),
                                  end_pos=m.end(),
                                  content=''.join(m.groups()),
                                  tag=tag,
                                  is_block=True)
                can_append = True
                for e in elements:
                    if e.start_pos < m.start() and e.end_pos > m.end():
                        can_append = False
                    elif e.start_pos > m.start() and e.end_pos < m.end():
                        elements.remove(e)
                if can_append:
                    elements.append(element)
        # print "\n\n\ndone with convert, element is"
        # for e in elements:
        #     print repr(str(e))
        # print "---"
        elements.sort(key=lambda element: element.start_pos)
        self._markdown = ''.join([str(e) for e in elements])

        for index, element in enumerate(DELETE_ELEMENTS):
            self._markdown = re.sub(element, '', self._markdown)
        return self._markdown

    @property
    def markdown(self):
        self.convert(self.html, self.options)
        return self._markdown


_inst = Tomd()
convert = _inst.convert
