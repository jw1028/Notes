# Mybatis

## 简介

MyBatis 是一款优秀的持久层框架，它支持自定义 SQL、存储过程以及高级映射。MyBatis 免除了几乎
所有的 JDBC 代码以及设置参数和获取结果集的工作。MyBatis 可以通过简单的 XML 或注解来配置和映
射原始类型、接口和 Java POJO（Plain Old Java Objects，普通老式 Java 对象）为数据库中的记录。


## JDBC操作回顾

## 执行步骤

Java 语言中对于数据库操作的原始方式，即通过 JDBC 来操作数据库，步骤几乎都比较固定，以下为语
法层面的步骤：

```
1 .创建数据库连接池 DataSource
2 .通过 DataSource 获取数据库连接 Connection
3 .编写要执行带? 占位符的 SQL 语句
4 .通过 Connection 及 SQL 创建操作命令对象 Statement
5 .替换占位符：指定要替换的数据库字段类型，占位符索引及要替换的值
6 .使用 Statement 执行 SQL 语句
7 .查询操作：返回结果集 ResultSet，更新操作：返回更新的数量
8 .处理结果集
9 .释放资源
```

## 示例代码

###### 下面的一个完整案例，展示了通过 JDBC 的API向数据库中添加一条记录，修改一条记录，查询一条记录

###### 的操作。

###### -- 创建数据库

```
create database if not exists `library` default character set utf8mb4;
-- 使用数据库
use library;
-- 创建表
create table if not exists `soft_bookrack` (
`book_name` varchar( 32 ) NOT NULL,
`book_author` varchar( 32 ) NOT NULL,
`book_isbn` varchar( 32 ) NOT NULL primary key
) ;
```


```
package com.bittech.jdbc.biz;
```

```
import javax.sql.DataSource;
import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
```



```
public class SimpleJdbcOperation {
```

```
private final DataSource dataSource;
```

```
public SimpleJdbcOperation(DataSource dataSource) {
this.dataSource = dataSource;
}
```

```
/**
* 添加一本书
*/
public void addBook() {
Connection connection = null;
PreparedStatement stmt = null;
try {
//获取数据库连接
connection = dataSource.getConnection();
//创建语句
stmt = connection.prepareStatement(
"insert into soft_bookrack (book_name, book_author,
book_isbn) values (?,?,?);"
);
//参数绑定
stmt.setString( 1 , "Spring in Action");
stmt.setString( 2 , "Craig Walls");
stmt.setString( 3 , "9787115417305");
//执行语句
stmt.execute();
} catch (SQLException e) {
//处理异常信息
} finally {
//清理资源
try {
if (stmt != null) {
stmt.close();
}
if (connection != null) {
connection.close();
}
} catch (SQLException e) {
//
}
}
}
```

```
/**
* 更新一本书
*/
public void updateBook() {
Connection connection = null;
PreparedStatement stmt = null;
try {
//获取数据库连接
connection = dataSource.getConnection();
//创建语句
stmt = connection.prepareStatement(
```

```
"update soft_bookrack set book_author=? where
book_isbn=?;"
);
//参数绑定
stmt.setString( 1 , "张卫滨");
stmt.setString( 2 , "9787115417305");
//执行语句
stmt.execute();
} catch (SQLException e) {
//处理异常信息
} finally {
//清理资源
try {
if (stmt != null) {
stmt.close();
}
if (connection != null) {
connection.close();
}
} catch (SQLException e) {
//
}
}
}
```

```
/**
* 查询一本书
*/
public void queryBook() {
Connection connection = null;
PreparedStatement stmt = null;
ResultSet rs = null;
Book book = null;
try {
//获取数据库连接
connection = dataSource.getConnection();
//创建语句
stmt = connection.prepareStatement(
"select book_name, book_author, book_isbn from
soft_bookrack where book_isbn =?"
);
//参数绑定
stmt.setString( 1 , "9787115417305");
//执行语句
rs = stmt.executeQuery();
if (rs.next()) {
book = new Book();
book.setName(rs.getString("book_name"));
book.setAuthor(rs.getString("book_author"));
book.setIsbn(rs.getString("book_isbn"));
}
System.out.println(book);
} catch (SQLException e) {
//处理异常信息
} finally {
//清理资源
try {
if (rs != null) {
```

### 问题

###### 对于不同业务来说，只有以下部分是不同的：

###### 带占位符的 SQL 语句。

```
要替换占位符的数据：一般使用 基础数据类型或 Java对象，需要明确替换哪个占位符，哪个值来
替换。
如果是查询，一般会将结果集转换为 Java对象。需要提供转换的 Java类型，及与结果集字段的映射
关系。
```

除了以上部分，CRUD 操作类型相同时，如都是查询操作，其他的代码都是类似的样板代码。包括：

```
创建同一个数据库连接池 DataSource
获取数据库连接 Connection
根据 业务SQL 创建操作命令对象 Statement
根据 业务要替换的数据 替换占位符
执行 SQL
处理查询结果集 ResultSet：根据 业务要映射的 Java类型 ，将结果集 ResultSet 的字段转换为
Java对象或对象中的属性。
处理异常
释放资源
```

可以看出少量的代码真正用于业务功能，大部分的代码都是样板代码。不过，这些样板代码非常重要，
清理资源和处理错误确保了数据访问的健壮性，避免了资源的泄露。

### 解决方案

###### 要解决以上问题，有以下方案：

###### 1. 最简单的，涉及工具类提供统一的功能：获取数据库连接，释放资源。

###### 2. 使用模版设计模式，父类的模板方法提供统一的逻辑，子类提供不同实现。但这部分统一代码逻辑

###### 都会比较复杂。

###### 3. 更进一步的考虑，其实可以通过 AOP 技术，自动的生成代理类，代理类的方法中织入了统一的样

###### 板代码。

```
rs.close();
}
if (stmt != null) {
stmt.close();
}
if (connection != null) {
connection.close();
}
} catch (SQLException e) {
//
}
}
}
```

```
public static class Book {
private String name;
private String author;
private String isbn;
//省略 setter getter 方法
}
}
```



###### 基于上面的原因，我们才需要使用框架：框架会采用第三种解决方案，自动的生成样板代码，我们只需

要提供 sql，要替换占位符的数据，返回结果集要转换的 java 类型。

以下为框架提供的功能：

##### 要执行的 SQL （一般是要替换占位符的数据Java对象）

##### 执行SQL

##### （框架提供）

##### 返回更新数量 返回结果集

##### 处理结果集

##### （一般转换为 Java对象）

##### 更新操作 查询操作

###### 可以看到，以上两个部分都涉及到对象操作的转换：

```
传入 Java对象，作为 SQL要替换值的输入数据；
查询操作，提供 Java类型作为结果，作为结果集转换的输出数据
```

这种框架一般称为 ORM 框架。

## ORM框架

### ORM简介

ORM（Object Relational Mapping），即对象关系映射。在面向对象编程语言中，将关系型数据库中的
数据与对象建立起映射关系，进而自动的完成数据与对象的互相转换：

1. 将输入数据（即传入对象）+SQL 映射成原生 SQL
2. 将结果集映射为返回对象，即输出对象

ORM 把数据库映射为对象：

```
数据库表（table）--> 类（class）
记录（record，行数据）--> 对象（object）
字段（field） --> 对象的属性（attribute）
```

一般的 ORM 框架，会将数据库模型的每张表都映射为一个 Java 类。


### 常见的 ORM 框架

#### Mybatis

Mybatis是一种典型的半自动的 ORM 框架，所谓的半自动，是因为还需要手动的写 SQL 语句，再由框
架根据 SQL 及 传入数据来组装为要执行的 SQL。其优点为：

1. 因为由程序员自己写 SQL，相对来说学习门槛更低，更容易入门。
2. 更方便做 SQL的性能优化及维护。
3. 对关系型数据库的模型要求不高，这样在做数据库模型调整时，影响不会太大。适合软件需求变更
   比较频繁的系统，因此国内系统大部分都是使用如 Mybatis 这样的半自动 ORM 框架。

其缺陷为：

```
不能跨数据库，因为写的 SQL 可能存在某数据库特有的语法或关键词
```

#### Hibernate

Hibernate是一种典型的全自动 ORM 框架，所谓的全自动，是 SQL 语句都不用在编写，基于框架的
API，可以将对象自动的组装为要执行的 SQL 语句。其优点为：

1. 全自动 ORM 框架，自动的组装为 SQL 语句。
2. 可以跨数据库，框架提供了多套主流数据库的 SQL 生成规则。

其缺点为：

```
学习门槛更高，要学习框架 API 与 SQL 之间的转换关系
对数据库模型依赖非常大，在软件需求变更频繁的系统中，会导致非常难以调整及维护。可能数据
库中随便改一个表或字段的定义，Java代码中要修改几十处。
很难定位问题，也很难进行性能优化：需要精通框架，对数据库模型设计也非常熟悉。
```

## 开发步骤

### 准备Maven项目

首先创建一个Maven项目 mybatis-sudy，在 pom.xml 中引入SpringBoot及Mybatis需要的依赖包，

如下：

```
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
xsi:schemaLocation="http://maven.apache.org/POM/4.0.
http://maven.apache.org/xsd/maven-4.0.0.xsd">
<modelVersion>4.0.0</modelVersion>
```

```
<!-- 默认使用的Spring Framework版本为5.2.10.RELEASE -->
<parent>
<groupId>org.springframework.boot</groupId>
<artifactId>spring-boot-starter-parent</artifactId>
<version>2.3.5.RELEASE</version>
<relativePath/> <!-- lookup parent from repository -->
</parent>
<groupId>org.example</groupId>
<artifactId>mybatis-study</artifactId>
<version>1.0-SNAPSHOT</version>
<properties>
<java.version>1.8</java.version>
```


```
</properties>
```

```
<dependencies>
```

```
<!-- spring-boot-starter-web: 基于SpringBoot开发的依赖包，
会再次依赖spring-framework中基本依赖包，aop相
关依赖包，web相关依赖包，
还会引入其他如json，tomcat，validation等依赖 -
->
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
```

```
<!-- 添加 Undertow 依赖 -->
<dependency>
<groupId>org.springframework.boot</groupId>
<artifactId>spring-boot-starter-undertow</artifactId>
</dependency>
```

```
<!--引入AOP依赖-->
<dependency>
<groupId>org.springframework.boot</groupId>
<artifactId>spring-boot-starter-aop</artifactId>
</dependency>
```

