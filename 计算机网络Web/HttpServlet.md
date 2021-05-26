@[TOC](Servlet)
#  什么是servlet

 - **概念**：Java Servlet 是运行在 Web 服务器或应用服务器上的程序，它是作为来自 Web 浏览器或其他 HTTP 客户端的请求和HTTP 服务器上的数据库或应用程序之间的中间层。
 - **定位**：Java Servlet用Java编写的服务器端程序（web application）。
 - **作用**：其主要功能在于交互式地浏览和修改数据，生成动态Web内容。
 - **理解**：狭义的Servlet是指Java语言实现的一个接口，广义的Servlet是指任何实现了这个Servlet接口的类，一般情况下，我们将Servlet理解为后者。

#  HttpServlet 和 Servlet 的关系
```java
interface Servlet { 
    void init(ServletConfig var1) throws ServletException; 
    void service(ServletRequest var1, ServletResponse var2) throws ServletException, IOException; 
    void destroy(); 
    // 省略了部分我们不关心的方法
}
```
Servlet 在这个语境下只是一个 java 中的普通接口

```java
abstract class HttpServlet implements Servlet {
    @Override
    protected void service(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException
    { 
        // 根据 request 的 method 不同，调用不同的方法 }
        // GET 时调用
        protected void doGet(protected void service(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException
        { ... }
        // POST 时调用
        protected void doPost(protected void service(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException
        { ... }
        // 省略了 HTTP 协议支持的其他方法
    }
}
```
**总结**
 HttpServlet 是 Servlet 接口的一个实现类，但它本身是个抽象类，所以需要根据需求，选择覆写 doGet 或者 doPost 或者其他合适的方法即可
 #  HttpServlet处理Http请求
 - Servlet的service()方法是请求的入口方法，HttpServlet实现service()方法在这个入口方法中根据不同的Http请求方法（如GET、POST请求）调用不同的方法。
 - 大多数应用程序都是要于HTTP结合起来使用。这意味着可以利用HTTP提供的特性。 javax.servlet.http包是ServletAPI中的第二个包，其中包含了用于编写Servlet应用程序的类和接口，并且许多类型都覆写了javax.servlet 中的类型。
 - HttpServlet类覆盖了 javax.servlet.GenericServlet
 类。使用HttpServlet时，需要使用代表Servlet请求和Servlet响应的 HttpServletRequest 和HttpServletResponse 对象。
 
 HttpServlet中的Service方法会检验用来发送请求的HTTP方法(通过调用request.getMethod() ), 并调用以下方法之一：
