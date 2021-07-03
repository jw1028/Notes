# SpringMVC

## Tomcat和Servlet执行流程回顾

## 概述

Spring Framework中Web模块包含了 spring-web、spring-webmvc、spring-websocket 和
spring-webmvc-portlet 4 个模块。

我们主要学习前两个模块：

```
spring-web 模块提供了web开发所需要的基础特性，如文件上传，基于IoC容器初始化 Servlet 监听器
```

等。

```
spring-webmvc 模块包含了Spring的 MVC 实现，及 REST 方式的 Web 服务。
```

SpringMVC框架围绕 DispatcherServlet（前端控制器） 这个核心展开，DispatcherServlet 是

SpringMVC框架的总导演、总策划，它负责截获请求并将其分派给相应的处理器处理。这部分我们在学
习完 SpringMVC 的使用后再来结合整体流程回顾。

传统的基于Spring Framework的web开发需要大量的 xml 配置，在有SpringBoot以后，Web开发的效
率得到了很大的提升，几乎大部分配置可以使用默认约定的规则。我们基于SpringBoot的项目来进行
SpringMVC的学习。

## MVC设计模式介绍

MVC（Model View Controller）是软件工程中的一种软件架构模式，它把软件系统分为模型、视图和控
制器三个基本部分。

|      |                                                              |
| ---- | ------------------------------------------------------------ |
|      | ![img](file:///C:\Users\86131\AppData\Local\Temp\ksohtml1316\wps1.png) |

**Model（模型）** 是应用程序中用于处理应用程序数据逻辑的部分。

通常模型对象负责在数据库中存取数据。

**View（视图）** 是应用程序中处理数据显示的部分。

通常视图是依据模型数据创建的。


**Controller（控制器）** 是应用程序中处理用户交互的部分。

通常控制器负责从视图读取数据，控制用户输入，并向模型发送数据。

说明：一般现在主流的前后端分离的开发模式，后端人员不再写前端代码，我们也不学习前端，对应
MVC中View的部分，我们也就不关心了。

## SpringMVC实战

为了进行以下实验，请准备以下网页资源：在 src/main/resources/static 目录中，创建

```
home.html：
```

### @Controller

@Controller注解标注是一个类是Web控制器，其和@Component注解等价，只不过在Web层使用，其
便于区分类的作用。

### @RequestMapping

@RequestMapping是Spring Web应用程序中最常被用到的注解之一。

在对SpringMVC进行配置的时候，需要指定请求与处理方法之间的映射关系，这时候就需要使用
@RequestMapping注解。该注解可以在控制器类的级别和其方法级别上使用。如以下控制器（注：返
回值可以参考下一章节《控制器方法的返回》）：

以上方法提供的服务路径为 /test/1。也就是类和方法上@RequestMapping配置的路径相加。此时可

以使用任何请求方法，且发生了重定向，地址栏URL会发生变化。

也可以单独只在方法上使用@RequestMapping，以下为新建的 Test2Controller：

```
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>主页</title>
</head>
<body>
<p>进入主页啦</p>
</body>
</html>
```


```
package org.example.demo.controller;
```

```
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;
```

```
@Controller
@RequestMapping("/test")
public class TestController {
```

```
@RequestMapping("/1")
public String test1(){
return "redirect:/home.html";
}
}
```



此时提供的服务路径为 /test2。

需要补充说明的：

@RequestMapping注解能够处理的HTTP请求方法有：GET, HEAD, POST, PUT, PATCH, DELETE,
OPTIONS, TRACE。

为了能够将一个请求映射到一个特定的HTTP方法，你需要在@RequestMapping中使用method参数声
明HTTP请求所使用的方法类型。如下示例，在 TestController 中添加请求映射方法：

### 控制器方法的返回

Controller方法支持多种返回类型，详细可参考：SpringMVC处理器方法返回类型。其中很多我们都用
不上。

以下的返回类型为重要的、经常使用的方式：

#### String返回类型

##### 有两种使用方式：

1. 返回 URI 资源路径的字符串，可以使用 redirect:/服务路径 表示重定向到某个路径，
   forward:/服务路径 表示转发到某个路径，如果前边不写默认就是转发。
2. @RequestMapping结合@ResponseBody，返回的字符串会作为响应体内容。此时响应的
   Content-Type为 text/plain 普通文本。

如下示例，在 TestController 中添加请求映射方法：

```
package org.example.demo.controller;
```

```
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;
```

```
@Controller
public class Test2Controller {
```

```
@RequestMapping("/test2")
public String test(){
return "redirect:/home.html";
}
}
```




##### //指定服务提供的请求方法

```
@RequestMapping(value = "/2", method = RequestMethod.GET)
public String test2(){
return "forward:/home.html";
}
```


```
@RequestMapping("/3")
@ResponseBody
public String test3(){
return "好了，已经知道了";
}
```


#### 返回普通的Java类型

```
返回类型为Object，一般使用带Getter，Setter方法的模型类
结合@ResponseBody使用，表示将对象序列化后的数据放在响应体返回
在SpringBoot中默认响应的Content-Type为 application/json
非字符串对象会自动序列化为 json 字符串
```

如下示例，在 TestController 中添加请求映射方法：

#### 返回ResponseEntity（了解）

使用SpringMVC框架中提供的ResponseEntity，可以灵活的设置响应状态码，响应头，响应体，该类的
方法主要为链式调用，如以下请求映射方法，和 test4 方法返回是一样的：

### @ResponseBody

##### 表示将控制器方法的返回序列化作为响应体内容返回前端。

根据之前《控制器方法的返回》说明，使用@ResponseBody注解：

1. 返回类型为String，表示响应Content-Type: text/plain，且响应体为控制器方法的字符串返回值
2. 返回类型为普通Java类型，表示响应Content-Type: application/json，以返回对象序列化为json后
   作为响应体。
3. @ResponseBody可以使用在类上，表示该类中所有方法都是默认以返回值作为响应体，也就是所
   有方法都使用@ResponseBody。

注意：如果返回值为null，表示响应体内容为空

如下示例，在 TestController 中添加请求映射方法：

```
@RequestMapping("/4")
@ResponseBody
public Object test4(){
Map<Integer, String> map = new HashMap<>();
map.put( 1 , "张三");
map.put( 2 , "李四");
map.put( 3 , "王五");
return map;
}
```


```
@RequestMapping("/7")
public ResponseEntity test7(){
Map<Integer, String> map = new HashMap<>();
map.put( 1 , "张三");
map.put( 2 , "李四");
map.put( 3 , "王五");
return ResponseEntity.status( 200 ).body(map);
}
```



### 补充：组合注解

可以使用组合注解来完成同时定义多个注解的效果，如：@RestController，@GetMapping，
@PostMapping

以下为@RestController注解申明：

说明该注解使用在类上，和使用两个注解@Controller，@ResponseBody在类上意思一样

同理：

@GetMapping即是：@RequestMapping(method = RequestMethod.GET)

@PostMapping即是：@RequestMapping(method = RequestMethod.POST)

### 控制器方法支持的参数类型

控制器方法中，可以自动注入一些对象，SpringMVC会自动将HTTP请求数据填充到特定的对象中。详细
内容可以参考：SpringMVC控制器方法参数列表。

以下方法参数注解为重要的，经常使用的方式：

首先定义一个控制器，使用@RestController，根据方法返回值类型，返回字符串网页，或是 json 序列
化对象：

##### 以下为在该控制器中定义的请求映射方法：

```
@RequestMapping("/5")
@ResponseBody
public String test5(){
return null;
}
```

```
@RequestMapping("/6")
@ResponseBody
public Object test6(){
return null;
}
```


```
@Target(ElementType.TYPE)
@Retention(RetentionPolicy.RUNTIME)
@Documented
@Controller
@ResponseBody
public @interface RestController {
...
```

##### 1 2 3 4 5 6 7

```
package org.example.demo.controller;
```

```
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
```

```
@RestController
@RequestMapping("/arg")
public class TestArgumentsController {
}
```





#### @PathVariable

一般的 URI 服务路径都是固定的，SpringMVC提供了 restful 风格可以变化的 URI。示例：

##### 说明：

##### {}是将服务路径 URI 中的部分定义为变量，之后在方法参数中获取该路径变量。更多格式可参考

##### URI格式。

```
请求 /arg/owners/1/pets/2，显示的网页内容为：主人id：1, 宠物id： 2 。
变量已经定义了为Long长整形，所以不能转换为Long的 URI 都会报错，如请求
/arg/owners/abc/pets/2 就会报错，响应状态码 400 。
变量名ownerId，petId必须和 URI 中的定义名称一致。
```

#### @RequestParam

当请求数据要绑定到某个简单对象时，可以使用@RequestParam。

```
URL 中的请求数据queryString
请求头，Content-Type为表单默认提交的格式 application/x-www-form-urlencoded，请求体中
的数据
请求头，Content-Type为 multipart/form-data，请求体中的数据。form-data 可以提交文本
数据，也可以提交二进制文件。
以上简单对象包括：基本数据类型、包装类型、MultipartFile（接收二进制文件）
```

需要注意@RequestParam注解参数默认为 required=true，如果不传该参数就会报错，需要指定
为：@RequestParam(required = false)。

示例一，通过 post 请求，请求数据的键分别为 username 和 password，指定为queryString，或

Content-Type为表单数据类型，form-data 都可以：

示例二：通过 post 请求，请求数据的键为 count，指定为非必须输入。

注意以上代码使用包装类型 Integer，如果使用 int，不传入键为 count 的请求数据就会报错，因为
null 无法转换为 int。

```
@GetMapping("/owners/{ownerId}/pets/{petId}")
public String findPet(@PathVariable Long ownerId, @PathVariable Long petId) {
return "主人id："+ownerId+", 宠物id："+petId;
}
```


```
@PostMapping("/param1")
public Object param1(@RequestParam String username, @RequestParam String
password){
Map<String, String> map = new HashMap<>();
map.put("用户名", username);
map.put("密码", password);
return map;
}
```


```
@PostMapping("/param2")
public Object param2(@RequestParam(required = false) Integer count){
Map<String, Integer> map = new HashMap<>();
map.put("count", count);
return map;
}
```



##### 建议是：必填的请求数据可以使用基本数据类型，可以不传的参数，都要使用包装类型。

示例三：通过 post 请求，使用 form-data 提交一个键为 file 的二进制文件，需要注意整个请求数据

大小不能超过10m，单个文件大小不超过1m。（这是 SpringBoot 的默认设置，修改需要通过
src/main/resources/application.properties 文件配置）

#### POJO对象

POJO（Plain Ordinary Java Object）：简单的 java 对象，实际就是属性提供了Getter，Setter方法的
普通对象。

使用 java 对象和使用@RequestParam注解非常类似，只是有点细节不同：

```
@RequestParam是以方法参数变量名和传入的键对应，POJO对象作为方法参数时，是以POJO对
象中的属性名对应传入的键
@RequestParam默认必须传入该请求数据，而 POJO 对象是根据请求数据来填充属性，如果请求
数据没有，则属性就是默认值（new对象时每个属性的默认值）。
```

示例一：简单的包装类型，和使用@RequestParam结果一样

示例二：使用自定义 POJO 类，通过SpringMVC框架自动解析请求数据并设置到对象中。

以下先定义一个用户类：

```
@PostMapping("/param3")
public Object param3(@RequestParam MultipartFile file) throws IOException {
Map<String, String> map = new HashMap<>();
map.put("文件名", file.getName()+", "+file.getOriginalFilename());
map.put("文件类型", file.getContentType());
map.put("文件大小", file.getSize()/ 1024 +"KB");
map.put("文件内容（二进制转字符串）", new String(file.getBytes()));
return map;
}
```

```
@PostMapping("/pojo1")
public Object pojo1(String username, Integer count){
Map<String, String> map = new HashMap<>();
map.put("用户名", username);
map.put("count", String.valueOf(count));
return map;
}
```


```
package org.example.demo.model;
```

```
import lombok.Getter;
import lombok.Setter;
import lombok.ToString;
```

```
@Getter
@Setter
@ToString
public class User {
```

```
private String username;
private String password;
}
```



##### 在请求映射方法中作为方法参数，让请求数据自动设置到对象属性：

示例三：POJO 对象同样可以直接获取 form-data 方式的数据，包括二进制文件

#### @RequestBody

当请求的数据类型Content-Type为 application/json 时，需要显示的使用@RequestBody注解。示

例：

##### 请求数据为：

对应在PostMan中操作是：

```
@PostMapping("/pojo2")
public Object pojo2(User user){
Map<String, String> map = new HashMap<>();
map.put("用户名", user.getUsername());
map.put("密码", user.getPassword());
return map;
}
```


```
@PostMapping("/pojo3")
public Object pojo3(User user, MultipartFile file) throws IOException {
Map<String, String> map = new HashMap<>();
map.put("用户名", user.getUsername());
map.put("密码", user.getPassword());
map.put("文件名", file.getName()+", "+file.getOriginalFilename());
map.put("文件类型", file.getContentType());
map.put("文件大小", file.getSize()/ 1024 +"KB");
map.put("文件内容（二进制转字符串）", new String(file.getBytes()));
return map;
}
```



```
@PostMapping("/json")
public Object json(@RequestBody User user) {
Map<String, String> map = new HashMap<>();
map.put("用户名", user.getUsername());
map.put("密码", user.getPassword());
return map;
}
```


```
POST /arg/json HTTP/1.
Host: localhost:
Content-Type: application/json
Content-Length: 49
```

```
{
"username":"abc",
"password":"123"
}
```



#### @RequestPart

对于请求的数据类型Content-Type为 multipart/form-data 时，二进制文件除了以上

@RequestParam和 POJO 对象的方式外，还可以使用@RequestPart。示例：

对于@RequestPart和@RequestParam的区别，涉及 form-data 比较复杂的请求数据提交，我们这里

不讨论，有兴趣的可以参考：SpringMVC MultiPart

#### Servlet API

在控制器方法参数中，可以使用Servlet相关API，SpringMVC会自动将相关Servlet对象装配到方法参数
中，如 HttpServletRequest、HttpServletResponse 、HttpSession 等。示例：

返回值设置为void，此时和在Servlet中开发差不多了。当然也可以使用返回值，SpringMVC会自动跳转
页面（无@ResponseBody，返回类型为String），或返回Content-Type: text/html的网页内容（使用
@ResponseBody，返回类型为String），或返回 json 字符串（@ResponseBody，返回 POJO 对象）

```
@PostMapping("/part")
public Object part(User user, @RequestPart MultipartFile file) throws
IOException {
Map<String, String> map = new HashMap<>();
map.put("用户名", user.getUsername());
map.put("密码", user.getPassword());
map.put("文件名", file.getName()+", "+file.getOriginalFilename());
map.put("文件类型", file.getContentType());
map.put("文件大小", file.getSize()/ 1024 +"KB");
map.put("文件内容（二进制转字符串）", new String(file.getBytes()));
return map;
}
```



```
@GetMapping("/servlet")
public void servlet(HttpServletRequest req, HttpServletResponse resp) throws
IOException {
req.setCharacterEncoding("UTF-8");
resp.setCharacterEncoding("UTF-8");
resp.setContentType("text/html");
String username = req.getParameter("username");
String password = req.getParameter("password");
PrintWriter pw = resp.getWriter();
pw.println("接收到的请求为：用户名="+username+"，密码："+password);
pw.flush();
pw.close();
}
```



#### @RequestHeader（了解）

绑定请求头Header信息

#### @CookieValue（了解）

绑定请求头Cookie里边的信息

### SpringMVC自定义配置

SpringBoot中使用SpringMVC非常方便，SpringBoot提供了大部分的MVC默认功能，并且需要自定义
某部分功能也非常方便，在配置类中实现 WebMvcConfigurer 接口，根据需要重写方法即可：

##### 我们这里只介绍两个以后用到的功能，也就是重写两个方法：

#### 自定义后端路径映射

重写 configurePathMatch 方法，实现时，可以添加统一的服务路径前缀：

此时所有定义的服务路径都要在前面加上 /api 再能访问，如 /arg/param1 现在应该访问
/api/arg/param1。

```
@GetMapping("/header")
public String header(@RequestHeader("Accept-Encoding") String encoding,
@RequestHeader("User-Agent") String userAgent) {
return String.format("<p>Accept-Encoding: %s</p><p>User-Agent: %s</p>",
encoding, userAgent);
}
```


```
@GetMapping("/cookie")
public String cookie(@CookieValue("JSESSIONID") String cookie) {
return String.format("JSESSIONID: %s", cookie);
}
```


```
package org.example.demo.config;
```

```
import org.springframework.context.annotation.Configuration;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;
```

```
@Configuration
public class AppConfig implements WebMvcConfigurer {
```

```
}
```


```
@Override
public void configurePathMatch(PathMatchConfigurer configurer) {
//Controller路径，统一添加请求的路径前缀，第二个参数，c是Controller类，返回boolean
表示是否添加前缀
//所有Controller请求路径，都要带/api的前缀
configurer.addPathPrefix("api", c->true);
}
```



#### 自定义Controller拦截器

重写 addInterceptors 方法，实现时，需要指定拦截器，并配置需要拦截、不拦截的路径。

在客户端发起请求时，如果路径最终匹配该规则，则执行拦截器中的接口方法。

以下示例，实现用户统一的会话管理：

首先定义一个用户登录接口：

注意现在需要加上路径前缀，使用 /api/user/login 访问。

再定义一个拦截器，需要实现 HandlerInterceptor 接口，根据需要重写接口方法，如以下代码：

```
package org.example.demo.controller;
```

```
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
```

```
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpSession;
import java.util.HashMap;
import java.util.Map;
```

```
@RestController
@RequestMapping("/user")
public class UserController {
```

```
@PostMapping("/login")
public Object login(String username, String password, HttpServletRequest
req){
Map<String, Object> map = new HashMap<>();
//模拟用户登录时，用户名和密码校验
if("abc".equals(username) && "123".equals(password)){
//登录成功，创建session
HttpSession session = req.getSession();
//添加用户身份信息到session
session.setAttribute("user", username+", "+password);
map.put("用户名", username);
map.put("密码", password);
}
return map;
}
}
```


```
package org.example.demo.config.interceptor;
```

```
import org.springframework.http.HttpStatus;
import org.springframework.web.servlet.HandlerInterceptor;
```

```
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import javax.servlet.http.HttpSession;
```

```
public class LoginInterceptor implements HandlerInterceptor {
```

```
/**
```



最后在SpringMVC配置中，将该拦截器添加到配置中,：

以上配置通过将后端路径统一加上前缀 /api，再拦截除登录以外的其他后端接口，校验session来判断

是否允许继续执行控制器方法，很好的实现了统一的用户会话管理，也是经常使用的手段。

### @ControllerAdvice

@ControllerAdvice注解（控制器通知、控制器增强）定义的类，会自动注册为一个Bean对象，将扫描
指定包中带@Controller注解的类：在客户端发起请求，映射到控制器方法时，结合其他注解或接口完成
统一的增强功能。

注：可以不指定扫描的包，对容器中所有@Controller生效。

#### 应用一：统一异常处理

此时需要结合@ExceptionHandler使用，可以实现控制器方法中出现异常后的统一异常处理。

先定义一个抛异常的服务，在 org.example.demo.controller.TestRestController 中，定义如下

方法：

```
* 重写preHandle方法，表示请求路径最终匹配到某个Controller时，在调用控制器
* 方法前，先执行本拦截器的前置处理逻辑
*/
@Override
public boolean preHandle(HttpServletRequest request, HttpServletResponse
response, Object handler) throws Exception {
HttpSession session = request.getSession(false);
//session不为空，表示已登录
if(session != null){
//返回true，允许继续执行Controller中的方法
return true;
}
//响应状态码设置为 401
response.setStatus(HttpStatus.UNAUTHORIZED.value());
//返回false，不再执行Controller中的方法，直接响应一个空的响应体
return false;
}
}
```

```
@Override
public void addInterceptors(InterceptorRegistry registry) {
registry.addInterceptor(new LoginInterceptor())
.addPathPatterns("/api/**")//添加路径拦截规则，**表示下级多级目录的任意字符匹
配
.excludePathPatterns("/api/user/login");//排除登录路径
}
```

```
@GetMapping("/exception")
public Object exception(){
Map<Integer, String> map = new HashMap<>();
map.put( 1 , "张三");
map.put( 2 , "李四");
map.put( 3 , "王五");
int i = 1 / 0 ;
return map;
}
```



注意：该接口访问路径为 /api/exception，且因为配置了会话管理的拦截器，需要先登录以后再访

问。

接着再定义控制器通知及异常处理逻辑：

此时在登录以后，访问 /api/exception 接口将会报错，抛出的异常属于Exception类，所以会进入

@ExceptionHandler注解的方法，由该方法返回响应内容。可以看到，返回的数据为统一的异常信息。

#### 应用二：响应数据格式的统一封装

此时需要结合ResponseBodyAdvice接口，可以实现对控制器方法返回数据的统一封装。

```
package org.example.demo.config;
```

```
import org.springframework.web.bind.annotation.ControllerAdvice;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.ResponseBody;
```

```
import java.util.HashMap;
import java.util.Map;
```

```
//在SpringBoot中使用，会扫描启动类所在包下所有@Controller类
@ControllerAdvice
public class ExceptionAdvice {
```

```
//如果客户端请求，执行控制器方法抛Exception异常，会执行本方法
@ExceptionHandler(Exception.class)
//方法返回值作为响应体
@ResponseBody
public Object handle(Exception e){//方法参数即为捕获到的异常
//构造响应数据
Map<String, Object> map = new HashMap<>();
map.put("success", false);
map.put("code", "ERR000");
map.put("message", e.getMessage());
return map;
}
}
```

```
package org.example.demo.config;
```

```
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.core.MethodParameter;
import org.springframework.http.MediaType;
import org.springframework.http.server.ServerHttpRequest;
import org.springframework.http.server.ServerHttpResponse;
import org.springframework.web.bind.annotation.ControllerAdvice;
import
org.springframework.web.servlet.mvc.method.annotation.ResponseBodyAdvice;
```

```
import java.util.HashMap;
import java.util.Map;
```

```
//实现ResponseBodyAdvice接口，表示可以根据条件对返回的数据重写
@ControllerAdvice
```



这种统一数据格式的封装方式，当控制器方法设置的返回类型为Object，返回对象为null时，还是不能
封装为统一的格式，之后项目介绍另一种方式。

## SpringMVC流程

## 场景练习

```
public class ResponseAdvice implements ResponseBodyAdvice {
```

```
//注入容器中的ObjectMapper，SpringBoot默认使用jackson框架中的ObjectMapper完成
json的序列化
@Autowired
private ObjectMapper objectMapper;
```

```
//方法参数可以获取请求调用的控制器类及方法，再决定是否要执行响应内容重写
@Override
public boolean supports(MethodParameter returnType, Class converterType)
{
return true;
}
```

```
//响应的内容在返回客户端之前，会执行本方法，重写之后在返回
@Override
public Object beforeBodyWrite(Object body, MethodParameter returnType,
MediaType selectedContentType, Class selectedConverterType,
ServerHttpRequest request, ServerHttpResponse response) {
//构造一个要重写给客户端的统一数据格式
Map<String, Object> map = new HashMap<>();
map.put("success", true);
map.put("data", body);
//如果控制器方法返回类型为字符串，响应的Content-Type为text/plain，手动设置为
json，并重写为序列化后的json字符串
if(body instanceof String){
try {
response.getHeaders().setContentType(MediaType.APPLICATION_JSON);
return objectMapper.writeValueAsString(map);
} catch (JsonProcessingException e) {
throw new RuntimeException("json序列化失败");
}
}
return map;
}
}
```