```
<!-- mybatis-spring-boot-starter: Mybatis框架在SpringBoot中集成的依赖
包，
Mybatis是一种数据库对象关系映射Object-Relationl
Mapping（ORM）框架，
其他还有如Hibernate等 -->
<dependency>
<groupId>org.mybatis.spring.boot</groupId>
<artifactId>mybatis-spring-boot-starter</artifactId>
<version>2.1.3</version>
</dependency>
```

```
<!-- Mybatis代码生成工具 -->
<dependency>
<groupId>org.mybatis.generator</groupId>
<artifactId>mybatis-generator-core</artifactId>
<version>1.3.5</version>
</dependency>
```

```
<!-- druid-spring-boot-starter: 阿里Druid数据库连接池，同样的运行时需要
-->
<dependency>
<groupId>com.alibaba</groupId>
<artifactId>druid-spring-boot-starter</artifactId>
<version>1.2.3</version>
</dependency>
```


```
<!-- JDBC：mysql驱动包 -->
<dependency>
<groupId>mysql</groupId>
<artifactId>mysql-connector-java</artifactId>
<version>5.1.49</version>
<scope>runtime</scope>
</dependency>
```

```
<!-- spring-boot-devtools: SpringBoot的热部署依赖包 -->
<dependency>
<groupId>org.springframework.boot</groupId>
<artifactId>spring-boot-devtools</artifactId>
<scope>runtime</scope>
<!-- 不能被其它模块继承，如果多个子模块可以去掉 -->
<optional>true</optional>
</dependency>
```

```
<!-- lombok: 简化bean代码的框架 -->
<dependency>
<groupId>org.projectlombok</groupId>
<artifactId>lombok</artifactId>
<optional>true</optional>
</dependency>
```

```
<!-- spring-boot-starter-test: SpringBoot测试框架 -->
<dependency>
<groupId>org.springframework.boot</groupId>
<artifactId>spring-boot-starter-test</artifactId>
<scope>test</scope>
</dependency>
</dependencies>
```

```
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
```

### 准备数据库

由于Mybatis是数据库操作的框架，所以提前准备好数据库表及数据：随便找个文件，编写初始化
sql。

以下在项目根目录下创建 db 文件夹，并创建一个 init.sql 的文件。内容为课堂博客项目的数据库表

及数据的初始化语句：

```
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
```

```
</plugins>
</build>
```

```
</project>
```


```
drop database if exists mybatis_study;
create database mybatis_study character set utf8mb4;
```

```
use mybatis_study;
```

```
drop table if exists user;
create table user(
id int primary key auto_increment,
username varchar( 20 ) not null unique comment '账号',
password varchar( 20 ) not null comment '密码',
nickname varchar( 20 ) comment '用户昵称',
sex bit default 0 comment '性别，0/false为女，1/true为男',
birthday date comment '生日',
head varchar( 50 ) comment '头像地址',
create_time timestamp default now() comment '创建日期，默认为插入时的日期'
) comment '用户表';
```

```
drop table if exists article;
create table article(
id int primary key auto_increment,
title varchar( 20 ) not null comment '文章标题',
content mediumtext not null comment '文章内容',
view_count int default 0 comment '文章浏览量',
user_id int comment '外键：用户id',
create_time timestamp default now() comment '创建日期，默认为插入时的日期',
foreign key(user_id) references user(id)
) comment '文章表';
```



### 准备SpringBoot启动类

主要包括启动类，随便创建一个包，并在包下创建一个带 @SpringBootApplication 注解的启动类：

### 准备SpringBoot配置文件

准备SpringBoot的默认配置文件，在 src/main/resources 下创建 application.properties 文

件。

由于引入了Mybatis相关依赖包，会根据配置文件 application.properties 的内容自动初始化

Mybatis相关配置类，如果不配置会报错。

在 application.properties 中添加如下内容：

```
insert into user(username, password) values ('a1', '11');
insert into user(username, password) values ('a2', '12');
insert into user(username, password) values ('b', '2');
insert into user(username, password) values ('c', '3');
```

```
insert into article(title, content, user_id) value ('快速排序', 'public ...',
1 );
insert into article(title, content, user_id) value ('冒泡排序', 'private
...', 1 );
insert into article(title, content, user_id) value ('选择排序', 'private
...', 1 );
insert into article(title, content, user_id) value ('归并排序', 'public ...',
2 );
insert into article(title, content, user_id) value ('插入排序', 'protected
...', 2 );
insert into article(title, content, user_id) value ('希尔排序', 'protected
...', 3 );
insert into article(title, content, user_id) value ('List', 'public ...',
4 );
insert into article(title, content, user_id) value ('Set', 'public ...', 4 );
insert into article(title, content, user_id) value ('Map', 'public ...', 4 );
```


```
package org.example;
```

```
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
```

```
@SpringBootApplication
public class Application {
```

```
public static void main(String[] args) {
SpringApplication.run(Application.class, args);
}
}
```


```
#debug=true
# 设置打印日志的级别，及打印sql语句
#日志级别：trace,debug,info,warn,error
#基本日志
logging.level.root=INFO
#扫描的包并按debug日志级别打印：druid.sql.Statement类和org.example包
logging.level.druid.sql.Statement=DEBUG
```



以上 mybatis.mapper-locations 指定了Mybatis的映射文件路径，在 classpath 路径的 mapper文件

夹下，所有以 Mapper结尾的 xml 文件。这些映射文件我们会在之后创建。

### 验证以上配置

配置好了以后，运行SpringBoot启动类，不出现报错即可。

### Mybatis开发

以上环境准备好了，就可以进行Mybatis开发了，对于Mybatis的使用，其实都是对之前所说几块内容的
开发，对照之前的图：

##### 要执行的 SQL （一般是要替换占位符的数据Java对象）

##### 执行SQL

##### （框架提供）

##### 返回更新数量 返回结果集

##### 处理结果集

##### （一般转换为 Java对象）

##### 更新操作 查询操作

###### 主要包括以下几个部分：

```
logging.level.org.example=DEBUG
```

```
#数据库连接池配置：
spring.datasource.url=jdbc:mysql://localhost:3306/mybatis_study?
useUnicode=true&characterEncoding=UTF-8&useSSL=false
spring.datasource.username=root
spring.datasource.password= 123456
```

```
#指定Mybatis表和实体映射关系xml配置文件，包含表与实体的映射，字段和属性的映射，及各个sql
语句
mybatis.mapper-locations=classpath:mapper/**Mapper.xml
```


#### Java实体类

需要根据数据库表建立 Java类，表中的每个字段需要对应类中的属性。之后会在 Mybatis 的映射文件中
配置字段与属性的映射关系。请大家自行完成这部分代码。可以参考以前的课堂博客项目。

这部分实体类对象，对应以上图中绿色的两个部分，一般会以如下方式呈现：

1. 作为传入数据，表现在方法参数上。
2. 作为结果集转换的输出数据，表现在方法的返回值上。

#### 配置Mybatis数据操作Mapper接口

###### 这部分对应以上图中淡黄色的部分：由开发人员提供执行SQL的接口，框架会自动为接口生成代理类，

###### 代理类中会包含模版方法的代码逻辑。

本部分会将几个部件都组织起来： **sql语句** ， **传入要替换占位符的数据** ，及 **查询结果集的返回类型** 。

在接口上可以指定后边两个，sql会在下一个Mybatis实体映射文件中配置。

注意接口需要使用注解 @Mapper 及 @Component。在SpringBoot启动后，SpringBoot会自动扫描到启
动类包下的注解类，且Mybatis框架会进一步完成生成代理类的工作。

实际上，官方对此有两种方式配置，可以参考Mybatis在SpringBoot中的配置

以下为 org.example.mapper 包下创建的文章类的 Mybatis 映射 Mapper 接口：

#### 配置Mybatis实体映射文件

映射文件是xml文件，且在 application.properties 中指定了路径，是在

