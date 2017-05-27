# tomd
Convert HTML to Markdown.

## Road map

- [x] Basic support
- [ ] Full support(Table, Nested list ,etc)
- [ ] Command line tool

## Installation

`pip install tomd`

## Getting Started

Input

```python
from tomd import Tomd

Tomd("<h1>h1</h1>").markdown
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
<th>表头1</th>
<th>表头2</th>
</tr>
</thead>
<tbody>
<tr>
<td>表格单元</td>
<td>表格单元</td>
</tr>
<tr>
<td>表格单元</td>
<td>表格单元</td>
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


|表头1|表头2
|------
|表格单元|表格单元
|表格单元|表格单元

```
