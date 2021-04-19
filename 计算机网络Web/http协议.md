

# http（超文本传输协议）

什么是协议呢？简单点来说就是双方指定的规则，不能够违背的约定。下面我们来了解一下http协议。

# URL（统一资源定位符）

## URL格式

平时我们俗称的 "**网址**" 其实就是说的 **URL**比如百度搜索蛋糕为例
![在这里插入图片描述](https://img-blog.csdnimg.cn/20210329001241855.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQ1NjYxMTI1,size_16,color_FFFFFF,t_70)
![在这里插入图片描述](https://img-blog.csdnimg.cn/20210329002844121.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQ1NjYxMTI1,size_16,color_FFFFFF,t_70)

## urlencode和urldecode（编码和解码）

像 <code>**/ ? :**</code> 等这样的字符, 已经被url当做特殊意义理解了. 因此这些字符不能随意出现.

比如, 某个参数中需要带有这些特殊字符, 就必须先对特殊字符进行转义. 转义的规则如下:
**将需要转码的字符转为16进制，然后从右到左，取4位(不足4位直接处理)，每2位做一位，前面加上%， 编码成%XY格式**
![在这里插入图片描述](https://img-blog.csdnimg.cn/20210329003536759.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQ1NjYxMTI1,size_16,color_FFFFFF,t_70)

# http协议格式

http主要分为两部分，Request（请求）、Respsone（相应）
![在这里插入图片描述](https://img-blog.csdnimg.cn/20210329003727740.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQ1NjYxMTI1,size_16,color_FFFFFF,t_70)

## Request（请求）

**请求主要分为四部分：**

### 请求行（首行）

 首行由三部分组成，请求方法，URL，版本号

 - **请求方法**

常用的请求方法有[GET]和[POST]，二者还是有一定的区别的，
<code>GET的请求数据只能放在URL中(万恶的源泉）</code>，所有就导致了一系列的问题。
1.首先GET方法的数据类型只能为ASCII码格式（POST为任意格式）
2.GET发送的数据有长度限制（POST没有限制）
3.GET请求数据放在URL中，这样会直接显示出来，所以不安全，且一般请求正文 为空（POST可以将数据放在请求正文中，所以相对来说比较安全）

 - **URL （要访问的地址）**
 - **版本号（协议的版本号）**

### 请求报头

**常见的header**

 - **<code>Content-Type:** 数据类型(text/html等)
 - **Content-Length**: Body的长度
 - **Host**: 客户端告知服务器, 所请求的资源是在哪个主机的哪个端口上;
 - **User-Agent:** 声明用户的操作系统和浏览器版本信息;
 - **referer**: 当前页面是从哪个页面跳转过来的;
 - **<code>location**: 搭配3xx状态码使用, 告诉客户端接下来要去哪里访问;
 - **Cookie**: 用于在客户端存储少量信息. 通常用于实现会话(session)的功能;

### 空行

标志着请求报头的结束，下面为请求正文

###  请求正文

具体需要服务器干什么，给我们什么相应

说再多也没用，抓个包来看看吧

## Response（相应）

**相应也分为四部分：**

### 状态行

状态行由三部分组成：版本号、状态码、状态描述

 - **版本号**：即为协议的版本号
 - **<code>状态码**：反映的是对于客户端的请求我们做出了怎样的回应
   ![在这里插入图片描述](https://img-blog.csdnimg.cn/20210329011113598.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQ1NjYxMTI1,size_16,color_FFFFFF,t_70)
   **常见的状态码有：**
 - **200**：请求成功，一般用于get和post请求
 - **301（重定向）**：永久重定向，请求的资源已经被永久移动到新的URL，之后任何新的请求都会用新的URL代替
 - **302（转发）**：临时重定向，与301类似，只是资源被临时移动，客户端应继续使用原有的URL
   转发和重定向的区别：
    重定向：返回3XX状态码+Location响应头，表示要跳转的路径，浏览器接收到相应数据后自动跳转
    转发：一次请求，后端接收直接把转发路径的资源作为响应体返回
    区别：
    URL路径是否改变：重定向会改变，转发不会
    发起的网络请求次数：重定向发起两次，转发发起一次
    ![在这里插入图片描述](https://img-blog.csdnimg.cn/20210329163938370.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQ1NjYxMTI1,size_16,color_FFFFFF,t_70)

 - **400**：客户端请求的语法错误（http协议格式不对、请求数据格式、数据类型等书写错误）
 - **403**：服务器理解客户端的请求，但拒绝了（权限不够）
 - **404**：服务器无法根据客户单的请求找到资源（找到了相应的主机，但没找到资源）
   **405**：客户端请求中的方法被禁止（没有重写）

 **状态码描述**：状态码的相应描述

### 响应报头

和上面Request一样

### 空行

区分响应报头和响应正文的

### 响应正文

对于客户端的请求返回的数据

## 抓包分析

说再多也没用，抓个包来看看吧
![在这里插入图片描述](https://img-blog.csdnimg.cn/20210329163320508.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQ1NjYxMTI1,size_16,color_FFFFFF,t_70)

# 客户端与服务端的联系

![在这里插入图片描述](https://img-blog.csdnimg.cn/2021032916413338.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQ1NjYxMTI1,size_16,color_FFFFFF,t_70)


