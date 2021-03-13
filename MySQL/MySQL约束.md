# 约束

# 约束类型

 - **<code>not null</code>** - 指示某列不能存储 NULL 值。

创建表时，可以指定某列不为空：

> -- 重新设置学生表结构
> ==DROP TABLE IF EXISTS student;
> CREATE TABLE student (
>  id INT <code>NOT NULL</code>,
> sn INT,
> name VARCHAR(20),
> qq_mail VARCHAR(20)
> );==

 - <code>unique</code>- 保证某列的每行必须有唯一的值。

 指定sn列为唯一的、不重复的：

> -- 重新设置学生表结构
> ==DROP TABLE IF EXISTS student;
> CREATE TABLE student ( 
> id INT NOT NULL, 
> sn INT <code>UNIQUE</code>, 
> name VARCHAR(20),
> qq_mail VARCHAR(20)
> );==


 - <code>default</code> - 规定没有给列赋值时的默认值。

指定插入数据时，name列为空，默认值unkown：

> -- 重新设置学生表结构
> ==DROP TABLE IF EXISTS student;
> CREATE TABLE student ( 
> id INT NOT NULL,
>  sn INT UNIQUE,
> name VARCHAR(20) <code>DEFAULT</code> 'unkown', 
> qq_mail VARCHAR(20)
> );==

 - <code>primary key</code> (not null和unique的结合）确保某列（或两个列多个列的结合）**有唯一标识**，有助于更容易更快速地找到表中的一个特定的记录。

指定id列为主键：

> -- 重新设置学生表结构
> ==DROP TABLE IF EXISTS student;
> CREATE TABLE student (
> id INT NOT NULL <code>PRIMARY KEY</code>, 
> sn INT UNIQUE,
> name VARCHAR(20) DEFAULT 'unkown', 
> qq_mail VARCHAR(20)
> );==

对于整数类型的主键，常配搭自增长**auto_increment**来使用。插入数据对应字段不给值时，**使用最大值+1**。

> -- 主键是 NOT NULL 和 UNIQUE 的结合，可以不用 NOT NULL 
> ==id INT <code>PRIMARY KEY auto_increment</code>==,


 - <code>foreign key</code>- 保证一个表中的数据**匹配**另一个表中的值的**参照完整性**。

 外键用于**关联**其他表的主键或唯一键，

 语法：

> <code>foreign key</code> (字段名) <code>references</code> 主表(列)

案例：
创建班级表**classes，id为**主键：

> -- 创建班级表，有使用MySQL关键字作为字段时，需要使用``来标识
> ==DROP TABLE IF EXISTS classes;
> CREATE TABLE classes (
> id INT <code>PRIMARY KEY</code> auto_increment, 
> name VARCHAR(20),
> `desc` VARCHAR(100)
> );==

创建学生表**student**，一个学生对应一个班级，一个班级对应多个学生。使用**id**为主键，
**classes_id**为外键，关联班级表**id**

> -- 重新设置学生表结构
> ==DROP TABLE IF EXISTS student;
> CREATE TABLE student (
> id INT PRIMARY KEY auto_increment, 
> sn INT UNIQUE,
> name VARCHAR(20) DEFAULT 'unkown', 
> qq_mail VARCHAR(20),
> classes_id int,
> <code>FOREIGN KEY </code>(classes_id) <code>REFERENCES</code> classes(id)
> );==

 - <code>check</code>- 保证列中的值符合指定的条件。

 MySQL使用时不报错，但忽略该约束：


> ==drop table if exists test_user; 
> create table test_user (
> id int,
> name varchar(20), 
> sex varchar(1),
> <code>check</code> (sex ='男' or sex='女')
> );==

# 表的设计

一对一
![在这里插入图片描述](https://img-blog.csdnimg.cn/20210311002001736.png)
一对多
![在这里插入图片描述](https://img-blog.csdnimg.cn/20210311002020844.png)
多对多
![在这里插入图片描述](https://img-blog.csdnimg.cn/20210311002052558.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQ1NjYxMTI1,size_16,color_FFFFFF,t_70)
创建学生课程中间表，考试成绩表

> -- 创建课程学生中间表：考试成绩表
> ==DROP TABLE IF EXISTS score;
> CREATE TABLE score (
> id INT PRIMARY KEY auto_increment, 
> score DECIMAL(3, 1),
> student_id int, 
> course_id int,
> FOREIGN KEY (student_id) REFERENCES student(id),
>  FOREIGN KEY (course_id) REFERENCES course(id)
> );==

# 查询

## 聚合查询

常见的统计总数、计算平局值等操作，可以使用聚合函数来实现，常见的聚合函数有：

 - **聚合函数**
   ![在这里插入图片描述](https://img-blog.csdnimg.cn/20210311002454101.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQ1NjYxMTI1,size_16,color_FFFFFF,t_70)

 - **group by子句**

**SELECT** 中使用 **GROUP BY** 子句可以对指定列进行分组查询。需要满足：使用 **GROUP BY** 进行分组查询时，<code>**SELECT** 指定的字段必须是“分组依据字段”</code>，其他字段若想出现在**SELEC**T 中则必须包含在聚合函数中。

 - **having**

**GROUP BY** 子句进行分组以后，需要对分组结果再进行条件过滤时，不能使用 **WHERE** 语句(where和聚合函数不能一起使用)，而需要用**HAVING**

## 联合查询

实际开发中数据往往来自不同的表，所以需要<code>**多表联合查询**</code>。多表查询是对多张表的数据取<code>**笛卡尔积**</code>：
注意：关联查询可以对关联表使用别名。
![在这里插入图片描述](https://img-blog.csdnimg.cn/20210312004226516.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQ1NjYxMTI1,size_16,color_FFFFFF,t_70)

 - **内连接**
   ![在这里插入图片描述](https://img-blog.csdnimg.cn/20210312010400382.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQ1NjYxMTI1,size_16,color_FFFFFF,t_70)


>==select 字段 from 表1 别名1 <code>[inner] join</code> 表2 别名2 <code>on</code> 连接条件 <code>and</code> 其他条件; 
>select 字段 from 表1 别名1,表2 别名2 <code>where</code> 连接条件 <code>and</code> 其他条件;==

 - **外连接**
   外连接分为**左外连接**和**右外连接**。如果联合查询，左侧的表完全显示我们就说是左外连接；右侧的表完  全显示我们就说是右外连接。
    ![在这里插入图片描述](https://img-blog.csdnimg.cn/20210312010419488.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQ1NjYxMTI1,size_16,color_FFFFFF,t_70)

![在这里插入图片描述](https://img-blog.csdnimg.cn/20210312010444689.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQ1NjYxMTI1,size_16,color_FFFFFF,t_70)

> -- 左外连接，表1完全显示
> ==select 字段名	from 表名1 <code>left join</code> 表名2 <code>on</code> 连接条件;==
> -- 右外连接，表2完全显示
> ==select 字段 from 表名1 <code>right join</code> 表名2 <code>on</code>	连接条件;==

 - **自连接**

 自连接是指在<code>**同一张表**</code>连接自身进行查询。

 - **子查询**

子查询是指**嵌入**在**其他sql语句中**的**select**语句，也叫**嵌套查询**  

1.<code>[NOT] IN</code>关键字：

> -- 使用IN
> ==select * from score where course_id <code>in</code> (select id from course where name='语文' or name='英文');==
> -- 使用 NOT IN
> ==select * from score where course_id <code>not in</code> (select id from course where name!='语文' and name!='英文');==

2.<code>[NOT] EXISTS</code>关键字：(比较复杂，我们一般采用in）

> -- 使用 EXISTS
> ==select * from score sco where <code>exists</code> (select sco.id from course cou where (name='语文' or name='英文') and cou.id = sco.course_id);==
> -- 使用 NOT EXISTS
> ==select * from score sco where <code>not exists</code> (select sco.id from course cou where (name!='语文' and name!='英文') and cou.id = sco.course_id);==

 - **合并查询**

 在实际应用中，为了合并多个select的执行结果，可以使用集合操作符 union，union all。使用UNION和UNION ALL时，前后查询的结果集中，字段需要一致。

 1.<code> union

该操作符用于取得两个结果集的并集。当使用该操作符时，**会自动去掉结果集中的重复行。**

2.<code>union all</code>
该操作符用于取得两个结果集的并集。当使用该操作符时，**不会去掉结果集中的重复行。** 

## SQ中关键字的执行顺序

<code>SQL查询中各个关键字的执行先后顺序:</code> f**rom > on> join > where > group by > with > having > select > distinct > order by > limit**
