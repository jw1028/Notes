**MySQL**

# 客户端连接服务器

MySQL默认只允许在服务器本机 使用 root 用户登录，要开启 root 用户的远程登录，在MySQL服务器本机执行：

> mysql -u root -p
>

要求输入密码，没有设置密码则直接回车进入MySQL命令行以后，可以看到 mysql>

> – 使用mysql数据库
> use mysql;

> – 更新用户表的root账户，设置为任意ip都可以访问，密码修改为123456
> update user set host="%",authentication_string=password(‘123456’)where user="root";

> – 刷新权限
> flush privileges;
> – 退出
> quit;

# 数据库操作

## 1显示当前的数据库

> show databases；;

## 2创建数据库

语法：

> create database [IF NOT EXISTS] db_name [create_specification [, create_specification] …]
>
> create_specification: [DEFAULT] CHARACTER SET charset_name [DEFAULT]
> COLLATE collation_name

说明：

[] 是可选项
CHARACTER SET: 指定数据库采用的字符集（一般采用utf-8,但在sql中为utf8mb4）
COLLATE: 指定数据库字符集的校验规则
示例：

> 创建名为 db_test1 的数据库
> create database db_test1;

> 如果系统没有 db_test 的数据库，则创建一个使用utf8mb4字符集的 db_test 数据库，如果有则不创建
> create database if not exists db_test character set utf8mb4;

## 3使用数据库

> use 数据库名;

## 4删除数据库

> 语法：
> drop database [if exists] db_name;

说明:
数据库删除以后，内部看不到对应的数据库，里边的表和数据全部被删除

常用数据类型
红色标注的为常用的。

数值类型
分为整型和浮点型：


字符类型


日期类型

### 表的操作（CRUD）

CRUD 即增加(Create)、查询(Retrieve)、更新(Update)、删除(Delete)四个单词的首字母缩写。

> 需要操作数据库中的表时，需要先使用该数据库：
> use db_test;

查看表结构
desc 表名;

示例


创建表
语法：

> create table table_name (
> field1 datatype,
> field2 datatype, field3 datatype
> );

可以使用comment增加字段说明。
示例：

> create table stu_test ( id int,
> name varchar(20) comment ‘姓名’,
> password varchar(50) comment ‘密码’,
> age int,
> sex varchar(1),
> birthday timestamp,
> amout decimal(13,2),
> resume text
> );

删除表
语法格式：

> drop [TEMPORARY] table[if exists] tbl_name [, tbl_name] …
>

示例：

> – 删除 stu_test 表
> drop table stu_test;
> – 如果存在 stu_test 表，则删除 stu_test 表
> drop table if exists stu_test;

接下来进入主题吧

### 新增（Create）

语法：

> insert[into] table_name [(column [, column] …)]
> values(value_list) [, (value_list)] …
> value_list: value, [, value] …

案例：
一个小习惯，在创建前先把之前的表删除。

> – 创建一张学生表
> drop table if exists student;
> create table student (
> id INT,
> sn INT comment ‘学号’,
> name VARCHAR(20) comment ’ 姓 名 ',
> qq_mail VARCHAR(20) comment ‘QQ邮箱’
> );

> 1.单行数据 + 全列插入
>
> – 插入两条记录，value_list 数量必须和定义表的列的数量及顺序一致
> insert into student values(100, 10000, ‘唐三藏’, NULL);
> insert into student values(101, 10001, ‘孙悟空’, ‘11111’);

> 2多行数据 + 指定列插入
> – 插入两条记录，value_list 数量必须和指定列数量及顺序一致
> insert into student (id, sn, name) values
> (102, 20001, ‘曹孟德’),
> (103, 20002, ‘孙仲谋’);

### 查询（Retrieve）

语法：

> select
> [distinct] {* | {column [, column] …} [from table_name]
> [where…]
> [order by column [asc| desc], …] limit…

> 全列查询

> – 通常情况下不建议使用 * 进行全列查询
> – 1. 查询的列越多，意味着需要传输的数据量越大；
> – 2. 可能会影响到索引的使用。
> select* fromexam_result;

> 指定列查询

> – 指定列的顺序不需要按定义表的顺序来
> select id, name, english from exam_result;

> 查询字段为表达式

> – 表达式不包含字段
> select id, name, 10 from exam_result;
> – 表达式包含一个字段
> select id, name, english + 10 from exam_result;
> – 表达式包含多个字段
> select id, name, chinese + math + english from exam_result;



别名 as
为查询结果中的列指定别名，表示返回的结果集中，以别名作为该列的名称，语法：

> selectcolumn [as] alias_name […] fromtable_name;
> – 结果集中，表头的列名=别名
> select id, name, chinese + math + english 总分 fromexam_result;

去重 distinct
使用distinct关键字对某列数据进行去重：

> select distinct math fromexam_result;
>

排序 order by
语法：

> – asc为升序 默认为升序（从小到大）
> – desc为降序（从大到小）
> select… from table_name [where…] order by column [asc|desc], […];

注意
1.没有 ORDER BY 子句的查询，返回的顺序是未定义的，永远不要依赖这个顺序
2.NULL 数据排序，视为比任何值都小，升序出现在最上面，降序出现在最下面
3.可以使用表达式及别名排序

4.可以对多个字段进行排序，排序优先级随书写顺序

条件查询 where
比较运算符

逻辑运算符

注：
1.where条件可以使用表达式，但不能使用别名。
2.AND的优先级高于OR，在同时使用时，需要使用小括号()包裹优先执行的部分
分页查询：limit
语法：

> – 起始下标为 0
> – 从 0 开始，筛选 n 条结果
> select… from table_name [where…] [order by…] limit n;
> – 从 s 开始，筛选 n 条结果
> select… fromtable_name [where …] [order by…] limit s, n;
> – 从 s 开始，筛选 n 条结果，比第二种用法更明确，建议使用
> select … from table_name [where…] [order by …] limit n offset s;</code?

案例：按 id 进行分页，每页 3 条记录，分别显示 第 1、2、3 页

> – 第 1 页
> select id, name, math, english, chinese from exam_result order by id limit 3 offset 0;
> – 第 2 页
> select id, name, math, english, chinese from exam_result order by id limit 3 offset 3;
> – 第 3 页，如果结果不足 3 个，不会有影响 如果n越界，不会有影响
> select id, name, math, english, chinese from exam_result order by id limit 3 offset 6;

### 修改（Update）

语法：

> update table_name set column = expr [, column = expr …] [where …] [order by…] [limit…]
>

案例：

> – 将孙悟空同学的数学成绩变更为 80 分
> update exam_result set math = 80 where name = ‘孙悟空’;

### 删除（Delete）

语法：

> delete from table_name [where…] [order by…] [limit…]
>

案例：

> – 删除孙悟空同学的考试成绩
> delete fromexam_result where name = ‘孙悟空’;
> – 删除整表数据(删除的是整张表的数据，但是表还在，删除表的话用drop）
> delete from for_delete;
>