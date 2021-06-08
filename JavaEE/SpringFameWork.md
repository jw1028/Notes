@[TOC](Spring Framework)
# 为什么要使用Spring?
对于 Java 编程来说，使用 Spring 能完成的更加快速，更容易并更安全。Spring 专注于速度，便捷与开发效率，也正是如此，让Spring成为了全世界最流行的 Java 框架。
Spring Framework 属于其中最基础，最核心的部分，Spring下的其他大部分框架都依赖 Spring Framework 。
# 子模块简介
官网给出了一张Spring4.x的结构图。目前最新的5.x版本中Web模块的Portlet组件已经被废弃掉，同时    增加了用于异步响应式处理的WebFlux组件。
![在这里插入图片描述](https://img-blog.csdnimg.cn/20210606233302242.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQ1NjYxMTI1,size_16,color_FFFFFF,t_70)
对于整个Spring Framework来说，是学习、使用Spring生态项目（如Spring Boot、Spring Cloud等）的基石。也就是说，我们要引入其他Spring项目作为我们的依赖框架时，也会使用Spring Framework。
以上子模块包括的内容我们只学习其中最重要的三个部分：**Core Container、AOP、WebMVC**
## Core Container（核心容器）
本模块由 spring-core , spring-beans , spring-context , spring-context-support , and spring- expression 4 个模块组成。
其中spring-core 和 spring-beans 模块，这两个模块提供了整个Spring框架最基础的设施：IoC (Inversion of Control，控制反转) 和 DI (Dependency Injection，依赖注入)。
### IoC
**IoC (Inversion of Control，控制反转)** ，是面向对象编程中的一种设计原则，可以用来减低计算机代码之间的耦合度。只是因为该理论时间成熟相对较晚，并没有包含在GoF中。
系统中通过引入实现了IoC模式的IoC容器，即可由IoC容器来管理对象的生命周期、依赖关系等，从而使得应用程序的配置和依赖性规范与实际的应用程序代码分离。
从使用上看，以前手动new对象，并设置对象中属性的方式，控制权是掌握在应用程序自身。现在则全部转移到了容器，由容器来统一进行管理对象。因为控制权发生了扭转，所以叫**控制反转。**
实现了IoC思想的容器就是IoC容器，比如：SpringFremework.
### DI
**DI (Dependency Injection，依赖注入)** 是实现IoC的方法之一。所谓依赖注入，就是由**IOC容器在运行期间，动态地将某种依赖关系注入到对象之中。**
所以，依赖注入（DI）和控制反转（IoC）是从不同的角度的描述的同一件事情，就是指通过引入 IoC 容器，利用依赖关系注入的方式，实现对象之间的解耦。

# Spring容器使用流程
Spring容器的API有 **BeanFactory 和 ApplicationContext** 两大类，他们都是顶级接口。其中ApplicationContext 是 BeanFactory 的子接口。我们主要使用 ApplicationContext 应用上下文接口。
![在这里插入图片描述](https://img-blog.csdnimg.cn/20210607234513312.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQ1NjYxMTI1,size_16,color_FFFFFF,t_70)
# 开发步骤
## 准备Maven项目及环境

 - maven配置文件 pom.xml ；

```cpp
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <groupId>org.example</groupId>
    <artifactId>spring-study</artifactId>
    <version>1.0-SNAPSHOT</version>

    <properties>
        <java.version>1.8</java.version>
        <maven.compiler.source>${java.version}</maven.compiler.source>
        <maven.compiler.target>${java.version}</maven.compiler.target>
        <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
        <spring-framework.version>5.2.10.RELEASE</spring-framework.version>
    </properties>

    <dependencies>
        <dependency>
            <groupId>org.springframework</groupId>
            <artifactId>spring-beans</artifactId>
            <version>${spring-framework.version}</version>
        </dependency>
        <dependency>
            <groupId>org.springframework</groupId>
            <artifactId>spring-context</artifactId>
            <version>${spring-framework.version}</version>
        </dependency>

        <dependency>
            <groupId>org.projectlombok</groupId>
            <artifactId>lombok</artifactId>
            <version>1.18.16</version>
        </dependency>
    </dependencies>

    <build>
        <plugins>
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
配置完成记得要刷新下maven面板哦

 - 准备启动入口类
 
之后就可以使用Spring框架了，Spring提供了通过xml配置文件，来定义Bean，但是定义Bean的方式需    要通过包扫描的方式注册到容器中（其实还有其他方式，我们这里主要只掌握包扫描的方式）

写一个入口类：

```cpp
package org.example;

import org.springframework.context.ApplicationContext;
import org.springframework.context.support.ClassPathXmlApplicationContext;

public class App {

    public static void main(String[] args) {
        //根据Spring配置文件路径创建容器：应用上下文对象
        ApplicationContext context = new ClassPathXmlApplicationContext("beans.xml");
        //关闭容器
        ((ClassPathXmlApplicationContext) context).close();
    }
}
```

 - 准备Spring配置文件

定义需要加载的Bean配置文件，在src/main/resources下，创建beans.xml文件：

```cpp
<?xml version="1.0" encoding="UTF-8"?>

-<beans xsi:schemaLocation="http://www.springframework.org/schema/beans https://www.springframework.org/schema/beans/spring-beans.xsd http://www.springframework.org/schema/context https://www.springframework.org/schema/context/spring-context.xsd" xmlns:context="http://www.springframework.org/schema/context" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://www.springframework.org/schema/beans">

<context:component-scan base-package="org.example"/>

</beans>
```
## 初始化/注册Bean
### 方式一：类注解
在类上使用注解 @Controller ， @Service ， @Repository ， @Component 。需要保证该类会被Spring 扫描到，这种定义方式默认会注册一个名称为类名首字母小写的Bean对象到容器中。以下定义一个模拟数据库操作的类org.example.dao.LoginRepository @Repository 注解会注册名称为loginRepository的对象到容器中：

```cpp
package org.example.dao;
import org.example.model.User;
import org.springframework.stereotype.Repository;

@Repository
public class LoginRepository {
}
```
定义好了Bean对象，注册到容器中以后，就可以获取Bean对象了，在入口类org。example.APP中，可以通过	AplicattionContext对象获取Bean，有两种方式获取：

 - 通过类型获取：这种获取方式要求该类型的Bean只能有一个
 - 通过名称获取：同一个类型的Bean可以有多个

```cpp
package org.example;

import org.example.dao.LoginRepository;
import org.springframework.context.ApplicationContext;
import org.springframework.context.support.ClassPathXmlApplicationContext;

public class App {

public static void main(String[] args) {
//根据Spring配置文件路径创建容器：应用上下文对象ApplicationContext context = new
ClassPathXmlApplicationContext("beans.xml"); LoginRepository loginRepository1 = (LoginRepository)
context.getBean("loginRepository"); LoginRepository loginRepository2 =
context.getBean(LoginRepository.class); System.out.printf("loginRepository: %s%n", loginRepository1 ==
loginRepository2);
//关闭容器
((ClassPathXmlApplicationContext) context).close();
}
}
```

### 方式二：@Bean
当前类被 Spring 扫描到时，可以在方法上使用@Bean注解，通过方法返回类型，也可以定义、注册Bean对象，默认使用方法名作为Bean的名称。

先定义一个用户类 org.example.model.User ，注意这里没有使用任何Spring的注解，类不会被扫描到

```cpp
package org.example.model

import lombok.Getter; import lombok.Setter; import lombok.ToString;

@Getter 
@Setter 
@ToString
public class User {
private String username; private String password;
}
```
在loginController	中定义两个用户类：

```cpp
@Bean
public User user1(){
User user = new User(); user.setUsername("abc"); user.setPassword("123"); return user;
}
@Bean
public User user2(){
User user = new User(); user.setUsername("我不是汤神"); user.setPassword("tang"); return user;
}
```

 - 注入指定的Bean：**@Qualifier**
 
同类型的Bean有多个时，注入该类型Bean需要指定Bean的名称：
 - 属性名或方法参数名设置为Bean的名称
 - 属性名或方法参数设置 @Qualifier("名称") 注解，注解内的字符串是Bean对象的名称

以下 **loginController** 中定义了5个用户对象，且在方法参数中注入了Bean对象

```cpp
package org.example.controller;
import org.example.model.User;
import org.example.service.LoginService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.context.annotation.Bean;
import org.springframework.stereotype.Controller;
@Controller
public class LoginController {
    @Autowired
    private LoginService loginService;
    @Autowired
    @Qualifier("user1")
    private User u;
    @Autowired
    private User user1;
    @Bean
    public User user1(){
        User user = new User();
        user.setUsername("abc");
        user.setPassword("123");
        return user;
   }
    @Bean
    public User user2(){
        User user = new User();
        user.setUsername("我不是汤神");
        user.setPassword("tang");
        return user;
   }
    @Bean
    public User user3(LoginService loginService){
        System.out.printf("user3: %s%n", loginService == this.loginService);
        return new User();
   }
    @Bean
    public User user4(User user1){
        System.out.printf("user4: user1=%s%n", user1);
        return new User();
   }
    @Bean
    public User user5(@Qualifier("user2") User u){
        System.out.printf("user5: user2=%s%n", u);
        return new User();
   }
}
```

### 方式三：@Configuration
在类被Spring扫描到时，使用@configuration	注解，可以注册一个配置类到容器中。配置类一般用来自定义配置某些资源。之后会在SpringMVC中用到。
### 方式四：FactoryBean接口
FactoryBean接口实现如下：
![在这里插入图片描述](https://img-blog.csdnimg.cn/20210608000426323.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQ1NjYxMTI1,size_16,color_FFFFFF,t_70)
FactoryBean以Bean结尾，表示它是一个Bean，不同于普通Bean的是：实现了FactoryBean<T>接口的Bean，根据该Bean的ID从容器中获取的实际上是FactoryBean的getObject()返回的对象，而不是FactoryBean本身，如果要获取FactoryBean对象，请在id前面加一个&符号来获取。
示例：如下先定义一个Bean，实现FactoryBean接口，指定泛型为User类，会将getObject方法的返回对象注册到容器中。

```cpp
package org.example.model;

import org.springframework.beans.factory.FactoryBean;
import org.springframework.stereotype.Component;

@Component
public class ByFactoryBean implements FactoryBean<User> { @Override
public User getObject() throws Exception { User user = new User(); user.setUsername("abc"); user.setPassword("123");
return user;
}
@Override
public Class<?> getObjectType() { return User.class;
}
}
```
在org.example.App获取该Bean对象：

```cpp
1User user = (User) context.getBean("byFactoryBean");
System.out.printf("get bean by FactoryBean: %s%n", user);
```
因为已经定义过User对象了，所以只能通过 id 获取，通过类型获取会报错。

## 依赖注入（依赖装配）
### 属性注入

 - **@Autowrid**

当前类被 Spring 扫描到时，可以在属性上使用**@Autowrid**注解，会将容器中的Bean对象装配进来。

```cpp
package org.example.service;
import org.example.dao.LoginRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
@Service
public class LoginService {
    @Autowired
    private LoginRepository loginRepository; }
```

也可以在setter方法上使用@Autowrid注解：
说明：其实只要写在方法上的	@Autowrid注解，都会将容器中的Bean对象注入方法参数，setter注入本质也是这样，只是setter方法一般都是设置属性用的，所以也归到属性注入。

```cpp
package org.example.service;
import org.example.dao.LoginRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
@Service
public class LoginServiceBySetter {
    private LoginRepository loginRepository;
    public LoginRepository getLoginRepository() {
        return loginRepository;
   }
    @Autowired
    public void setLoginRepository(LoginRepository loginRepository) {
        System.out.printf("LoginServiceBySetter: loginRepository=%s%n", 
loginRepository);
        this.loginRepository = loginRepository;
   }
}
```

### 构造方法注入
当前类被 Spring 扫描到时，可以在构造方法上使用@Autowrid注解，作用和setter类似，会将容器中的Bean对象注入方法参数。

```cpp
package org.example.service;
import org.example.dao.LoginRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
@Service
public class LoginServiceByConstructor {
    private LoginRepository loginRepository;
    @Autowired
    public LoginServiceByConstructor(LoginRepository loginRepository){
        System.out.printf("LoginServiceByConstructor: %s%n", 
loginRepository);
        this.loginRepository = loginRepository;
   }
 }
```
## Bean的作用域
Spring 容器在初始化一个 Bean 的实例时，同时会指定该实例的作用域。Spring有6个作用域，最后四种是基于Spring WebMVC生效

 - singleton
 - prototype
 - request
 - session
 - application（了解）
 - websocket（了解）
## Bean的生命周期
生命周期概览
![在这里插入图片描述](https://img-blog.csdnimg.cn/20210608001932454.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQ1NjYxMTI1,size_16,color_FFFFFF,t_70)
Spring容器中Bean的生命周期，类似于流水线上制造一辆汽车，一台电脑，将繁多的工序流水线化、流程化以后，才可以方便的管理，如生产电脑经历了组装CPU，主板，显卡等等工序，需要在安装CPU以前检查是否有美国的监听器，就可以方便的到具体的流水线上某个点执行。Bean对象生命周期也是如此。

**总结**
对于Bean的生命周期，主要步骤为：
1. 实例化Bean：通过反射调用构造方法实例化对象。
2. 依赖注入：装配Bean的属性
3. 实现了Aware接口的Bean，执行接口方法：如顺序执行BeanNameAware、BeanFactoryAware、
ApplicationContextAware的接口方法。
4. Bean对象初始化前，循环调用实现了BeanPostProcessor接口的预初始化方法
（postProcessBeforeInitialization）
5. Bean对象初始化：顺序执行@PostConstruct注解方法、InitializingBean接口方法、init-method
方法
6. Bean对象初始化后，循环调用实现了BeanPostProcessor接口的后初始化方法
（postProcessAfterInitialization）
7. 容器关闭时，执行Bean对象的销毁方法，顺序是：@PreDestroy注解方法、DisposableBean接口
方法、destroy-method

补充说明：第一步的实例化是指new对象，Spring的语义中说初始化Bean包含Bean生命周期中的初始
化步骤。

