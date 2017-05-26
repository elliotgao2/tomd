from tomd import Tomd

string = """
<div class="article fmt article__content" data-id="1190000009562674" data-license="cc">
                    
<h2 id="articleHeader0">写在前面</h2>
<p>JavaScript 深入系列共计 15 篇已经正式完结，这是一个旨在帮助大家，其实也是帮助自己捋顺 JavaScript 底层知识的系列。重点讲解了如原型、作用域、执行上下文、变量对象、this、闭包、按值传递、call、apply、bind、new、继承等 JS 语言中的比较难懂的概念。</p>
<p>JavaScript 深入系列自 4 月 6 日发布第一篇文章，到 5 月 12 日发布最后一篇，感谢各位朋友的收藏、点赞，鼓励、指正。</p>
<p>顺便宣传一下该博客的 Github 仓库：<a href="https://github.com/mqyqingfeng/Blog" target="_blank">https://github.com/mqyqingfeng/Blog</a>，欢迎 star，鼓励一下作者。</p>
<p>而此篇，作为深入系列的总结篇，除了汇总各篇文章，作为目录篇之外，还希望跟大家聊聊，我为什么要写这个系列？</p>
<h2 id="articleHeader1">我为什么要写深入系列？</h2>
<p>讲一个对我学技术的态度很有影响的一件事情。</p>
<p>曾经团队邀请过 Nodejs 领域一个非常著名的大神来分享，这里便不说是谁了。当知道是他后，简直是粉丝的心情。但是课讲得确实一般，也许是第一次讲，准备不是很充足吧，以至于我都觉得我能讲得比他好，但是有两次，让我觉得这是真正的大神。一次就是，当有同事问到今年有什么流行的前端框架吗？这些框架有怎样的适用场景？该如何抉择？我以为大神一定会回答当时正火的 React、以及小鲜肉 Vue 之类，然后老生常谈的比较一番，但是他回答道：“I dont't care！因为这些并不重要，真正重要的是底层，当你了解了底层，你就能很轻松的明白这些框架的原理，当你明白了原理，这些框架又有什么意思呢？”</p>
<p>虽然这段话因为过去太久，已经不记得确切的表述，但是给了我非常深刻的印象，自己一路学习过来，新的东西不停的冒出，但是学的再多感觉自己也只是学了一堆 API，如果仅仅是为了解决工作上的问题，或许已经足够，但是内心经常还会冒出一种不安定感，这种不安定感或许来自于对 JavaScript 未知部分的恐惧，或许来自于解决问题却不明所以的尴尬，或许来自于屡次学习语言难点却不得门道的失败……代码写的越久，这种感觉就越是鲜明。</p>
<p>当然了，大家也不要过分解读底层，各种计算机语言追究到底层都是编译原理之类，如果是有这方面的兴趣，固然可以，但是如果本质上还是为了解决上层问题，倒不必一定要深究到这个层面。用 JavaScript 了解这门语言本身的使用和原理，用 jQuery 看看 jQuery 的源码实现，用 React 技术栈，写写 React、Redux 简单的模拟实现，诸如此类，都是对底层的一种追求。</p>
<p>这样讲的话，底层这个词，更像是一个方向，一种学习的态度吧。</p>
<p>为了更加深入的了解 JavaScript 这门语言，我将之前记录的一些要学习的关键词作为课题进行研究，后来研究的差不多了，才决定动笔写下这个系列。尽管这个系列很多地方上依然不够所谓的“深入”，但就跟学习这些内容之前的我相比，已然多了份安定感，解决一些问题时也多了份得心应手，也希望大家能从这个系列中有所收获。</p>
<p>然而即便已经写了 15 篇，也只是漫长路途的开始，在我 Github 博客仓库的描述中有写到，我预计写 4 个系列，JavaScript 深入系列，JavaScript 专题系列，ES6 系列，React 系列，其实从“深入系列”到“专题系列”再到“ React 系列”，就是原来写着上层的我决定从语言层面开始一步一步走回上层的记录，而现在，我也只是迈出了第一步。</p>
<h2 id="articleHeader2">重新修订</h2>
<p>在发布完最后一篇后，我花了一周时间，根据大家的评论和留言，并且参照阮一峰老师的<a href="https://github.com/ruanyf/document-style-guide" target="_blank">《中文技术文档的写作规范》</a>对所有的文章进行了一次修订。</p>
<p>说起来，改的最多的就是给英文单词两边加个空格……</p>
<p>此外，大家有疑问或指正或鼓励或感谢，尽管留言回复哈 []~(￣▽￣)~* 。</p>
<h2 id="articleHeader3">全目录</h2>
<ol>
<li><p><a href="https://segmentfault.com/a/1190000008959943">JavaScirpt深入之从原型到原型链</a></p></li>
<li><p><a href="https://segmentfault.com/a/1190000008972987" target="_blank">JavaScript深入之词法作用域和动态作用域</a></p></li>
<li><p><a href="https://segmentfault.com/a/1190000009006005">JavaScript深入之执行上下文栈</a></p></li>
<li><p><a href="https://segmentfault.com/a/1190000009018898" target="_blank">JavaScript深入之变量对象</a></p></li>
<li><p><a href="https://segmentfault.com/a/1190000009035308">JavaScript深入之作用域链</a></p></li>
<li><p><a href="https://segmentfault.com/a/1190000009048715" target="_blank">JavaScript深入之从ECMAScript规范解读this</a></p></li>
<li><p><a href="https://segmentfault.com/a/1190000009063218">JavaScript深入之执行上下文</a></p></li>
<li><p><a href="https://segmentfault.com/a/1190000009215716" target="_blank">JavaScript深入之闭包</a></p></li>
<li><p><a href="https://segmentfault.com/a/1190000009229025">JavaScript深入之参数按值传递</a></p></li>
<li><p><a href="https://segmentfault.com/a/1190000009257663" target="_blank">JavaScript深入之call和apply的模拟实现</a></p></li>
<li><p><a href="https://segmentfault.com/a/1190000009271416">JavaScript深入之bind的模拟实现</a></p></li>
<li><p><a href="https://segmentfault.com/a/1190000009286643" target="_blank">JavaScript深入之new的模拟实现</a></p></li>
<li><p><a href="https://segmentfault.com/a/1190000009328344">JavaScript深入之类数组对象与arguments</a></p></li>
<li><p><a href="https://segmentfault.com/a/1190000009359984" target="_blank">JavaScript深入之创建对象的多种方式以及优缺点</a></p></li>
<li><p><a href="https://segmentfault.com/a/1190000009389979">JavaScript深入之继承的多种方式以及优缺点</a></p></li>
</ol>
<h2 id="articleHeader4">作者推荐</h2>
<p>在我研究一些课题的时候，有时感觉自己深受启发，颇有醍醐灌顶的感觉，我也希望这个系列的读者能感受到跟作者当初学习这些内容时的一样兴奋的感觉，所以强烈推荐以下三篇：</p>
<ol>
<li><p><a href="https://segmentfault.com/a/1190000009048715" target="_blank">JavaScript深入之从ECMAScript规范解读this</a></p></li>
<li><p><a href="https://segmentfault.com/a/1190000009257663">JavaScript深入之call和apply的模拟实现</a></p></li>
<li><p><a href="https://segmentfault.com/a/1190000009286643" target="_blank">JavaScript深入之new的模拟实现</a></p></li>
</ol>
<h2 id="articleHeader5">真的完结？</h2>
<p>JavaScript 底层知识哪有这么一点呐！在不断学习的过程中，还会冒出一些新的课题适合划分到深入系列，如果是这样的话，就会偶尔发布一篇，当然了，如果冒出太多的话，不保证再来一个深入系列第二季，哈哈。</p>
<h2 id="articleHeader6">下期预告</h2>
<p>一周之内，会发布新的系列即 JavaScript 专题系列，这个系列主要研究日常开发中一些功能点的实现，比如防抖、节流、去重、拷贝、最值、扁平、柯里、递归、乱序、排序等，特点是抄袭 underscore 和 jQuery 的实现方式，而这次预计写二十篇左右。</p>
<p>感谢大家的阅读和支持，我是冴羽，JavaScript 专题系列再见啦！[]~(￣▽￣)~**</p>

                </div>
"""

print(Tomd(string).markdown)
# print(Tomd('<h1>title</h1>').markdown)