classpath:mapper/**Mapper.xml，该路径是在类加载路径下的mapper文件夹下，所有以
Mapper.xml 结尾的文件。

所以可以在 src/main/resources 下新建 mapper 文件夹，并创建文章类的映射文件

```
ArticleMapper.xml。
```

对于映射文件的配置可以参考官方文档 Mybatis入门。

一般前面部分格式都是固定的，如下：

```
package org.example.mapper;
```

```
import org.apache.ibatis.annotations.Mapper;
import org.example.model.Article;
import org.springframework.stereotype.Component;
```

```
@Mapper
@Component
public interface ArticleMapper {
```

```
Article selectById(Integer id);
}
```


###### 以下是对以上标签的说明：

```
<mapper>标签：需要指定 namespace 属性，表示命名空间，值为 mapper 接口的全限定名，包
括全包名.类名
<resultMap>标签：配置查询结果集与 Java 类的映射关系，包括如下配置：
```

1. id 绑定该映射的键，之后可以通过 id 值来使用。在本命名空间使用可以直接使用，其他命
   名空间需要以 命名空间.resultMap的id 的方式来使用。之后的部分会进一步使用。这里先大
   概介绍。
2. type 绑定该结果集映射的 Java 类。
3. <id>标签指定结果集的唯一标识，一般为数据库主键。
4. <result>标签指定结果集字段与 Java 类中属性的映射，其中 column 指定结果集字段，
   property 指定 Java 属性。

以下为文章接口的 xml 映射配置 ArticleMapper.xml：

#### 配置SQL

之后还需要在 Mybatis 映射文件中配置 SQL，需要配置在<mapper>标签下，与<resultMap>标签同
级，详细配置可以参考官方文档 Mybatis映射文件。

我们之前已经完成的文章接口，还需要配置接口对应要执行 SQL，对 CRUD 操作来说，每个不同类型的
操作都有对应的标签：

```
<select>标签：查询语句
<insert>标签：插入语句
<update>标签：修改语句
<delete>标签：删除语句
```

```
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE mapper PUBLIC "-//mybatis.org//DTD Mapper 3.0//EN"
"http://mybatis.org/dtd/mybatis-3-mapper.dtd">
<mapper namespace="{关联的mapper接口全限定名}">
<resultMap id="{结果集映射id}" type="{Java实体类}">
<id column="{结果集唯一标识}" property="{实体类属性}" />
<result column="{结果集字段1}" property="{实体类属性}" />
<result column="{结果集字段2}" property="{实体类属性}" />
</resultMap>
```

```
</mapper>
```


```
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE mapper PUBLIC "-//mybatis.org//DTD Mapper 3.0//EN"
"http://mybatis.org/dtd/mybatis-3-mapper.dtd">
<mapper namespace="org.example.mapper.ArticleMapper">
<resultMap id="BaseResultMap" type="org.example.model.Article">
<id column="id" property="id" />
<result column="title" property="title" />
<result column="content" property="content" />
<result column="view_count" property="viewCount" />
<result column="user_id" property="userId" />
<result column="create_time" property="createTime" />
</resultMap>
```

```
</mapper>
```



###### 以上标签在使用上有如下相同的配置：

1. 都必须指定 id 属性，该属性会绑定 mapper 接口方法，值和方法名相同。本质上 Mybatis 是根
   据 **mapper包名** 查找对应的命名空间，之后在调用方法时，在该命名空间下根据 **接口方法名** 查找
   对应 id 的 sql。以下为文章 selectById 查询方法的 sql 配置：

```
以上可以看到，首先指定了<select>查询标签，并指定 id 属性绑定 mapper 中叫 selectById
的方法
```

2. 使用 parameterType 指定传入数据的类型，该配置只能在mapper接口方法参数只有一个时使
   用，也可以省略。如果有多个方法参数，需要另行设置，后续会讲。
3. 查询语句可以使用 resultMap 属性绑定结果集映射，值为结果集映射的 id。注意返回结果集有
   一行和多行数据时，都可以使用 resultMap 绑定映射，对应接口方法的返回值是一个对象（结果
   集为一行），或 List<类型>（结果集为多行）
4. 对插入，修改，删除这样的更新操作来说，返回的值都是 int，表示更新成功的数量，所以不用指
   定 resultMap。
5. 传入数据可以在 sql 语句中使用 #{方法参数名} 的方式获取。

#### 单元测试

可以在SpringBoot中方便的使用 JUnit 来完成单元测试，在 src/test/java 中，创建以下单元测试

类：

```
<select id="selectById" parameterType="java.lang.Integer"
resultMap="BaseResultMap">
select * from article where id=#{id}
</select>
```

```
package test.example.mapper;
```

```
import org.example.model.Article;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.junit4.SpringRunner;
```

```
//指定为Spring环境中的单元测试
@RunWith(SpringRunner.class)
//指定为SpringBoot环境的单元测试，Application为启动类
@SpringBootTest(classes = Application.class)
//使用事务，在SpringBoot的单元测试中会自动回滚
@Transactional
public class ArticleMapperTest {
```

```
@Autowired
private ArticleMapper articleMapper;
```

```
@Test
public void selectById(){
Article article = articleMapper.selectById( 1 );
System.out.println(article);
}
```

```
}
```



###### 以上正确配置可以通过并打印出文章信息：

#### 插入操作示例

###### 以下演示了如何向文章表中新增一条文章。

###### 首先在接口中定义映射方法：

之后在 ArticleMapper.xml 映射文件中，配置 sql，更新操作只需要指定传入参数，如下：

要注意 #{参数} 是引用传入 Article 对象中的属性，不是数据库字段

单元测试代码：

```
2020-12-17 17:55:13.835 DEBUG 12212 --- [ main]
o.e.mapper.ArticleMapper.selectById : ==> Preparing: select * from
article where id=?
2020-12-17 17:55:13.850 DEBUG 12212 --- [ main]
o.e.mapper.ArticleMapper.selectById : ==> Parameters: 1(Integer)
2020-12-17 17:55:13.860 DEBUG 12212 --- [ main]
o.e.mapper.ArticleMapper.selectById : <== Total: 1
Article(id=1, title=快速排序, content=public ..., viewCount=0, userId=1,
createTime=Thu Dec 17 17:54:16 CST 2020, user=null)
```


```
package org.example.mapper;
```

```
import org.apache.ibatis.annotations.Mapper;
import org.example.model.Article;
import org.springframework.stereotype.Component;
```

```
@Mapper
@Component
public interface ArticleMapper {
```

```
Article selectById(Integer id);
```

```
int insert(Article article);
}
```


```
<insert id="insert" parameterType="org.example.model.Article">
insert into article(title, content, user_id) values
(
#{title},
#{content},
#{userId}
)
</insert>
```


###### 可以看到测试执行后数据库插入文章数据成功，但自增的主键没有返回：

### 课堂练习

###### 请大家自行完成以下操作：

1. 根据用户 id 查询一个用户的信息。
2. 根据用户 id 查询关联的所有文章信息。
3. 查询用户名以 a 开头的用户信息，要求方法参数分别为 String 和 User 类两种方式实现。
4. 新增一条用户，用户名为 d，密码为 4 ，用户昵称为 滴滴，生日为 1998 - 02 - 18 。
5. 将 id=2 的文章内容修改为 public static void main(String[] args){}。
6. 删除用户名为 c 的用户关联的所有文章。
   注：MySQL中的关联删除语法为：

## Mybatis进阶

### 多个方法参数

当接收多个方法参数时，xml 映射文件中的 sql 配置不能再使用 parameterType 属性，需要在方法参

数上使用 @Param("参数的名称")，之后在 sql 中使用 #{参数的名称} 的方式来替换占位符。

示例：查询文章标题包含 排序，且文章内容包含 public 的所有文章信息。

ArticleMapper中的方法定义：

```
@Test
public void insert(){
Article article = new Article();
article.setTitle("测试一下");
article.setContent("看看对不对哇");
article.setUserId( 4 );
int n = articleMapper.insert(article);
System.out.println(article);
}
```


```
2020-12-17 17:54:23.580 DEBUG 16472 --- [ main]
org.example.mapper.ArticleMapper.insert : ==> Preparing: insert into
article(title, content, user_id) values ( ?, ?,? )
2020-12-17 17:54:23.598 DEBUG 16472 --- [ main]
org.example.mapper.ArticleMapper.insert : ==> Parameters: 测试一下(String), 看
看对不对哇(String), 4(Integer)
2020-12-17 17:54:23.601 DEBUG 16472 --- [ main]
org.example.mapper.ArticleMapper.insert : <== Updates: 1
Article(id=null, title=测试一下, content=看看对不对哇, viewCount=null, userId=4,
createTime=null, user=null)
```


```
DELETE t1 FROM t1,t2 WHERE t1.id=t2.id
或
DELETE FROM t1 USING t1,t2 WHERE t1.id=t2.id
```


```
1 package org.example.mapper;
2
```

ArticleMapper.xml 映射文件的配置：

###### 单元测试的代码：

### #{参数} vs ${参数}

对于 **#{参数}** 的使用来说，如果参数是字符串，在替换占位符时，会在 sql 语句中加上单引号。

如果是不能使用单引号的字符串，例如 sql 语句是 order by 字段 {传入参数}，此时 **{传入参数}** 就需

要使用 **${传入参数}** 这样的占位符，替换时不会带上单引号。

示例：在以上模糊查询语句中，加上根据文章标题排序的功能，要求是根据方法参数传入的字符串 asc
或 desc 来排序 。

ArticleMapper接口方法调整为：

ArticleMapper.xml调整为：

```
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Param;
import org.example.model.Article;
import org.springframework.stereotype.Component;
```

```
import java.util.List;
```

```
@Mapper
@Component
public interface ArticleMapper {
```

```
Article selectById(Integer id);
```

```
int insert(Article article);
```

```
List<Article> selectLike(@Param("title") String title, @Param("content")
String content);
}
```


```
<select id="selectLike" resultMap="BaseResultMap">
select id, title, content, create_time, view_count, user_id
from article
where title like #{title}
and content like #{content}
</select>
```


```
@Test
public void selectLike(){
String title = "%排序%";
String content = "%public%";
List<Article> articles = articleMapper.selectLike(title, content);
System.out.println(articles);
}
```

```
List<Article> selectLike(@Param("title") String title, @Param("content")
String content,
@Param("orderBy") String orderBy);
```



###### 单元测试代码调整为：

### 插入时获取自增主键

在之前插入数据时，如果是自增主键，插入后无法获取到。此时需要在 Mybatis 映射文件中，<insert>
标签配置如下属性：

```
useGeneratedKeys：这会令 MyBatis 使用 JDBC 的 getGeneratedKeys 方法来取出由数据库内部
生成的主键（比如：像 MySQL 和 SQL Server 这样的关系型数据库管理系统的自动递增字段），
默认值：false。
keyColumn：设置生成键值在表中的列名，在某些数据库（像 PostgreSQL）中，当主键列不是表
中的第一列的时候，是必须设置的。如果生成列不止一个，可以用逗号分隔多个属性名称。
keyProperty：指定能够唯一识别对象的属性，MyBatis 会使用 getGeneratedKeys 的返回值或
insert 语句的 selectKey 子元素设置它的值，默认值：未设置（unset）。如果生成列不止一个，
可以用逗号分隔多个属性名称。
```

以上部分是官方说明，对此我们在只有一个主键，且为创建表时第一个列时，可以不设置 keyColumn。

示例：插入文章的 Mybatis 映射文件中，插入部分调整为：

只需要在<insert>标签新增 useGeneratedKeys 及 keyProperty 属性即可。可以在单元测试代码中执

行观察打印的文章信息，已经可以获取自增插入的主键值。

```
<select id="selectLike" resultMap="BaseResultMap">
select id, title, content, create_time, view_count, user_id
from article
where title like #{title}
and content like #{content}
order by title ${orderBy}
</select>
```


```
@Test
public void selectLike(){
String title = "%排序%";
String content = "%public%";
List<Article> articles = articleMapper.selectLike(title, content,
"desc");
System.out.println(articles);
}
```


```
<insert id="insert" parameterType="org.example.model.Article"
useGeneratedKeys="true" keyProperty="id">
insert into article(title, content, user_id) values
(
#{title},
#{content},
#{userId}
)
</insert>
```



### 一对一结果映射

###### 以上创建的文章表与用户表的关系为多对一的关系，一个用户对多个文章，一个文章对一个用户。如果

在查询文章时，需要把文章关联用户一起查询返回，需要怎么设计映射的 Java 对象呢？

一般考虑如下方式设计文章类：

###### 在文章类中，有用户类的成员变量，这样在查询文章时，一条文章可以关联一个用户。

###### 示例：查询所有文章及关联的用户信息

设计 ArticleMapper 接口方法：

根据以上接口方法，在 ArticleMapper.xml 中配置查询 sql 语句：

```
package org.example.model;
```

```
import lombok.Getter;
import lombok.Setter;
import lombok.ToString;
```

```
import java.util.Date;
```

```
@Getter
@Setter
@ToString
public class Article {
private Integer id;
```

```
private String title;
```

```
private String content;
```

```
private Integer viewCount;
```

```
private Integer userId;
```

```
private Date createTime;
```

```
private User user;
}
```


```
1 List<Article> selectAll();
```

```
<select id="selectAll"
resultMap="BaseResultMap">
select
a.id,
a.title,
a.content,
a.view_count,
a.user_id,
a.create_time,
u.id u_id,
u.username u_username,
u.password u_password,
```



以上 sql 查询字段需要将用户的结果集字段再次映射到用户resultMap，所以全部用户表的字段都给了别
名：统一加上前缀 u_

要产生结果集映射，还需要配置<resultMap>标签，由于文章的结果集还会映射用户类，所以也需要准
备好用户映射配置文件 UserMapper.xml：

然后在文章结果集映射中，将用户作为结果集映射的一部分，使用<association>标签作为一对一的关系
关联。

以下为 ArticleMapper.xml 的结果集映射配置：

```
u.nickname u_nickname,
u.sex u_sex,
u.birthday u_birthday,
u.head u_head,
u.create_time u_create_time
from article a
join user u
on u.id=a.user_id
</select>
```


```
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE mapper PUBLIC "-//mybatis.org//DTD Mapper 3.0//EN"
"http://mybatis.org/dtd/mybatis-3-mapper.dtd">
<mapper namespace="org.example.mapper.UserMapper">
<resultMap id="BaseResultMap" type="org.example.model.User">
<id column="id" property="id" />
<result column="username" property="username" />
<result column="password" property="password" />
<result column="nickname" property="nickname" />
<result column="sex" property="sex" />
<result column="birthday" property="birthday" />
<result column="head" property="head" />
<result column="create_time" property="createTime" />
</resultMap>
```

```
</mapper>
```


```
<resultMap id="BaseResultMap" type="org.example.model.Article">
<id column="id" property="id" />
<result column="title" property="title" />
<result column="content" property="content" />
<result column="view_count" property="viewCount" />
<result column="user_id" property="userId" />
<result column="create_time" property="createTime" />
<association property="user"
columnPrefix="u_"
resultMap="org.example.mapper.UserMapper.BaseResultMap">
</association>
<!-- <association property="user"
javaType="org.example.model.User">-->
<!-- <id column="u_id" property="id" />-->
<!-- <result column="u_username" property="username" />-->
<!-- <result column="u_password" property="password" />-->
<!-- <result column="u_nickname" property="nickname" />-->
<!-- <result column="u_sex" property="sex" />-->
<!-- <result column="u_birthday" property="birthday" />-->
```


以上使用 <association>标签，表示一对一的结果映射：

```
property 属性：指定 Article 中对应的属性，即用户。
resultMap 属性：指定关联的结果集映射，将基于该映射配置来组织用户数据。
columnPrefix 属性：绑定一对一对象时，是通过 columnPrefix+association.resultMap.column
来映射结果集字段。association.resultMap.column是指 <association>标签中 resultMap属性，
对应的结果集映射中，column字段。
```

完成以上功能的单元测试：

###### 可以看到打印的文章对象中已包含了用户信息：

```
<!-- <result column="u_head" property="head" />-->
<!-- <result column="u_create_time" property="createTime" />-
->
<!-- </association>-->
</resultMap>
```


```
@Test
public void selectAll(){
List<Article> articles = articleMapper.selectAll();
articles.forEach(System.out::println);
}
```


```
2021-01-22 18:08:26.474 DEBUG 15756 --- [ main]
o.e.mapper.ArticleMapper.selectAll : ==> Preparing: select a.id,
a.title, a.content, a.view_count, a.user_id, a.create_time, u.id u_id,
u.username u_username, u.password u_password, u.nickname u_nickname, u.sex
u_sex, u.birthday u_birthday, u.head u_head, u.create_time u_create_time
from article a join user u on u.id=a.user_id
2021-01-22 18:08:26.489 DEBUG 15756 --- [ main]
o.e.mapper.ArticleMapper.selectAll : ==> Parameters:
2021-01-22 18:08:26.503 DEBUG 15756 --- [ main]
o.e.mapper.ArticleMapper.selectAll : <== Total: 9
Article(id=1, title=快速排序, content=public ..., viewCount=0, userId=1,
createTime=Thu Jan 21 15:56:12 CST 2021, user=User(id=1, username=a1,
password=11, nickname=null, sex=false, birthday=null, head=null,
createTime=Thu Jan 21 15:56:12 CST 2021, articles=[]))
Article(id=2, title=冒泡排序, content=private ..., viewCount=0, userId=1,
createTime=Thu Jan 21 15:56:13 CST 2021, user=User(id=1, username=a1,
password=11, nickname=null, sex=false, birthday=null, head=null,
createTime=Thu Jan 21 15:56:12 CST 2021, articles=[]))
Article(id=3, title=选择排序, content=private ..., viewCount=0, userId=1,
createTime=Thu Jan 21 15:56:13 CST 2021, user=User(id=1, username=a1,
password=11, nickname=null, sex=false, birthday=null, head=null,
createTime=Thu Jan 21 15:56:12 CST 2021, articles=[]))
Article(id=4, title=归并排序, content=public ..., viewCount=0, userId=2,
createTime=Thu Jan 21 15:56:13 CST 2021, user=User(id=2, username=a2,
password=12, nickname=null, sex=false, birthday=null, head=null,
createTime=Thu Jan 21 15:56:12 CST 2021, articles=[]))
Article(id=5, title=插入排序, content=protected ..., viewCount=0, userId=2,
createTime=Thu Jan 21 15:56:13 CST 2021, user=User(id=2, username=a2,
password=12, nickname=null, sex=false, birthday=null, head=null,
createTime=Thu Jan 21 15:56:12 CST 2021, articles=[]))
```


```
Article(id=6, title=希尔排序, content=protected ..., viewCount=0, userId=3,
createTime=Thu Jan 21 15:56:13 CST 2021, user=User(id=3, username=b,
password=2, nickname=null, sex=false, birthday=null, head=null,
createTime=Thu Jan 21 15:56:12 CST 2021, articles=[]))
Article(id=7, title=List, content=public ..., viewCount=0, userId=4,
createTime=Thu Jan 21 15:56:13 CST 2021, user=User(id=4, username=c,
password=3, nickname=null, sex=false, birthday=null, head=null,
createTime=Thu Jan 21 15:56:12 CST 2021, articles=[]))
Article(id=8, title=Set, content=public ..., viewCount=0, userId=4,
createTime=Thu Jan 21 15:56:13 CST 2021, user=User(id=4, username=c,
password=3, nickname=null, sex=false, birthday=null, head=null,
createTime=Thu Jan 21 15:56:12 CST 2021, articles=[]))
Article(id=9, title=Map, content=public ..., viewCount=0, userId=4,
createTime=Thu Jan 21 15:56:14 CST 2021, user=User(id=4, username=c,
password=3, nickname=null, sex=false, birthday=null, head=null,
createTime=Thu Jan 21 15:56:12 CST 2021, articles=[]))
2021-01-22 18:08:26.512 INFO 15756 --- [ main]
o.s.t.c.transaction.TransactionContext : Rolled back transaction for test:
[DefaultTestContext@747ddf94 testClass = ArticleMapperTest, testInstance =
test.example.mapper.ArticleMapperTest@7a904f32, testMethod =
selectAll@ArticleMapperTest, testException = [null],
mergedContextConfiguration = [WebMergedContextConfiguration@35e2d654
testClass = ArticleMapperTest, locations = '{}', classes = '{class
org.example.Application, class org.example.Application}',
contextInitializerClasses = '[]', activeProfiles = '{}',
propertySourceLocations = '{}', propertySourceProperties =
'{org.springframework.boot.test.context.SpringBootTestContextBootstrapper=tr
ue}', contextCustomizers =
set[org.springframework.boot.test.context.filter.ExcludeFilterContextCustomi
zer@1e7c7811,
org.springframework.boot.test.json.DuplicateJsonObjectContextCustomizerFacto
ry$DuplicateJsonObjectContextCustomizer@a38d7a3,
org.springframework.boot.test.mock.mockito.MockitoContextCustomizer@0,
org.springframework.boot.test.web.client.TestRestTemplateContextCustomizer@4
3bd930a,
org.springframework.boot.test.autoconfigure.properties.PropertyMappingContex
tCustomizer@0,
org.springframework.boot.test.autoconfigure.web.servlet.WebDriverContextCust
omizerFactory$Customizer@42607a4f,
org.springframework.boot.test.context.SpringBootTestArgs@1,
org.springframework.boot.test.context.SpringBootTestWebEnvironment@3224f60b]
, resourceBasePath = 'src/main/webapp', contextLoader =
'org.springframework.boot.test.context.SpringBootContextLoader', parent =
[null]], attributes =
map['org.springframework.test.context.web.ServletTestExecutionListener.activ
ateListener' -> true,
'org.springframework.test.context.web.ServletTestExecutionListener.populated
RequestContextHolder' -> true,
'org.springframework.test.context.web.ServletTestExecutionListener.resetRequ
estContextHolder' -> true]]
```



### 一对多结果映射

###### 以上文章关联用户是一对一的关系，反过来，用户关联文章就是一对多的关系。例如查询用户，同样需

要把该用户关联的多个文章一起返回，先考虑，如何设计结果集映射的 Java 对象？

以下为用户类的设计：

在用户类中，一个用户对象关联多个文章，通过用户中 List 类型的成员变量来组织关系。

示例：查询所有用户信息及关联的文章信息

设计 UserMapper 接口方法：

```
package org.example.model;
```

```
import lombok.Getter;
import lombok.Setter;
import lombok.ToString;
```

```
import java.util.Date;
import java.util.List;
```

```
@Getter
@Setter
@ToString
public class User {
private Integer id;
```

```
private String username;
```

```
private String password;
```

```
private String nickname;
```

```
private Boolean sex;
```

```
private Date birthday;
```

```
private String head;
```

```
private Date createTime;
```

```
private List<Article> articles;
}
```

```
package org.example.mapper;
```

```
import org.apache.ibatis.annotations.Mapper;
import org.example.model.User;
import org.springframework.stereotype.Component;
```

```
import java.util.List;
```

```
@Mapper
@Component
public interface UserMapper {
```



根据以上接口方法，在 UserMapper.xml 映射文件中配置查询 sql 语句：

<resultMap>结果集映射中，一对多关系需要使用<collection>标签，使用方法和<association>类似。

以下为 UserMapper.xml 的结果集映射配置：

###### 以下是单元测试代码：

```
List<User> selectAll();
}
```


```
<select id="selectAll" resultMap="BaseResultMap">
select
a.id a_id,
a.title a_title,
a.content a_content,
a.view_count a_view_count,
a.user_id a_user_id,
a.create_time a_create_time,
u.id,
u.username,
u.password,
u.nickname,
u.sex,
u.birthday,
u.head,
u.create_time
from article a
join user u
on u.id=a.user_id
</select>
```

```
<!-- 定义结果集映射关系：绑定结果集字段和转换的java对象之间的关系 -->
<resultMap id="BaseResultMap" type="org.example.model.User">
<!-- 结果集字段和java对象属性的映射 -->
<id column="id" property="id" />
<result column="username" property="username" />
<result column="password" property="password" />
<result column="nickname" property="nickname" />
<result column="sex" property="sex" />
<result column="birthday" property="birthday" />
<result column="head" property="head" />
<result column="create_time" property="createTime" />
<collection property="articles"
columnPrefix="a_"
resultMap="org.example.mapper.ArticleMapper.BaseResultMap"
/>
</resultMap>
```


```
package org.example.mapper;
```

```
import org.example.model.User;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
```


###### 以下为输出内容，可以看到用户已经绑定了多个文章数据：

```
import org.springframework.test.context.junit4.SpringRunner;
```

```
import java.util.List;
```

```
//指定为Spring环境中的单元测试
@RunWith(SpringRunner.class)
//指定为SpringBoot环境的单元测试，Application为启动类
@SpringBootTest(classes = Application.class)
//使用事务，在SpringBoot的单元测试中会自动回滚
@Transactional
public class UserMapperTest {
```

```
@Autowired
private UserMapper userMapper;
```

```
@Test
public void selectAll(){
List<User> users = userMapper.selectAll();
users.stream()
.forEach(System.out::println);
}
}
```


```
User(id=1, username=a1, password=11, nickname=null, sex=false, birthday=null,
head=null, createTime=Thu Jan 21 15:56:12 CST 2021, articles=[Article(id=1,
title=快速排序, content=public ..., viewCount=0, userId=1, createTime=Thu Jan
21 15:56:12 CST 2021, user=null), Article(id=2, title=冒泡排序,
content=private ..., viewCount=0, userId=1, createTime=Thu Jan 21 15:56:13
CST 2021, user=null), Article(id=3, title=选择排序, content=private ...,
viewCount=0, userId=1, createTime=Thu Jan 21 15:56:13 CST 2021, user=null)])
User(id=2, username=a2, password=12, nickname=null, sex=false, birthday=null,
head=null, createTime=Thu Jan 21 15:56:12 CST 2021, articles=[Article(id=4,
title=归并排序, content=public ..., viewCount=0, userId=2, createTime=Thu Jan
21 15:56:13 CST 2021, user=null), Article(id=5, title=插入排序,
content=protected ..., viewCount=0, userId=2, createTime=Thu Jan 21 15:56:13
CST 2021, user=null)])
User(id=3, username=b, password=2, nickname=null, sex=false, birthday=null,
head=null, createTime=Thu Jan 21 15:56:12 CST 2021, articles=[Article(id=6,
title=希尔排序, content=protected ..., viewCount=0, userId=3, createTime=Thu
Jan 21 15:56:13 CST 2021, user=null)])
User(id=4, username=c, password=3, nickname=null, sex=false, birthday=null,
head=null, createTime=Thu Jan 21 15:56:12 CST 2021, articles=[Article(id=7,
title=List, content=public ..., viewCount=0, userId=4, createTime=Thu Jan 21
15:56:13 CST 2021, user=null), Article(id=8, title=Set, content=public ...,
viewCount=0, userId=4, createTime=Thu Jan 21 15:56:13 CST 2021, user=null),
Article(id=9, title=Map, content=public ..., viewCount=0, userId=4,
createTime=Thu Jan 21 15:56:14 CST 2021, user=null)])
2021-01-22 18:14:08.347 INFO 14128 --- [ main]
o.s.t.c.transaction.TransactionContext : Rolled back transaction for test:
[DefaultTestContext@747ddf94 testClass = UserMapperTest, testInstance =
test.example.mapper.UserMapperTest@476e8796, testMethod =
selectAll@UserMapperTest, testException = [null], mergedContextConfiguration
= [WebMergedContextConfiguration@35e2d654 testClass = UserMapperTest,
locations = '{}', classes = '{class org.example.Application, class
org.example.Application}', contextInitializerClasses = '[]', activeProfiles =
'{}', propertySourceLocations = '{}', propertySourceProperties =
'{org.springframework.boot.test.context.SpringBootTestContextBootstrapper=tru
e}', contextCustomizers =
set[org.springframework.boot.test.context.filter.ExcludeFilterContextCustomiz
er@1e7c7811,
org.springframework.boot.test.json.DuplicateJsonObjectContextCustomizerFactor
y$DuplicateJsonObjectContextCustomizer@a38d7a3,
org.springframework.boot.test.mock.mockito.MockitoContextCustomizer@0,
org.springframework.boot.test.web.client.TestRestTemplateContextCustomizer@43
bd930a,
org.springframework.boot.test.autoconfigure.properties.PropertyMappingContext
Customizer@0,
org.springframework.boot.test.autoconfigure.web.servlet.WebDriverContextCusto
mizerFactory$Customizer@42607a4f,
org.springframework.boot.test.context.SpringBootTestArgs@1,
org.springframework.boot.test.context.SpringBootTestWebEnvironment@3224f60b],
resourceBasePath = 'src/main/webapp', contextLoader =
'org.springframework.boot.test.context.SpringBootContextLoader', parent =
[null]], attributes =
map['org.springframework.test.context.web.ServletTestExecutionListener.activa
teListener' -> true,
'org.springframework.test.context.web.ServletTestExecutionListener.populatedR
equestContextHolder' -> true,
'org.springframework.test.context.web.ServletTestExecutionListener.resetReque
stContextHolder' -> true]]
```


### 动态sql

动态 sql 是Mybatis的强大特性之一，能够完成不同条件下不同的 sql 拼接。

可以参考官方文档：Mybatis动态sql

首先思考一个问题，某系统要完成用户注册功能，会在数据库中要插入一个用户，注册时，用户名密码
是必填项，其他字段（昵称、性别、生日、头像）是选填项，在以Mybatis完成 sql 插入语句时，如何能
完成以上功能。

要注意，性别字段在数据库设置了默认值约束，不插入字段时，默认插入 0 。显示指定 null 来插入，就
没有默认值 0 了。如以下 sql，结果会不同：

插入的用户名为 d 的性别会为默认值 0 。

插入的用户名为 d 的性别会为给定的null。

表现在Mybatis中即为用户对象中 sex 属性的值，如果是null就不应该插入，使用默认值 0 ，有值才插
入。

先定义 UserMapper 中的接口方法：

#### <if>if标签

再完成 UserMapper.xml 的插入语句，此时可以使用Mybatis提供的<if>标签：

###### 

```
1 insert into user(username, password) values ('d', '4');
```

```
1 insert into user(username, password, sex) values ('d', '4', null);
```

```
1 int insert(User user);
```

```
<insert id="insert" parameterType="org.example.model.User"
useGeneratedKeys="true" keyProperty="id">
insert into user(
username,
password,
nickname,
<if test="sex != null">
sex,
</if>
birthday,
head
) values (
#{username},
#{password},
#{nickname},
<if test="sex != null">
#{sex},
</if>
#{birthday},
#{head}
```



注意 test 中的 sex，是传入对象中的属性，不是数据库字段。

完成单元测试代码，需要提供多个测试用例，一个 sex 属性使用 null，一个使用不为 null 的值：

#### <trim>trim标签

之前的插入用户功能，只是有一个 sex 字段可能是选填项，如果有多个字段，一般考虑使用<trim>标签
结合<if>标签，对多个字段都采取动态生成的方式。

<trim>标签中有如下属性：

```
prefix：表示整个语句块，以prefix的值作为前缀
suffix：表示整个语句块，以suffix的值作为后缀
prefixOverrides：表示整个语句块要去除掉的前缀
suffixOverrides：表示整个语句块要去除掉的后缀
```

调整 UserMapper.xml 的插入语句为：

```
</insert>
```


```
@Test
public void insert1(){
User user = new User();
user.setUsername("d");
user.setPassword("4");
user.setSex(true);
userMapper.insert(user);
System.out.println(user);
}
```

```
@Test
public void insert2(){
User user = new User();
user.setUsername("e");
user.setPassword("5");
userMapper.insert(user);
System.out.println(user);
}
```


```
<insert id="insert" parameterType="org.example.model.User"
useGeneratedKeys="true" keyProperty="id">
insert into user
<trim prefix="(" suffix=")" suffixOverrides=",">
<if test="username != null">
username,
</if>
<if test="password != null">
password,
</if>
<if test="nickname != null">
nickname,
</if>
<if test="sex != null">
sex,
</if>
<if test="birthday != null">
```


在以上 sql 动态解析时，会将第一个 <trim> 部分做如下处理：

```
基于 prefix 配置，开始部分加上 (
基于 suffix 配置，结束部分加上 )
多个 <if>组织的语句都以 , 结尾，在最后拼接好的字符串还会以 , 结尾，会基于
suffixOverrides 配置去掉最后一个 ,
注意 <if test=“createTime != null”> 中的 createTime 是传入对象的属性
```

#### <where>where标签

传入的用户对象，根据属性做where条件查询，用户对象中属性不为 null 的，都为查询条件。如
user.username 为 "a"，则查询条件为 where username="a"：

UserMapper 接口中新增条件查询方法：

UserMapper.xml 中新增条件查询 sql：

```
birthday,
</if>
<if test="head != null">
head,
</if>
<if test="createTime != null">
create_time,
</if>
</trim>
<trim prefix="values (" suffix=")" suffixOverrides=",">
<if test="username != null">
#{username},
</if>
<if test="password != null">
#{password},
</if>
<if test="nickname != null">
#{nickname},
</if>
<if test="sex != null">
#{sex},
</if>
<if test="birthday != null">
#{birthday},
</if>
<if test="head != null">
#{head},
</if>
<if test="createTime != null">
#{createTime},
</if>
</trim>
</insert>
```


```
1 List<User> selectByCondition(User user);
```

```
<select id="selectByCondition" parameterType="org.example.model.User"
resultMap="BaseResultMap">
```

###### 


以上<where>标签也可以使用 <trim prefix="where" prefixOverrides="and"> 替换。

单元测试代码如下：



根据传入的用户对象属性来更新用户数据，可以使用<set>标签来指定动态内容。

UserMapper 接口中修改用户方法：根据传入的用户 id 属性，修改其他不为 null 的属性：

```
select id, username, password, nickname, sex, birthday, head,
create_time
from user
<where>
<if test="username != null">
and username=#{username}
</if>
<if test="password != null">
and password=#{password}
</if>
<if test="nickname != null">
and nickname=#{nickname}
</if>
<if test="sex != null">
and sex=#{sex}
</if>
<if test="birthday != null">
and birthday=#{birthday}
</if>
<if test="head != null">
and head=#{head}
</if>
<if test="createTime != null">
and create_time=#{createTime}
</if>
</where>
</select>
```

```
@Test
public void selectByCondition(){
User user = new User();
user.setUsername("e");
user.setPassword("5");
List<User> users = userMapper.selectByCondition(user);
System.out.println(users);
}
```

```
@Test
public void selectByCondition2(){
User user = new User();
user.setSex(false);
List<User> users = userMapper.selectByCondition(user);
System.out.println(users);
}
```


```
1 int updateById(User user);
```

UserMapper.xml 中添加更新用户 sql：

以上<set>标签也可以使用 <trim prefix="set" suffixOverrides=","> 替换。

单元测试代码如下：

#### <foreach>foreach标签

对集合进行遍历时可以使用该标签。<foreach>标签有如下属性：

```
collection：绑定方法参数中的集合，如 List，Set，Map或数组对象
item：遍历时的每一个对象
open：语句块开头的字符串
close：语句块结束的字符串
separator：每次遍历之间间隔的字符串
```

示例：根据多个文章 id 来删除文章数据。

ArticleMapper 中新增接口方法：

```
<update id="updateById" parameterType="org.example.model.User">
update user
<set>
<if test="username != null">
username=#{username},
</if>
<if test="password != null">
password=#{password},
</if>
<if test="nickname != null">
nickname=#{nickname},
</if>
<if test="sex != null">
sex=#{sex},
</if>
<if test="birthday != null">
birthday=#{birthday},
</if>
<if test="head != null">
head=#{head},
</if>
<if test="createTime != null">
create_time=#{createTime},
</if>
</set>
where id=#{id}
</update>
```

```
@Test
public void updateById(){
User user = new User();
user.setId( 1 );
user.setUsername("aaa");
user.setPassword("123");
int n = userMapper.updateById(user);
System.out.println(n);
}
```



ArticleMapper.xml 中新增删除 sql：

###### 单元测试代码：

### MyBatis代码生成工具

###### 对于常见的单表操作，几乎所有功能都是相同的，如：

###### 根据主键查询单条数据

###### 根据主键修改单条数据

###### 根据主键删除单条数据

###### 插入单条数据

如果对每张表都要完成类似的Mybatis代码，包括Mapper，XML，实体类，其中代码都是类似，而且工
作量也是非常大的。

幸好官方提供了一套Mybatis的生成工具，可以通过工具自动生成以上代码：

参考资料：Mybatis生成工具官方文档，Mybatis生成工具详解

**以下代码请新创建项目使用，以免生成的代码对现有代码造成影响。**

#### 使用示例一

###### 使用简单的生成方式，准备以下两个资源：

在 src/main/resources 目录下，创建 generator/config.xml 配置文件，生成工具会使用该配置信

息完成代码生成：

```
1 int deleteByIds(List<Integer> ids);
```

```
<delete id="deleteByIds">
delete from article
where id in
<foreach collection="list" item="item" open="(" close=")" separator=",">
#{item}
</foreach>
</delete>
```


```
@Test
public void deleteByIds(){
List<Integer> list = new ArrayList<>();
list.add( 2 );
list.add( 3 );
int n = articleMapper.deleteByIds(list);
System.out.println(n);
}
```


```
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE generatorConfiguration
PUBLIC "-//mybatis.org//DTD MyBatis Generator Configuration 1.0//EN"
"http://mybatis.org/dtd/mybatis-generator-config_1_0.dtd">
```

```
<generatorConfiguration>
```

```
<!-- 引入某个配置文件的信息，以 ${键} 的方式获取值 -->
```



```
<properties resource="application.properties" />
```

```
<context id="Mysql" defaultModelType="flat" targetRuntime="MyBatis3">
```

```
<!-- 表名或字段名为关键字的时候，生成的sql中给表名或字段名添加分隔符 ` -->
<property name="beginningDelimiter" value="true" />
<property name="endingDelimiter" value="true" />
```

```
<!-- 生成的Java文件的编码 -->
<property name="javaFileEncoding" value="UTF-8"/>
```

```
<!-- 不生成注释 -->
<commentGenerator>
<property name="suppressDate" value="true"/>
<property name="suppressAllComments" value="true" />
</commentGenerator>
```

```
<!-- JDBC连接配置 -->
<jdbcConnection driverClass="${spring.datasource.driver-class-name}"
connectionURL="${spring.datasource.url}"
userId="${spring.datasource.username}"
password="${spring.datasource.password}">
<!-- 读取数据库表定义的注释信息 -->
<property name="useInformationSchema" value="true" />
</jdbcConnection>
```

```
<!-- 默认false，把JDBC DECIMAL 和 NUMERIC 类型解析为 Integer，
为 true时把JDBC DECIMAL 和 NUMERIC 类型解析为
java.math.BigDecimal -->
<javaTypeResolver>
<property name="forceBigDecimals" value="false" />
</javaTypeResolver>
```

```
<!-- 生成实体类的配置 -->
<javaModelGenerator targetProject="src/test/java"
targetPackage="org.example.model">
<!-- 指定需要继承的父类 -->
<!-- <property name="rootClass"
value="org.example.base.BaseEntity"/>-->
</javaModelGenerator>
```

```
<!-- 生成XML文件的配置 -->
<sqlMapGenerator targetProject="src/test/resources"
targetPackage="mapper">
</sqlMapGenerator>
```

```
<!-- 生成Mapper接口配置 -->
<javaClientGenerator type="XMLMAPPER"
targetProject="src/test/java"
targetPackage="org.example.mapper">
<!-- 指定要继承的父接口 -->
<!-- <property name="rootInterface"
value="org.example.base.BaseMapper"/>-->
</javaClientGenerator>
```

```
<!-- 需要生成的表，%表示模糊匹配，也可以指定具体的表名 -->
<table tableName="%"
enableCountByExample="false"
```

###### 以上配置为不同数据库生成代码时，需要修改的部分有：

```
<javaModelGenerator>、<sqlMapGenerator>、<javaClientGenerator> 标签中，
targetPackage属性，需要修改为自己要生成的包路径
<table> 标签中，<columnOverride> 表示覆盖的配置，如果不需要可以不用
```

以上配置完成后，可以使用生成工具了，官方提供了两种方式运行，插件或main方法运行，我们这里采
取main方法的方式。

随便在一个包下，创建如下Mybatis代码生成工具的启动类，以下为 org.example.tool.Generator：

```
enableDeleteByExample="false"
enableSelectByExample="false"
enableUpdateByExample="false"
>
<!-- insert方法通过自增主键插入数据后，主键值是否设置到对象属性中 -->
<generatedKey column="id" sqlStatement="JDBC"/>
<!-- 字段覆盖：表中content字段为text数据类型时，默认会生成为二进制，可以指
定为字符串 -->
<columnOverride column="content" jdbcType="VARCHAR" />
</table>
</context>
</generatorConfiguration>
```

```
package org.example.tool;
```

```
import org.mybatis.generator.api.MyBatisGenerator;
import org.mybatis.generator.config.Configuration;
import org.mybatis.generator.config.xml.ConfigurationParser;
import org.mybatis.generator.internal.DefaultShellCallback;
```

```
import java.io.InputStream;
import java.util.ArrayList;
import java.util.List;
```

```
public class Generator {
```

```
private static final boolean OVERWRITE = true;
```

```
private static final String CONFIG_PATH = "generator/config.xml";
```

```
public static void main(String[] args) throws Exception {
```

```
System.out.println("--------------------start generator-------------
------");
List<String> warnings = new ArrayList<>();
```

```
ClassLoader classloader =
Thread.currentThread().getContextClassLoader();
InputStream is = classloader.getResourceAsStream(CONFIG_PATH);
ConfigurationParser cp = new ConfigurationParser(warnings);
Configuration config = cp.parseConfiguration(is);
DefaultShellCallback callback = new DefaultShellCallback(OVERWRITE);
MyBatisGenerator myBatisGenerator = new MyBatisGenerator(config,
callback, warnings);
myBatisGenerator.generate(null);
warnings.forEach(System.err::println);
```

运行启动类，会根据 generator/config.xml 配置文件内容，在项目的 src/test/java 和

```
src/test/resources 目录下，生成指定的文件。 注意：不要直接在 src/main/java 或
src/main/resources 下生成，以免覆盖已有文件。
```

以上配置文件在使用上稍微有点笨重：

```
生成的Mapper接口都是一堆类似的方法
实体类中生成一大堆的Getter，Setter方法
生成的XML文件如果没有删除，再次生成时，会以追加的方式生成
```

对以上问题，我们可以使用以下配置方案

#### 使用示例二

为所有Mapper接口指定父接口，以下为 src/main/java 中，创建 org.example.base.BaseMapper

接口：

之后生成的Mapper接口统一继承该父接口，不再有自己的方法。

再提供几个生成工具的插件，以下都为在 src/main/java 中，org.example.tool 包下创建的插件

类：

生成插件：生成的实体类可以使用lombok注解，不生成Getter，Setter方法：

```
System.out.println("--------------------end generator---------------
----");
}
}
```

```
package org.example.base;
```

```
public interface BaseMapper<T> {
```

```
int deleteByPrimaryKey(Integer id);
```

```
int insert(T record);
```

```
int insertSelective(T record);
```

```
T selectByPrimaryKey(Integer id);
```

```
int updateByPrimaryKeySelective(T record);
```

```
int updateByPrimaryKey(T record);
}
```

```
package org.example.tool;
```

```
import org.mybatis.generator.api.IntrospectedColumn;
import org.mybatis.generator.api.IntrospectedTable;
import org.mybatis.generator.api.PluginAdapter;
import org.mybatis.generator.api.dom.java.FullyQualifiedJavaType;
import org.mybatis.generator.api.dom.java.Interface;
import org.mybatis.generator.api.dom.java.Method;
import org.mybatis.generator.api.dom.java.TopLevelClass;
import org.mybatis.generator.internal.util.StringUtility;
```



```
import java.util.HashSet;
import java.util.List;
import java.util.Properties;
```

```
/**
* 生成插件：
* 1. 实体类可以指定lombok注解，而不生成Getter，Setter方法
* 2. 可以指定继承的父类，会指定父接口使用的泛型类型（实体）
*/
public class DefaultGeneratorPlugin extends PluginAdapter {
```

```
private HashSet<String> rootMappers = new HashSet<>();
```

```
//是否需要生成Data注解
private boolean needsData = false;
//是否需要生成Getter注解
private boolean needsGetter = false;
//是否需要生成Setter注解
private boolean needsSetter = false;
//是否需要生成ToString注解
private boolean needsToString = false;
//是否需要生成Accessors(chain = true)注解
private boolean needsAccessors = false;
//是否需要生成EqualsAndHashCode注解
private boolean needsEqualsAndHashCode = false;
```

```
@Override
public boolean validate(List<String> warnings) {
return true;
}
```

```
@Override
public void setProperties(Properties properties) {
super.setProperties(properties);
String rootMappers = properties.getProperty("rootMappers");
if (StringUtility.stringHasValue(rootMappers)) {
for (String mapper : rootMappers.split(",")) {
this.rootMappers.add(mapper);
}
}
//lombok扩展
String lombok = properties.getProperty("lombok");
if (lombok != null && !"".equals(lombok)) {
this.needsData = lombok.contains("Data");
//@Data 优先级高于 @Getter @Setter @RequiredArgsConstructor
@ToString @EqualsAndHashCode
this.needsGetter = !this.needsData &&
lombok.contains("Getter");
this.needsSetter = !this.needsData &&
lombok.contains("Setter");
this.needsToString = !this.needsData &&
lombok.contains("ToString");
this.needsEqualsAndHashCode = !this.needsData &&
lombok.contains("EqualsAndHashCode");
this.needsAccessors = lombok.contains("Accessors");
}
}
```


```
@Override
public boolean clientGenerated(Interface interfaze, TopLevelClass
topLevelClass, IntrospectedTable introspectedTable) {
//获取实体类
FullyQualifiedJavaType entityType = new
FullyQualifiedJavaType(introspectedTable.getBaseRecordType());
//import接口
for (String mapper : rootMappers) {
interfaze.addImportedType(new FullyQualifiedJavaType(mapper));
interfaze.addSuperInterface(new FullyQualifiedJavaType(mapper +
"<" + entityType.getShortName() + ">"));
}
//import实体类
interfaze.addImportedType(entityType);
interfaze.addImportedType(new
FullyQualifiedJavaType("org.apache.ibatis.annotations.Mapper"));
interfaze.addAnnotation("@Mapper");
return true;
}
```

```
/**
* 生成基础实体类
*
* @param topLevelClass
* @param introspectedTable
* @return
*/
@Override
public boolean modelBaseRecordClassGenerated(TopLevelClass
topLevelClass, IntrospectedTable introspectedTable) {
//lombok扩展开始
//如果需要Data，引入包，代码增加注解
if (this.needsData) {
topLevelClass.addImportedType("lombok.Data");
topLevelClass.addAnnotation("@Data");
}
//如果需要Getter，引入包，代码增加注解
if (this.needsGetter) {
topLevelClass.addImportedType("lombok.Getter");
topLevelClass.addAnnotation("@Getter");
}
//如果需要Setter，引入包，代码增加注解
if (this.needsSetter) {
topLevelClass.addImportedType("lombok.Setter");
topLevelClass.addAnnotation("@Setter");
}
//如果需要ToString，引入包，代码增加注解
if (this.needsToString) {
topLevelClass.addImportedType("lombok.ToString");
topLevelClass.addAnnotation("@ToString");
}
//如果需要Getter，引入包，代码增加注解
if (this.needsAccessors) {
topLevelClass.addImportedType("lombok.experimental.Accessors");
topLevelClass.addAnnotation("@Accessors(chain = true)");
}
//如果需要Getter，引入包，代码增加注解
if (this.needsEqualsAndHashCode) {
```

```
topLevelClass.addImportedType("lombok.EqualsAndHashCode");
topLevelClass.addAnnotation("@EqualsAndHashCode");
}
return true;
}
```

```
/**
* 如果需要生成Getter注解，就不需要生成get相关代码了
*/
@Override
public boolean modelGetterMethodGenerated(Method method, TopLevelClass
topLevelClass, IntrospectedColumn introspectedColumn, IntrospectedTable
introspectedTable, ModelClassType modelClassType) {
return !(this.needsData || this.needsGetter);
}
```

```
/**
* 如果需要生成Setter注解，就不需要生成set相关代码了
*/
@Override
public boolean modelSetterMethodGenerated(Method method, TopLevelClass
topLevelClass, IntrospectedColumn introspectedColumn, IntrospectedTable
introspectedTable, ModelClassType modelClassType) {
return !(this.needsData || this.needsSetter);
}
```

```
@Override
public boolean clientInsertMethodGenerated(Method method, Interface
interfaze, IntrospectedTable introspectedTable) {
return false;
}
```

```
@Override
public boolean clientInsertMethodGenerated(Method method, TopLevelClass
topLevelClass, IntrospectedTable introspectedTable) {
return false;
}
```

```
@Override
public boolean clientInsertSelectiveMethodGenerated(Method method,
Interface interfaze, IntrospectedTable introspectedTable) {
return false;
}
```

```
@Override
public boolean clientInsertSelectiveMethodGenerated(Method method,
TopLevelClass topLevelClass, IntrospectedTable introspectedTable) {
return false;
}
```

```
@Override
public boolean clientSelectByPrimaryKeyMethodGenerated(Method method,
Interface interfaze, IntrospectedTable introspectedTable) {
return false;
}
```

```
@Override
```

```
public boolean clientSelectByPrimaryKeyMethodGenerated(Method method,
TopLevelClass topLevelClass, IntrospectedTable introspectedTable) {
return false;
}
```

```
@Override
public boolean clientUpdateByPrimaryKeySelectiveMethodGenerated(Method
method, Interface interfaze, IntrospectedTable introspectedTable) {
return false;
}
```

```
@Override
public boolean clientUpdateByPrimaryKeySelectiveMethodGenerated(Method
method, TopLevelClass topLevelClass, IntrospectedTable introspectedTable) {
return false;
}
```

```
@Override
public boolean
clientUpdateByPrimaryKeyWithoutBLOBsMethodGenerated(Method method,
Interface interfaze, IntrospectedTable introspectedTable) {
return false;
}
```

```
@Override
public boolean
clientUpdateByPrimaryKeyWithoutBLOBsMethodGenerated(Method method,
TopLevelClass topLevelClass, IntrospectedTable introspectedTable) {
return false;
}
```

```
@Override
public boolean clientDeleteByPrimaryKeyMethodGenerated(Method method,
Interface interfaze, IntrospectedTable introspectedTable) {
return false;
}
```

```
@Override
public boolean clientDeleteByPrimaryKeyMethodGenerated(Method method,
TopLevelClass topLevelClass, IntrospectedTable introspectedTable) {
return false;
}
```

```
@Override
public boolean clientCountByExampleMethodGenerated(Method method,
Interface interfaze, IntrospectedTable introspectedTable) {
return false;
}
```

```
@Override
public boolean clientCountByExampleMethodGenerated(Method method,
TopLevelClass topLevelClass, IntrospectedTable introspectedTable) {
return false;
}
```

```
@Override
public boolean clientDeleteByExampleMethodGenerated(Method method,
Interface interfaze, IntrospectedTable introspectedTable) {
```

```
return false;
}
```

```
@Override
public boolean clientDeleteByExampleMethodGenerated(Method method,
TopLevelClass topLevelClass, IntrospectedTable introspectedTable) {
return false;
}
```

```
@Override
public boolean clientSelectByExampleWithBLOBsMethodGenerated(Method
method, Interface interfaze, IntrospectedTable introspectedTable) {
return false;
}
```

```
@Override
public boolean clientSelectByExampleWithBLOBsMethodGenerated(Method
method, TopLevelClass topLevelClass, IntrospectedTable introspectedTable) {
return false;
}
```

```
@Override
public boolean clientSelectByExampleWithoutBLOBsMethodGenerated(Method
method, Interface interfaze, IntrospectedTable introspectedTable) {
return false;
}
```

```
@Override
public boolean clientSelectByExampleWithoutBLOBsMethodGenerated(Method
method, TopLevelClass topLevelClass, IntrospectedTable introspectedTable) {
return false;
}
```

```
@Override
public boolean clientUpdateByExampleSelectiveMethodGenerated(Method
method, Interface interfaze, IntrospectedTable introspectedTable) {
return false;
}
```

```
@Override
public boolean clientUpdateByExampleSelectiveMethodGenerated(Method
method, TopLevelClass topLevelClass, IntrospectedTable introspectedTable) {
return false;
}
```

```
@Override
public boolean clientUpdateByExampleWithBLOBsMethodGenerated(Method
method, Interface interfaze, IntrospectedTable introspectedTable) {
return false;
}
```

```
@Override
public boolean clientUpdateByExampleWithBLOBsMethodGenerated(Method
method, TopLevelClass topLevelClass, IntrospectedTable introspectedTable) {
return false;
}
```

```
@Override




###### 生成插件：XML文件以覆盖的方式生成

注释生成插件：实体类根据数据库表及字段comment生成注释

```

```java
public boolean clientUpdateByExampleWithoutBLOBsMethodGenerated(Method
                                                                method, Interface interfaze, IntrospectedTable introspectedTable) {
    return false;
}
    @Override
    public boolean clientUpdateByExampleWithoutBLOBsMethodGenerated(Method
                                                                    method, TopLevelClass topLevelClass, IntrospectedTable introspectedTable) {
    return false;
}

}

    package org.example.tool;

    import org.mybatis.generator.api.GeneratedXmlFile;
