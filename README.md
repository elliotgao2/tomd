# tomd
Convert HTML to Markdown.

```
from tomd import Tomd

Tomd('<h1>title</h1>').markdown
Tomd('<h1>title</h1>','h1').markdown
Tomd('https://github.com').markdown
Tomd('https://github.com','.title .content').markdown
```
