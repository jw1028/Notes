# JDBC

**JDBC**，即**<code>Java Database Connectivity</code>**，java数据库连接。是一种用于执行SQL语句的Java API，它是Java中的数据库连接规范。这个API由 java.sql.*,javax.sql.* 包中的一些类和接口组成，它为Java 开发人员操作数据库提供了一个标准的API，可以为多种关系数据库提供统一访问。

# JDBC工作原理

**JDBC** 为多种关系数据库提供了统一访问方式，作为特定厂商数据库访问**API**的一种高级抽象，它主要包含一些通用的接口类。

**JDBC访问数据库层次结构:**
![在这里插入图片描述](https://img-blog.csdnimg.cn/20210316222825462.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQ1NjYxMTI1,size_16,color_FFFFFF,t_70)
**JDBC优势：**

 - Java语言访问数据库操作完全面向抽象接口编程 
 - 开发数据库应用不用限定在特定数据库厂商的API 
 - 程序的可移植性大大增强

# JDBC的使用

**JDBC使用步骤总结**

  1. 准备数据库驱动包，并添加到项目的依赖中：
  2. 创建数据库连接**Connection**


```java
//  加载JDBC驱动程序：反射，这样调用初始化com.mysql.jdbc.Driver类，即将该类加载到JVM方法区，并执行该类的静态方法块、静态属性。
Class.forName("com.mysql.jdbc.Driver");

// 创建数据库连接
Connection connection = 
DriverManager.getConnection("jdbc:mysql://localhost:3306/test?
user=root&password=root&useUnicode=true&characterEncoding=UTF-8");
```

```java
//MySQL数据连接的URL参数格式如下：
jdbc:mysql://服务器地址:端口/数据库名?参数名=参数值
```

  3. 创建操作命令**Statement**


```java
Statement statement = connection.createStatement();
```

  5. 使用操作命令来执行**SQL**


```java
ResultSet resultSet= statement.executeQuery(
"select id, sn, name, qq_mail, classes_id from student");
```

  7. 处理结果集**ResultSet**


```java
while (resultSet.next()) {
	int id = resultSet.getInt("id"); 
	String sn = resultSet.getString("sn");
	String name = resultSet.getString("name");
	int classesId = resultSet.getInt("classes_id"); 
		System.out.println(String.format("Student: id=%d, sn=%s, name=%s,
classesId=%s", id, sn, name, classesId));
}
```

  9. 释放资源**close**


```java
//关闭结果集
		if (resultSet != null) 
		{ 
			try {
				resultSet.close();
		} catch (SQLException e) { 
			e.printStackTrace();
			}
		}
//关闭命令
        if (statement != null) { 
            try {
                statement.close();
        } catch (SQLException e) { 
                e.printStackTrace();
                }
        }
//关闭连接命令
        if (connection != null) {
            try {
                connection.close();
            } catch (SQLException e) {
                e.printStackTrace();
            }
        }

```

 

# JDBC常用接口和类

**JDBC API**
在**Java  JDBC**编程中对数据库的操作均使用JDK自带的API统一处理，通常与特定数据库的驱动类是完全解耦的。**Java JDBC API** （位于 <code>java.sql </code>包下）

## 数据库连接Connection

**Connection**接口实现类由数据库提供，获取**Connection**对象通常有两种方式：

一种是通过**DriverManager**（驱动管理类）的静态方法获取：

```java
// 加载JDBC驱动程序
Class.forName("com.mysql.jdbc.Driver");

// 创建数据库连接
Connection connection = DriverManager.getConnection(url);
```

一种是通过**DataSource**（数据源）对象获取。实际应用中会使用DataSource对象。

```java
DataSource ds = new MysqlDataSource();
((MysqlDataSource) ds).setUrl("jdbc:mysql://localhost:3306/test"); ((MysqlDataSource) ds).setUser("root");
((MysqlDataSource) ds).setPassword("root"); 
Connection connection = ds.getConnection();
```


以上两种方式的区别是：

 - 1.DriverManager类来获取的Connection连接，是无法重复利用的，每次使用完以后释放资源  时，通过connection.close()都是关闭物理连接。
 - 2.DataSource提供连接池的支持。连接池在初始化时将创建一定数量的数据库连接，这些连接是可以复用的，每次使用完数据库连接，释放资源调用connection.close()都是将Conncetion连接对象回收。

## Statement对象

**Statement**对象主要是将SQL语句发送到数据库中。JDBC API中主要提供了三种Statement对象。
![在这里插入图片描述](https://img-blog.csdnimg.cn/2021031623213358.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQ1NjYxMTI1,size_16,color_FFFFFF,t_70)
最常用的是**PreparedStatemen**t对象，以下对其的总结：
![在这里插入图片描述](https://img-blog.csdnimg.cn/20210316232243261.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQ1NjYxMTI1,size_16,color_FFFFFF,t_70)
主要掌握两种执行SQL的方法：

 - **executeQuery()** 方法执行后返回单个结果集的，通常用于select语句
 - **executeUpdate()**方法返回值是一个整数，指示受影响的行数，通常用于update、insert、delete 语句

## ResultSet对象

ResultSet对象它被称为结果集，它代表符合SQL语句条件的所有行，并且它通过一套getXXX方法提供  了对这些行中数据的访问。
ResultSet里的数据一行一行排列，每行有多个字段，并且有一个记录指针，指针所指的数据行叫做当前数据行，我们只能来操作当前的数据行。我们如果想要取得某一条记录，就要使用ResultSet的next()    方法 ,如果我们想要得到ResultSet里的所有记录，就应该使用while循环。