import org.mybatis.generator.api.IntrospectedTable;
import org.mybatis.generator.api.PluginAdapter;

​```

```

    import java.lang.reflect.Field;

import java.util.List;

```
    ```
    public class OverIsMergeablePlugin extends PluginAdapter {
        @Override
        public boolean validate(List<String> warnings) {
            return true;
        }

        ```
           ```
            @Override
            public boolean sqlMapGenerated(GeneratedXmlFile sqlMap,
                                           IntrospectedTable introspectedTable) {
            try {
                Field field = sqlMap.getClass().getDeclaredField("isMergeable");
                field.setAccessible(true);
                field.setBoolean(sqlMap, false);
            } catch (Exception e) {
                e.printStackTrace();
            }
            return true;
        }
    }

```

    ```
    
    package org.example.tool;

```

    ```
    
    import org.mybatis.generator.api.CommentGenerator;

import org.mybatis.generator.api.IntrospectedColumn;
import org.mybatis.generator.api.IntrospectedTable;
import org.mybatis.generator.api.dom.java.*;
import org.mybatis.generator.api.dom.xml.XmlElement;
import org.mybatis.generator.internal.util.StringUtility;

```

    ```
    
    import java.util.Properties;

```

    ```
    
    public class DefaultCommentGenerator implements CommentGenerator {
        @Override
        public void addConfigurationProperties(Properties properties) {



        }
    
        @Override
        public void addFieldComment(Field field, IntrospectedTable
                                    introspectedTable, IntrospectedColumn introspectedColumn) {
            if(introspectedColumn.isIdentity())
                field.addJavaDocLine("");
            if (StringUtility.stringHasValue(introspectedColumn.getRemarks())) {
                field.addJavaDocLine("/**");
                StringBuilder sb = new StringBuilder();
                sb.append(" * ");
                sb.append(introspectedColumn.getRemarks());
                field.addJavaDocLine(sb.toString());
                field.addJavaDocLine(" */");
            }
        }
    
        @Override
        public void addFieldComment(Field field, IntrospectedTable
                                    introspectedTable) {
    
        }
    
        @Override
        public void addModelClassComment(TopLevelClass topLevelClass,
                                         IntrospectedTable introspectedTable) {
            if (StringUtility.stringHasValue(introspectedTable.getRemarks())) {
                topLevelClass.addJavaDocLine("/**");
                topLevelClass.addJavaDocLine(" *
                                             "+introspectedTable.getRemarks());
                                             topLevelClass.addJavaDocLine(" */");
                                             }
                                             }



                                             @Override
                                             public void addClassComment(InnerClass innerClass, IntrospectedTable
                                                                         introspectedTable) {



                                             }



                                             ```java
                                             @Override
                                             public void addClassComment(InnerClass innerClass, IntrospectedTable
                                                                         introspectedTable, boolean markAsDoNotDelete) 
                                             }
                                             ```





                                             @Override
                                             public void addEnumComment(InnerEnum innerEnum, IntrospectedTable
                                                                        introspectedTable) {



                                             }



                                             @Override
    
                                             ```
                                             修改 src/main/resource/generator/config.xml 文件内容：
    
                                             ```
    
                                             public void addGetterComment(Method method, IntrospectedTable
                                                                          introspectedTable, IntrospectedColumn introspectedColumn) {



                                             }



                                             @Override
                                             public void addSetterComment(Method method, IntrospectedTable
                                                                          introspectedTable, IntrospectedColumn introspectedColumn) {
    
                                                 ```
    
                                                     ```
    
                                             }
    
                                             ```
    
                                             ```
    
                                             @Override
                                             public void addGeneralMethodComment(Method method, IntrospectedTable
                                                                                 introspectedTable) {
    
                                                 ```
    
                                                     ```
    
                                             }
    
                                             ```
    
                                             ```
    
                                             @Override
                                             public void addJavaFileComment(CompilationUnit compilationUnit) {
    
                                                 ```
    
                                                     ```
    
                                             }
    
                                             ```
    
                                             ```
    
                                             @Override
                                             public void addComment(XmlElement xmlElement) {
    
                                                 ```
    
                                                     ```
    
                                             }
    
                                             ```
    
                                             ```
    
                                             @Override
                                             public void addRootComment(XmlElement rootElement) {
    
                                                 ```
    
                                                     ```
    
                                             }
                                             }

```


```

```
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE generatorConfiguration
PUBLIC "-//mybatis.org//DTD MyBatis Generator Configuration 1.0//EN"
"http://mybatis.org/dtd/mybatis-generator-config_1_0.dtd">
```

```
<generatorConfiguration>
```

```
<!-- 引入某个配置文件的信息，以 ${键} 的方式获取值 -->
<properties resource="application.properties" />
```

```
<context id="Mysql" defaultModelType="flat" targetRuntime="MyBatis3">
```

```
<!-- 表名或字段名为关键字的时候，生成的sql中给表名或字段名添加分隔符 ` -->
<property name="beginningDelimiter" value="true" />
<property name="endingDelimiter" value="true" />
```

```
<!-- 生成的Java文件的编码 -->
<property name="javaFileEncoding" value="UTF-8"/>
```

```
<!-- 自定义插件：Mapper不生成方法，指定父接口来继承使用 -->
<plugin type="org.example.tool.DefaultGeneratorPlugin">
```



```
<property name="rootMappers" value="org.example.base.BaseMapper"
/>
<property name="lombok" value="Getter,Setter,ToString"/>
</plugin>
```

```
<!-- 自定义插件：生成的XML文件会覆盖已有文件 -->
<plugin type="org.example.tool.OverIsMergeablePlugin" />
```

```
<!-- 自定义注释插件：生成的实体类中，根据表和字段的comment生成注释 -->
<commentGenerator type="org.example.tool.DefaultCommentGenerator" />
```

```
<!-- JDBC连接配置 -->
<jdbcConnection driverClass="${spring.datasource.driver-class-name}"
connectionURL="${spring.datasource.url}"
userId="${spring.datasource.username}"
password="${spring.datasource.password}">
<!-- 读取数据库表定义的注释信息 -->
<property name="useInformationSchema" value="true" />
</jdbcConnection>
```

```
<!-- 默认false，把JDBC DECIMAL 和 NUMERIC 类型解析为 Integer，
为 true时把JDBC DECIMAL 和 NUMERIC 类型解析为
java.math.BigDecimal -->
<javaTypeResolver>
<property name="forceBigDecimals" value="false" />
</javaTypeResolver>
```

```
<!-- 生成实体类的配置 -->
<javaModelGenerator targetProject="src/test/java"
targetPackage="org.example.model">
<!-- 指定需要继承的父类 -->
<!-- <property name="rootClass"
value="org.example.base.BaseEntity"/>-->
</javaModelGenerator>
```

```
<!-- 生成XML文件的配置 -->
<sqlMapGenerator targetProject="src/test/resources"
targetPackage="mapper">
</sqlMapGenerator>
```

```
<!-- 生成Mapper接口配置 -->
<javaClientGenerator type="XMLMAPPER"
targetProject="src/test/java"
targetPackage="org.example.mapper">
<!-- 指定要继承的父接口 -->
<!-- <property name="rootInterface"
value="org.example.base.BaseMapper"/>-->
</javaClientGenerator>
```

```
<!-- 需要生成的表，%表示模糊匹配，也可以指定具体的表名 -->
<table tableName="%"
enableCountByExample="false"
enableDeleteByExample="false"
enableSelectByExample="false"
enableUpdateByExample="false"
>
<!-- insert方法通过自增主键插入数据后，主键值是否设置到对象属性中 -->
<generatedKey column="id" sqlStatement="JDBC"/>
```


###### 启动类和之前一样，直接运行即可生成。




```
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE generatorConfiguration
        PUBLIC "-//mybatis.org//DTD MyBatis Generator Configuration 1.0//EN"
        "http://mybatis.org/dtd/mybatis-generator-config_1_0.dtd">
<generatorConfiguration>
    <!-- 引入某个配置文件的信息，以 ${键} 的方式获取值 -->
    <properties resource="application.properties" />
    <context id="Mysql" defaultModelType="flat" targetRuntime="MyBatis3">
        <!-- 表名或字段名为关键字的时候，生成的sql中给表名或字段名添加分隔符 ` -->
        <property name="beginningDelimiter" value="true" />
        <property name="endingDelimiter" value="true" />
        <!-- 生成的Java文件的编码 -->
        <property name="javaFileEncoding" value="UTF-8"/>
        <!-- 自定义插件：Mapper不生成方法，指定父接口来继承使用 -->
        <plugin type="org.example.tool.DefaultGeneratorPlugin"> 123456789
            <property name="rootMappers" value="org.example.base.BaseMapper"
/>
            <property name="lombok" value="Getter,Setter,ToString"/>
        </plugin>
        <!-- 自定义插件：生成的XML文件会覆盖已有文件 -->
        <plugin type="org.example.tool.OverIsMergeablePlugin" />
        <!-- 自定义注释插件：生成的实体类中，根据表和字段的comment生成注释 -->
        <commentGenerator type="org.example.tool.DefaultCommentGenerator" />
        <!-- JDBC连接配置 -->
        <jdbcConnection driverClass="${spring.datasource.driver-class-name}"
                        connectionURL="${spring.datasource.url}"
                        userId="${spring.datasource.username}"
                        password="${spring.datasource.password}">
            <!-- 读取数据库表定义的注释信息 -->
            <property name="useInformationSchema" value="true" />
        </jdbcConnection>
        <!-- 默认false，把JDBC DECIMAL 和 NUMERIC 类型解析为 Integer，
                为 true时把JDBC DECIMAL 和 NUMERIC 类型解析为
java.math.BigDecimal -->
        <javaTypeResolver>
            <property name="forceBigDecimals" value="false" />
        </javaTypeResolver>
        <!-- 生成实体类的配置 -->
        <javaModelGenerator targetProject="src/test/java"
                            targetPackage="org.example.model">
            <!-- 指定需要继承的父类 -->
<!--           <property name="rootClass" 
value="org.example.base.BaseEntity"/>-->
        </javaModelGenerator>
        <!-- 生成XML文件的配置 -->
        <sqlMapGenerator targetProject="src/test/resources"
                         targetPackage="mapper">
        </sqlMapGenerator>
        <!-- 生成Mapper接口配置 -->
        <javaClientGenerator type="XMLMAPPER"
                             targetProject="src/test/java"
                             targetPackage="org.example.mapper">
            <!-- 指定要继承的父接口 -->
<!--           <property name="rootInterface" 
value="org.example.base.BaseMapper"/>-->
        </javaClientGenerator>
        <!-- 需要生成的表，%表示模糊匹配，也可以指定具体的表名 -->
        <table tableName="%"
               enableCountByExample="false"
               enableDeleteByExample="false"
               enableSelectByExample="false"
               enableUpdateByExample="false"
        >
            <!-- insert方法通过自增主键插入数据后，主键值是否设置到对象属性中 -->
            <generatedKey column="id" sqlStatement="JDBC"/>
<!-- 字段覆盖：表中content字段为text数据类型时，默认会生成为二进制，可以指
定为字符串 -->
<columnOverride column="content" jdbcType="VARCHAR" />
</table>
</context>
</generatorConfiguration>
```

启动类和之前一样，直接运行即可生成。
