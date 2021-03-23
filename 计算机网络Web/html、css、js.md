# HTML、CSS、JS

前端三兄弟，<code>html、css和js</code>，我们可以用人来帮助我们理解，**html帮我们构建静态页面**（它相当于人的骨架），但光是骨架特别难看，所以我们需要**css来美化页面**（相当于人的皮），但这样的做出来的页面是静态的，所以我们需要**js来实现动态和交互**（相当于人的灵魂，使人变得有灵性）。

# html

**HTML** 不是一门编程语言，而是一种用来告知浏览器如何组织页面的**标记语言**。它由一系列的**元素（elements）组成**，这些元素可以用来包围不同部分的内容，使其以某种方式呈现或者工作。 一对标签（ tags）可以为一段文字或者一张图片添加超链接，将文字设置为斜体，改变字号，等等。

## 元素(Element)

```java
<p>我爱我的祖国</p>
```

![在这里插入图片描述](https://img-blog.csdnimg.cn/20210323094919516.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQ1NjYxMTI1,size_16,color_FFFFFF,t_70)

 - **开始标签**：包含元素的名称（本例为 p），被左、右角括号所包围。表示元素从这里开始或者开始起作用。
 - 与开始标签相似，只是其在元素名之前包含了一个斜杠。这表示着元素的结尾。 元素的内容，本例中就是所输入的文本本身。
 - **开始标签、结束标签与内容相结合，便是一个完整的元素。**

**HTML**    中事先规定了一些元素，每种元素都有其语义(semantic)，这里的 p 是段落(paragraph)的语义。

### 嵌套元素(Nesting Element)

可以把元素放到其它元素之中——这被称作嵌套。

```java
<p>我爱我的<strong>祖国</strong></p>
```


> 				这里使用<strong></strong>标签，来强调 祖国 这一内容。

### 块级(block)元素和内联(inline)元素

```java
<p>第一段</p>
<p>第二段</p>
<p>第三段</p>
<p>第四段</p>
```

```java
<strong>第一句话</strong>
<strong>第二句话</strong>
<strong>第三句话</strong>
<strong>第四句话</strong>
```

 - 块级元素在页面中默认以块的形式展现。更多的是表示一类段落的语义。
 - 内联元素不会导致文本换行。更多的表示一个词、一句话等语义。

### 空元素(Empty Element)

**不是所有元素都拥有开始标签，内容，结束标签。**一些元素只有一个标签，通常用来在此元素所在位置  **插入/嵌入**一些东西。例如：元素<img> 是用来在元素<img> 所在位置插入一张指定的图片。

```java
<img src="图片地址源">
```

### 常见的元素介绍

 - **标题**： `<h1> 到<h6>从大到小`
 - **段落**： `<p>`
 - **列表:**

```java
无序列表： <ul> </ul>
```

```java
有序列表(): <ol></ol>
```

```java
列表项目():<ls><ls>
```

 - **超链接**： `<a>`

```java
<p><a  targey="_blank" href="http://www.baidu.com/"></a></p>
```

 - **图片：**

 

```java
<img src=“图片”>
```

 - **块级无语义元素：**

```java
 <div></div>
```

无语义元素，通常是用来组织内容，**方便之后通过 css 或者 js 对其进行布局或操作。**

 - **内联无语义元素**

```java
 <span>
```

## 属性(Attributes)

元素可以拥有属性
![在这里插入图片描述](https://img-blog.csdnimg.cn/20210323095927121.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQ1NjYxMTI1,size_16,color_FFFFFF,t_70)
属性包含元素的额外信息，这些信息不会出现在实际的内容中,但确有其他特殊的意义。在上述例子中，我们指定了 id 这个属性，它的值是 pid，还指定了 class 这个属性，它的值是 c1 和 c2。
一个属性必须包含如下内容：

 - 1.**一个空格**，在属性和元素名称之间。(如果已经有一个或多个属性，就与前一个属性之间有一个空格。)
 - 2.属性名称，后面**跟着一个等于号=**。
 - 3.一个属性值，由一对**引号“ ”引起来**。


### 布尔属性

一些属性，本身可以没有值，这类属性被称为布尔属性。我们更多关心的是这个元素是否有这个属性。

```java
<input type="text" disabled>
<input type="text" disabled="true">
<input type="text" disabled="false">
<input type="text" disabled="随便写什么">
```

上述四种写法，其实效果是完全一样的。都是使得一个输入 **(input)** 禁止输入 **(disabled)。**     

### 单引号或者双引号？

HTML 中，单引号和双引号的地位是相同的，以下两种情况都可以：

```java
<a  href="http://www.example.com">示例站点链接</a>

<a  href='http://www.example.com'>示例站点链接</a>
```

在一个HTML中已使用一种引号，你可以在此引号中嵌套另外一种引号：

```java
<a href="http://www.example.com" title="你觉得'好玩吗'？">示例站点链接</a>

<a href="http://www.example.com" title='你觉得"好玩吗"？'>示例站点链接</a>
```




## 文档结构(Document Structure)

一个html文件应包含以下结构

```java
 <html><!--html文件标识 -->
	<head><!-- 头部：用于设置编码格式和添加一些css样式，连接js之类的 -->
		<meta charset=utf8>
	    <title>标题</title>
	</head>
	<body>
		<!-- 主体 -->
	</body>
</html>
```

## 实体引用(Entity References)

在**HTML**中，字符  **<*,>,',",&*,**	是特殊字符. 它们是HTML语法自身的一部分, 那么你如何将这些字符包含进你的文本中呢, 比如说如果你真的想要在文本中使用符号&或者小于号, 而不想让它们被浏览器视为代码并被解释?
我们必须使用**字符引用** —— **表示字符的特殊编码,** 它们可以在那些情况下使用. **每个字符引用以符号&开始, 以分号(;)结束.**
常见实体引入如下：

![在这里插入图片描述](https://img-blog.csdnimg.cn/20210323101453506.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQ1NjYxMTI1,size_16,color_FFFFFF,t_70)
**HTML中的空白**

```java
<p>狗 狗 很 呆 萌。</p>

<p>狗 狗		很 呆 萌。</p>
```

这两段代码表示是一样的，无论你在HTML元素的内容中使用多少空格(包括空白字符，包括换行)，当渲染这些代码的时候，HTML 解释器会将连续出现的空白字符减少为一个单独的空格符。如果要使用**多个空格**，**需要使用&nbsp**。

## DOM(Document Object Model) 树

**DOM**（Document  Object   Model——**文档对象模型**）是载入到浏览器中的文档模型，以节点树的形式来表现文档，每个节点代表文档的构成部分（例如:页面元素、字符串或注释等等）。
![在这里插入图片描述](https://img-blog.csdnimg.cn/20210323101956968.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQ1NjYxMTI1,size_16,color_FFFFFF,t_70)

## 连接css和js

```java
<head>
<link rel="stylesheet" type="text/css" href="路径.css" />
</head>

<script type="text/javascript" src="路径.js"></script>
```

# JavaScript

**JavaScript 是一种脚本，一门编程语言**，它可以在网页上实现复杂的功能，网页展现给你的不再是干巴巴的静态信息，而是丰富多彩的动态信息JavaScript 怎能缺席。它是网页的灵魂。

## JS的两种写法：

JS的代码主要分为两类，基础的逻辑业务代码（if，for，praseInt）和操控控件的代码（取控件，设置控件的值）

 - 使用原生JS
   不同的浏览器解析js的结果是不一样的
    原生js写起来太麻烦

```java
 var num1 = document.getElementById("num1");
 var num2 = document.getElementById("num2");
```

 - 使用jQuery
   方便简单的操控插件

```java
var num1 = jQuery("#num1");
var num2 = jQuery("#num2");
```

