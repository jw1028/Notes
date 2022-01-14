@[TOC](Redis学习之旅--事务)
# Redis中事务的一些特性

 - Redis事务的本质：一组命令的集合！一个事务中所有的命令都会被序列化，在事务执行过程中，会按照顺序执行！
 - 一次性、顺序性、排他性！执行一系列的命令！
 - <code>Redis事务没有隔离级别的概念！
 - <code>Redis单条命令保存原子性，但是事务不保证原子性！
 - 所有命令在事务中，并没有直接被执行！只有发起执行命令的时候才会执行！

# 事务的相关命令
开始事务（multi）
命令入队（.....）
执行事务(执行事务)

 - 正常执行事务！

```bash
127.0.0.1:6379> multi	#开启事务
OK
#命令入队
127.0.0.1:6379> set k1 v1
QUEUED
127.0.0.1:6379> set k2 v2
QUEUED
127.0.0.1:6379> get k2
QUEUED
127.0.0.1:6379> set k3 v3
QUEUED
127.0.0.1:6379> exec	#执行事务
1) OK
2) OK
3) "v2"
4) OK

```

 - 放弃事务

```bash
127.0.0.1:6379> multi	#开启事务
OK
127.0.0.1:6379> set k1 v1
QUEUED
127.0.0.1:6379> set k2 v2
QUEUED
127.0.0.1:6379> set k4 v4
QUEUED
127.0.0.1:6379> discard	#取消事务
OK
127.0.0.1:6379> get k4	#事务队列中的命令都不会被执行！
(nil)

```

 - 编译型异常（代码有问题！命令有错！）事务中所有的命令都不会被执行！

```bash
127.0.0.1:6379> multi
OK
127.0.0.1:6379> set k1 v1
QUEUED
127.0.0.1:6379> set k2 v2
QUEUED
127.0.0.1:6379> set k3 v3
QUEUED
127.0.0.1:6379> getset k3	#错误的命令（java中没有）
(error) ERR wrong number of arguments for 'getset' command
127.0.0.1:6379> set k4 v4
QUEUED
127.0.0.1:6379> exec	#执行事务报错
(error) EXECABORT Transaction discarded because of previous errors.
127.0.0.1:6379> get k4	#所有的命令都不会被执行！
(nil)
```

 - 运行时异常（1/0），如果事务队列中存在语法行，那么执行命令的时候，其他命令是可以正常执行的，错误命令抛出异常

```bash
127.0.0.1:6379> set k1 "v1"
OK
127.0.0.1:6379> multi
OK
127.0.0.1:6379> incr k1	#执行的时候会报错（string不能加1）
QUEUED
127.0.0.1:6379> set k2 v2
QUEUED
127.0.0.1:6379> get k2
QUEUED
127.0.0.1:6379> exec
1) (error) ERR value is not an integer or out of range
2) OK
3) "v2"
127.0.0.1:6379> get k2
"v2"

```

# 监控 Watch
悲观锁：

 - 很悲观，认为什么时候都会出现问题，无论做什么都会加锁！

乐观锁：

 - 很乐观，认为什么时候都不会出现问题，所以不会上锁！更新数据的时候去判断一下，在此期间是否有人修改过这个数据
 - 获取version
 - 更新的时候比较version


Redis监视测试

 - 正常执行成功

```python
127.0.0.1:6379> flushdb
OK
127.0.0.1:6379> set money 100
OK
127.0.0.1:6379> set out 0
OK
127.0.0.1:6379> watch money 	#监视money
OK
127.0.0.1:6379> multi	
OK
127.0.0.1:6379> decrby money 20
QUEUED
127.0.0.1:6379> incrby out 20
QUEUED
127.0.0.1:6379> exec	#事务正常结束，数据期间没有发生变动，这个时候正常执行成功！
1) (integer) 80
2) (integer) 20

```

 - 测试多线程修改值，使用watch可以当做Redis的乐观锁来操作

```python
#客户端1在未执行前客户端2对money进行了修改
127.0.0.1:6379> watch money #监视money
OK
127.0.0.1:6379> multi
OK
127.0.0.1:6379> decrby money 10
QUEUED
127.0.0.1:6379> incrby out 10
QUEUED
127.0.0.1:6379> exec	#执行之前，另一个线程修改了我们的值，这个时候就会导致事务执行失败！
(nil)
#客户端2对money进行了修改
[root@VM-0-13-centos bin]# redis-cli
127.0.0.1:6379> get money
"80"
127.0.0.1:6379> set money 10000
OK
```
![在这里插入图片描述](https://img-blog.csdnimg.cn/1aaad53a43a34c188226e6d84c3fcee6.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA6LW1amM=,size_20,color_FFFFFF,t_70,g_se,x_16)

