# tomd

![[License](https://pypi.python.org/pypi/tomd/)](https://img.shields.io/pypi/l/tomd.svg)
![[Pypi](https://pypi.python.org/pypi/tomd/)](https://img.shields.io/pypi/v/tomd.svg)
![[Python](https://pypi.python.org/pypi/tomd/)](https://img.shields.io/pypi/pyversions/tomd.svg)

When crawling online articles such as news, blogs, etc. I want to save them in markdown files but not databases.
Tomd has the ability of converting a HTML that converted from markdown. If a HTML can't be described by markdown, tomd can't convert it right.
Tomd is a python tool.


## Road map

- [x] Basic support
- [ ] Full support(Nested list)
- [ ] Command line tool

## Installation

`pip install tomd`

## Getting Started

Input

```python
import tomd

tomd.Tomd('<h1>h1</h1>').markdown
# or
tomd.convert('<h1>h1</h1>')
```

Output

```markdown
# h1
```

## Usage

```python
from tomd import Tomd


html="""
<h1>h1</h1>
<h2>h2</h2>
<h3>h3</h3>
<h4>h4</h4>
<h5>h5</h5>
<h6>h6</h6>
<p>paragraph
<a href="https://github.com">link</a>
<img src="https://github.com" class="dsad">img</img>
</p>
<ul>
<li>1</li>
<li>2</li>
<li>3</li>
</ul>
<ol>
<li>1</li>
<li>2</li>
<li>3</li>
</ol>
<blockquote>blockquote</blockquote>
<p><code>inline code</code></p>
<pre><code>block code</code></pre>
<p>
<del>del</del>
<b>bold</b>
<i>italic</i>
<b><i>bold italic</i></b>
</p>

<hr/>

<table>
<thead>
<tr>
<th>th1</th>
<th>th2</th>
</tr>
</thead>
<tbody>
<tr>
<td>td</td>
<td>td</td>
</tr>
<tr>
<td>td</td>
<td>td</td>
</tr></tbody></table>
"""


Tomd(html).markdown
```

## Result

```markdown
# h1

## h2

### h3

#### h4

##### h5

###### h6

paragraph
[link](https://github.com)
![img](https://github.com)


- 1
- 2
- 3

1. 1
1. 2
1. 3

> blockquote

`inline code`


block code


~~del~~
**bold**
*italic*
***bold italic***


---


|th1|th2
|------
|td|td
|td|td

```
