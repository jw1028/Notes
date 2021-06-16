@[TOC](SpringBoot)
# 为什么要使用SpringBoot
SpringBoot对上述Spring的缺点进行的改善和优化，基于约定优于配置的思想，可以让开发人员不必在配置与逻辑业务之间进行思维的切换，全身心的投入到逻辑业务的代码编写中，从而大大提高了开发的
效率，一定程度上缩短了项目周期。
# SpringBoot的特点

 - 为基于Spring的开发提供更快的入门体验
 - 开箱即用，没有代码生成，也无需XML配置。同时也可以修改默认值来满足特定的需求
 - 提供了一些大型项目中常见的非功能性特性，如嵌入式服务器、安全、指标，健康检测、外部配置等
 - SpringBoot不是对Spring功能上的增强，而是提供了一种快速使用Spring的方式

# 搭建SpringBoot项目
## 方式一：官网创建
访问 [ https://start.spring.io/](https://start.spring.io/) 创建，如下图所示：

![在这里插入图片描述](https://img-blog.csdnimg.cn/20210611204557865.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQ1NjYxMTI1,size_16,color_FFFFFF,t_70)


点击 **GENERATE** 生成并下载项目压缩包。下载完成后解压 该项目文件，使用 IDEA 打开即可。
## 方式二：IDEA创建
![在这里插入图片描述](https://img-blog.csdnimg.cn/20210611204624924.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQ1NjYxMTI1,size_16,color_FFFFFF,t_70)
![在这里插入图片描述](https://img-blog.csdnimg.cn/20210611204633533.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQ1NjYxMTI1,size_16,color_FFFFFF,t_70)
![在这里插入图片描述](https://img-blog.csdnimg.cn/20210611204640389.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQ1NjYxMTI1,size_16,color_FFFFFF,t_70)

## 方式一：普通Maven项目创建
本身SpringBoot就是一个Maven项目，以上工具的方式，只是生成了一些默认的内容，如以下项目结构为工具生成（我们自己手动创建文件夹即可）：
![在这里插入图片描述](https://img-blog.csdnimg.cn/20210611204741257.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQ1NjYxMTI1,size_16,color_FFFFFF,t_70)
以上部分，<code>pom.xml根据需要的依赖包设置(需要我们自己导依赖的）</code>，其他自己手动生成也可以的，所以不用纠结非要使用工具。

需要注意的是，SpringBoot引入的是内嵌式服务器Tomcat9.0.39，该版本的Tomcat内嵌服务器，在启动时为了提高性能会加载本地库（需要下载该库文件），并且会使用 JDK9 以上版本的API，在启动就会报错（抛异常），虽然不影响使用，但是体验总归不太好。可以改用另一种服务器，**Undertow**，该 Web服务器是红帽公司（RedHat）采用 Java 开发的灵活的高性能 Web 服务器，它具有如下特性：

 - 1.完全内嵌式的Web服务器，直接使用 API 就可以启动一个 Web 服务器。
 - 2.完全兼容 Java EE Servlet 4 和低级非堵塞的处理器。
 - 3.提供包括阻塞和基于 NIO 的非堵塞机制。
在高并发请求的系统中，从性能测试的对比数据上看，Undertow 比 Tomcat 在内存和性能的表现更优，目前很多使用 SpringBoot 的项目都将默认内嵌的 Tomcat 服务器更换为了 Undertow。
在SpringBoot中更换 Web 服务器非常方便，只需要调整 Maven 依赖，移除默认内嵌的 Tomcat 服务器，加入 Undertow 服务器即可，而使用上和 Tomcat 没什么不同。

pom.xml内容如下：

```cpp
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <!-- 默认使用的Spring Framework版本为5.2.10.RELEASE -->
    <parent>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-parent</artifactId>
        <version>2.3.5.RELEASE</version>
        <relativePath/> <!-- lookup parent from repository -->
    </parent>
    <groupId>org.example</groupId>
    <artifactId>springboot-study</artifactId>
    <version>1.0-SNAPSHOT</version>

    <properties>
        <java.version>1.8</java.version>
    </properties>

    <dependencies>

        <!-- spring-boot-starter-web: 基于SpringBoot开发的依赖包，
                                 会再次依赖spring-framework中基本依赖包，aop相关依赖包，web相关依赖包，
                                 还会引入其他如json，tomcat，validation等依赖 -->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
            <!-- 排除tomcat依赖 -->
            <exclusions>
                <exclusion>
                    <groupId>org.springframework.boot</groupId>
                    <artifactId>spring-boot-starter-tomcat</artifactId>
                </exclusion>
            </exclusions>
        </dependency>

        <!-- 添加 Undertow 依赖 -->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-undertow</artifactId>
        </dependency>

        <!--引入AOP依赖-->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-aop</artifactId>
        </dependency>

        <!-- spring-boot-devtools: SpringBoot的热部署依赖包 -->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-devtools</artifactId>
            <scope>runtime</scope>
            <!-- 不能被其它模块继承，如果多个子模块可以去掉 -->
            <optional>true</optional>
        </dependency>

        <!-- lombok: 简化bean代码的框架 -->
        <dependency>
            <groupId>org.projectlombok</groupId>
            <artifactId>lombok</artifactId>
            <optional>true</optional>
        </dependency>

        <!-- spring-boot-starter-test: SpringBoot测试框架 -->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-test</artifactId>
            <scope>test</scope>
            <exclusions>
                <exclusion>
                    <groupId>org.junit.vintage</groupId>
                    <artifactId>junit-vintage-engine</artifactId>
                </exclusion>
            </exclusions>
        </dependency>
    </dependencies>

    <build>
        <plugins>
            <!-- SpringBoot的maven打包插件 -->
            <plugin>
                <groupId>org.springframework.boot</groupId>
                <artifactId>spring-boot-maven-plugin</artifactId>
            </plugin>
            <!-- 明确指定一些插件的版本，以免受到 maven 版本的影响 -->
            <plugin>
                <artifactId>maven-clean-plugin</artifactId>
                <version>3.1.0</version>
            </plugin>
            <plugin>
                <artifactId>maven-compiler-plugin</artifactId>
                <version>3.8.1</version>
            </plugin>
            <plugin>
                <artifactId>maven-deploy-plugin</artifactId>
                <version>2.8.2</version>
            </plugin>
            <plugin>
                <artifactId>maven-install-plugin</artifactId>
                <version>2.5.2</version>
            </plugin>
            <plugin>
                <artifactId>maven-jar-plugin</artifactId>
                <version>3.2.0</version>
            </plugin>
            <plugin>
                <artifactId>maven-resources-plugin</artifactId>
                <version>3.1.0</version>
            </plugin>
            <plugin>
                <artifactId>maven-site-plugin</artifactId>
                <version>3.3</version>
            </plugin>
            <plugin>
                <artifactId>maven-surefire-plugin</artifactId>
                <version>2.22.2</version>
            </plugin>

        </plugins>
    </build>

</project>
```

# 基于SpringBoot项目的Web开发说明
## 嵌入式的Web服务器
SpringBoot 已经集成了 Tomcat，以后就不用像传统 Web 开发那样还需要下载一个 Tomcat 程序，配置启动了。只需要启动生成的启动类即可。
## 默认的Web资源文件夹
SpringBoot 默认会使用 **src/main/resources** 目录下的如下文件夹作为Web资源文件夹：

 - 1.**/static**：静态资源文件夹，如html，js，css等存放
 - 2.**/public**：静态资源文件夹，同上
 - 3.**/templates**：模版资源文件夹（后端模版框架使用的模版文件，会解析变量后再生成动态 html）

注：<code>在以上路径中的资源，服务路径不需要在前再加/static，/public。</code>如在 static 文件夹下的home.html ，服务路径为：/home.html(直接输入/home.html即可不需要加/static）

如果是使用普通Maven项目搭建，可以自行创建以上文件夹，在 src/main/resources 下创建public 和 static 文件夹即可。

## 默认的配置文件
SpringBoot默认使用src/main/resource/application.properties 作为启动的配置文件，可以自定义如启动端口等等配置。

如果是使用普通Maven项目搭建，在 src/main/resources 下创建 application.properties 内容为空即可（可以自己根据需要添加一些内容例如tomcat启动端口，数据库连接设置）。
## 默认的应用上下文路径
SpringBoot启动的Web项目，应用上下文路径默认为 /

## 启动类
如果是使用普通Maven项目搭建，可以自行编写启动类：类上使用 **@SpringBootApplication** 注解：

```cpp
package org.example;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

//SpringBoot启动类注解
@SpringBootApplication
public class Application {

    public static void main(String[] args) {
        // 注意第一个参数是当前类的类对象
        SpringApplication.run(Application.class, args);
    }
}
```
需要修改的配置如下：
![在这里插入图片描述](https://img-blog.csdnimg.cn/20210611205941840.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQ1NjYxMTI1,size_16,color_FFFFFF,t_70)
![在这里插入图片描述](https://img-blog.csdnimg.cn/2021061121000130.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQ1NjYxMTI1,size_16,color_FFFFFF,t_70)

## 验证Web静态资源

 - 在 src/main/resources 下的 static 或 public 目录中，创建 html 网页并访问。

![在这里插入图片描述](https://img-blog.csdnimg.cn/20210611210146624.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQ1NjYxMTI1,size_16,color_FFFFFF,t_70)

 - 启动Application启动类
 - 访问index.html
![在这里插入图片描述](https://img-blog.csdnimg.cn/20210611210415243.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQ1NjYxMTI1,size_16,color_FFFFFF,t_70)