![在这里插入图片描述](https://img-blog.csdnimg.cn/20210402001617644.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQ1NjYxMTI1,size_16,color_FFFFFF,t_70)
实际在编写servlet程序的时候，不再需要覆盖Service方法了，只要覆盖doGet或者doPost即可。
# Servlet 客户端 HTTP 请求
## 客户端Request常见报头
![在这里插入图片描述](https://img-blog.csdnimg.cn/20210402001836362.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQ1NjYxMTI1,size_16,color_FFFFFF,t_70)

## 操作 HTTP Request头的方法
下面的方法可用在 Servlet 程序中读取 HTTP 头。这些方法通过 HttpServletRequest 对象使用。
![在这里插入图片描述](https://img-blog.csdnimg.cn/20210402002005895.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQ1NjYxMTI1,size_16,color_FFFFFF,t_70)
# Servlet 服务器 HTTP 响应
## 服务器端Response常见报头
![在这里插入图片描述](https://img-blog.csdnimg.cn/20210402002137516.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQ1NjYxMTI1,size_16,color_FFFFFF,t_70)

## 操作HTTP Response头的方法
下面的方法可用于在 Servlet 程序中设置 HTTP 响应报头。这些方法通过 HttpServletResponse 对象可用。
![在这里插入图片描述](https://img-blog.csdnimg.cn/20210402002219987.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQ1NjYxMTI1,size_16,color_FFFFFF,t_70)

# Servlet 对象的生命周期
![在这里插入图片描述](https://img-blog.csdnimg.cn/20210402000813594.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQ1NjYxMTI1,size_16,color_FFFFFF,t_70)
# Session和Cookie
**Http** 是一个**无状态**协议, 就是说这一次请求和上一次请求是没有任何关系的，互不认识的，没有关联的。这种无状态的的好处是快速（但服务器连接是数量限制的，为65535）。坏处是需要进行用户状态保持的场景时[比如，登陆状态下进行页面跳转，或者用户信息多页面共享等场景]，必须使用一些方式或者手段比如： **session** 和**cookie**
## Cookie

 - **使用场景**
 
**免登陆**（**Http** 是一个无状态的协议，但是访问有些资源的时候往往需要经过认证的账户才能访问， 而且要一直保持在线状态）
 - **实现**
用户第一次登陆通过之后，服务端响应头携带Set-Cookie信息，告诉客户端，让浏览器自动设置Cookie到本地，之后的每次请求浏览器都会自动携带Cookie头（将用户的信息保存在客户端本地（和浏览器相关的本地路径下），域名绑定用户信息的cookie，之后在此访问某个域名的时候，浏览器自动从本地抓取该域名的cookie信息）如下图：
![在这里插入图片描述](https://img-blog.csdnimg.cn/20210401000141628.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQ1NjYxMTI1,size_16,color_FFFFFF,t_70)
 - **小结**
 
  cookie是保存在客户端本地的文件
  cookie常用于免登陆
  登陆成功后响应头返回Set-Cookie,之后每次都会自动携带Cookie头
 
 - **Servlet操作cookie**
 以下是在 Servlet 中操作 Cookies 时可使用的有用的方法列表。
![在这里插入图片描述](https://img-blog.csdnimg.cn/20210402002421680.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQ1NjYxMTI1,size_16,color_FFFFFF,t_70)


## Session
 - **使用场景**

Cookie解决了一定的问题，但是又引进了新的安全问题，一旦cookie丢失，用户信息泄露，而且可以随意修改cookie的值来模拟登陆，所以有了另一种解决方法，将**用户敏感信息保存至服务器**

 - **实现**
 
1、 登陆成功后，服务器生成随机的字符串sessionid（类似于通行证），保存在tomcat的用户信息数据结构中，一个sessionid绑定一个用户，但一个用户保存多个信息
2、 然后将sessionid放在响应头的一个键值对里（键是双方约定好的，值就是sessionid的值）
 3、客户端之后的请求，都会携带sessionid（例如JSESSIONID=xxxxx）
 4、服务端接收请求，验证sessionid（在map中根据通行证号，查询用户，来判断是否登录）

![在这里插入图片描述](https://img-blog.csdnimg.cn/20210401002001166.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQ1NjYxMTI1,size_16,color_FFFFFF,t_70)
![在这里插入图片描述](https://img-blog.csdnimg.cn/20210401002024114.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQ1NjYxMTI1,size_16,color_FFFFFF,t_70)

 - **小结**
session用于会话，保持身份验证（主要解决敏感资源的访问问题）
session的信息保存在服务器当中
session在会话结束（超时/注销），或者服务器重启后会消失
 - **Servlet 操作session方法（HttpSession** 
 
Servlet 还提供了 HttpSession 接口，该接口提供了一种跨多个页面请求或访问网站时识别用户以及存储有关用户信息的方式。
Servlet 容器使用这个接口来创建一个 HTTP 客户端和 HTTP 服务器之间的 session 会话。会话持续一个指定的时间段，跨多个连接或页面请求。
我们可以通过调用 HttpServletRequest 的公共方法 getSession() 来获取 HttpSession 对象，如下所示：

```java
HttpSession session = request.getSession();//默认为true 登陆成功则创建
HttpSession session = request.getSession(false);//true 登录验证不通过则不创建
```
需要在向客户端发送任何文档内容之前调用 request.getSession()
下面总结了 HttpSession 对象中可用的几个重要的方法：
![在这里插入图片描述](https://img-blog.csdnimg.cn/20210402002701613.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQ1NjYxMTI1,size_16,color_FFFFFF,t_70)

## 二者的区别
 - Cookie以文本文件格式存储在浏览器中，而session存储在服务端
 - 因为每次发起Http 请求，都要携带有效Cookie信息，所以Cookie一般都有大小限制，以防止增加网络压力,一般不超过4k
 - 可以轻松访问cookie值但是我们无法轻松访问会话值，因此session方案更安全
