from tomd import Tomd

string = """
<div class="markdown_body"><p>XData</p>
<p>Github: <a href="https://github.com/gaojiuli/xdata" rel="nofollow">https://github.com/gaojiuli/xdata</a></p>
<p>一款非常实用的数据验证工具, 通常用于请求数据的验证.</p>
<h2>Features</h2>
<ul>
<li>验证数据一步到位</li>
<li>容易扩展,容易自定义数据类型以及验证方式</li>
<li>无第三方依赖</li>
</ul>
<h2>Required</h2>
<ul>
<li>python &gt;= 3.5</li>
</ul>
<h2>Installation</h2>
<p><code>pip install xdata</code></p>
<h2>Usage</h2>
<h3>ValidatedData</h3>
<pre><code class="hljs python"><span class="hljs-keyword">from</span> xdata <span class="hljs-keyword">import</span> *

<span class="hljs-class"><span class="hljs-keyword">class</span> <span class="hljs-title">UserSchema</span><span class="hljs-params">(Schema)</span>:</span>
    telephone = Str(length=<span class="hljs-number">11</span>, required=<span class="hljs-keyword">True</span>)
    password = Str(min_length=<span class="hljs-number">8</span>,max_length=<span class="hljs-number">16</span>, required=<span class="hljs-keyword">True</span>)
    
request_data = {
    <span class="hljs-string">'telephone'</span>:<span class="hljs-string">'18180050000'</span>,
    <span class="hljs-string">'password'</span>:<span class="hljs-string">'idonotknow'</span>
}

schema = UserSchema(request_data)
<span class="hljs-keyword">if</span> schema.valid:
    print(schema.validated_data) <span class="hljs-comment"># {'telephone': '18180050000', 'password': 'idonotknow'}</span>

</code></pre>
<h3>Errors</h3>
<pre><code class="hljs python"><span class="hljs-keyword">from</span> xdata <span class="hljs-keyword">import</span> *

<span class="hljs-class"><span class="hljs-keyword">class</span> <span class="hljs-title">UserSchema</span><span class="hljs-params">(Schema)</span>:</span>
    telephone = Str(length=<span class="hljs-number">11</span>, required=<span class="hljs-keyword">True</span>)
    password = Str(min_length=<span class="hljs-number">8</span>, max_length=<span class="hljs-number">16</span>, required=<span class="hljs-keyword">True</span>)


request_data = {}

schema = UserSchema(request_data)
<span class="hljs-keyword">if</span> <span class="hljs-keyword">not</span> schema.valid:
    print(schema.errors)  <span class="hljs-comment"># {'telephone': 'telephone is required', 'password': 'password is required'}</span>
</code></pre>
<h3>DataTypes</h3>
<pre><code class="hljs lisp">from xdata import *

DataType(<span class="hljs-name">required=True</span>,default='<span class="hljs-number">11</span>',choices=[])

Str(<span class="hljs-name">length=11</span>, max_length=12,min_length=10,regex=<span class="hljs-string">""</span>)
Int(<span class="hljs-name">max=10000</span>,min=12)
Bool(<span class="hljs-name">max=10000</span>,min=12)
Decimal(<span class="hljs-name">left=5</span>,right=2)
DateTime(<span class="hljs-name">max_datetime=</span>'<span class="hljs-number">2001</span><span class="hljs-number">-01</span><span class="hljs-number">-01</span> <span class="hljs-number">00</span>:<span class="hljs-number">00</span>:<span class="hljs-number">00</span>', min_datetime='<span class="hljs-number">2000</span><span class="hljs-number">-01</span><span class="hljs-number">-01</span> <span class="hljs-number">00</span>:<span class="hljs-number">00</span>:<span class="hljs-number">00</span>')
Date(<span class="hljs-name">max_date=</span>'<span class="hljs-number">2001</span><span class="hljs-number">-01</span><span class="hljs-number">-01</span>', min_date='<span class="hljs-number">2000</span><span class="hljs-number">-01</span><span class="hljs-number">-01</span>')
Time(<span class="hljs-name">max_time=</span>'<span class="hljs-number">06</span>:<span class="hljs-number">00</span>:<span class="hljs-number">00</span>', min_time='<span class="hljs-number">05</span>:<span class="hljs-number">00</span>:<span class="hljs-number">00</span>')

</code></pre>
<h2>Test</h2>
<p><code>coverage run --source=xdata -m pytest &amp;&amp; coverage report</code></p>
<p>Github: <a href="https://github.com/gaojiuli/xdata" rel="nofollow">https://github.com/gaojiuli/xdata</a></p>
<p>欢迎有兴趣的朋友一起参与进来</p>
</div>
"""
# Tomd(string)
Tomd(string)
