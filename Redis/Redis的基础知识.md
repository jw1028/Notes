@[TOC](Redis学习之旅--初始redis)
# 概述
## Redis是什么？
Redis（<code>Re</code>mote <code>Di</code>ctionary <code>S</code>erver）<code>远程字典服务</code>！是一个开源的使用ANSI**C语言**编写、支持网络、可基于内存亦可持久化的日志型、<code>key-value</code>数据库，并提供多种语言的API。是免费和开源的！是当下最热门的NoSQL技术之一！也被人们称之为结构化数据库！Redis会周期性的把更新的数据写入磁盘或者把修改操作写入追加的记录文件，并在此基础上实现master-slave（主从）同步。
## Redis能干嘛？
 - 内存存储、持久化（内存中是断电即失、所以持久化很重要（人rdb、aof））
 - 效率高、可用于告诉缓存
 - 发布订阅系统（消息队列）
 - 地图信息分析
 - 计时器、计数器（浏览量）
 - ......

## Redis的特点
 - 多样的数据类型
 - 持久化
 - 集群
 - 事务
 - .....
 
## 拓展
 - Redis官网：https://redis.io/  
 - Redis中文官网：http://www.redis.cn/

 注意：Wdinow在Github上下载（停更很久了！）
 Redis推荐都是在Linux服务器上搭建的，基于Linux学习！

## 下载
### Windows下载
1.网盘下载链接https://pan.baidu.com/s/1VHiNbmrupYU2yN9D_nybYQ
2.解压到自己的电脑环境上！Redis非常小，只有5M
![在这里插入图片描述](https://img-blog.csdnimg.cn/69c02766fade478691906401be881095.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA6LW1amM=,size_20,color_FFFFFF,t_70,g_se,x_16)
3.开启Redis，双击运行服务即可
![在这里插入图片描述](https://img-blog.csdnimg.cn/780c6398dd95466996332d5fd0e5480b.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA6LW1amM=,size_20,color_FFFFFF,t_70,g_se,x_16)
4，打开客户端进行链接测试
![在这里插入图片描述](https://img-blog.csdnimg.cn/b1b930be98b248e594680210b477da71.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA6LW1amM=,size_20,color_FFFFFF,t_70,g_se,x_16)
### Linux安装

 - 下载安装包！网盘链接https://pan.baidu.com/s/1B7VQauxUXbuspqXpQTMcXQ
   
 - 解压Redis的安装包！程序的/opt目录下

![在这里插入图片描述](https://img-blog.csdnimg.cn/297a332da951484ebb9f1173e472fac0.png)
 - 进入解压后的文件，可以看到我们Redis的配置文件
 ![在这里插入图片描述](https://img-blog.csdnimg.cn/8b2c4d36635d45b6bfff1d18585f8708.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA6LW1amM=,size_20,color_FFFFFF,t_70,g_se,x_16) 
- 基本环境安装
 

```java
yum install gcc-c++
make
make install
```

 - 默认安装路径 /usr/local/bin

![在这里插入图片描述](https://img-blog.csdnimg.cn/1673b8e1b70e4e44985dc06c49477631.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA6LW1amM=,size_20,color_FFFFFF,t_70,g_se,x_16)

 - 拷贝默认配置文件

![在这里插入图片描述](https://img-blog.csdnimg.cn/8b8ea34191764f599df6b2180f44ed2d.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA6LW1amM=,size_20,color_FFFFFF,t_70,g_se,x_16)

 - Redis默认不是后台启动的，需要修改配置文件

![在这里插入图片描述](https://img-blog.csdnimg.cn/90a537df77af4fe6a9b74143ed7e73ab.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA6LW1amM=,size_20,color_FFFFFF,t_70,g_se,x_16)

 - 启动Redis服务

![在这里插入图片描述](https://img-blog.csdnimg.cn/33ac1c590aca434e8b6a5eca86b79243.png)


 - 使用redis-cli测试连接

![在这里插入图片描述](https://img-blog.csdnimg.cn/67882c76076f4e06b9fe4e870cad6458.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA6LW1amM=,size_20,color_FFFFFF,t_70,g_se,x_16)

 - 查看Redis进程是否开启ps -ef|grep redis
![在这里插入图片描述](https://img-blog.csdnimg.cn/a334bcf27d02421ebc92f42e84566889.png)
 - 关闭Redis服务
 ![在这里插入图片描述](https://img-blog.csdnimg.cn/02a417ee72bb44388c0eed620b05ae69.png)
 - 查看进程是否存在
![在这里插入图片描述](https://img-blog.csdnimg.cn/4f13bc8b46de46dc8c83f705c86d34f0.png)
## redis-benchmark(测性能的）

```java
测试：100个并发连接，100000个请求
redis-benchmark -h localhost -p 6379 -c 100 -n 100000
```
![在这里插入图片描述](https://img-blog.csdnimg.cn/baa8cdc88d5a49c19a0ab18b76831fb4.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA6LW1amM=,size_20,color_FFFFFF,t_70,g_se,x_16)
查看分析
![在这里插入图片描述](https://img-blog.csdnimg.cn/c743c32b1ee349369520cd828f3e3c37.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA6LW1amM=,size_20,color_FFFFFF,t_70,g_se,x_16)
![在这里插入图片描述](https://img-blog.csdnimg.cn/9b979cfa48b54a5093d3dd37924f7251.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA6LW1amM=,size_20,color_FFFFFF,t_70,g_se,x_16)
# Redis基础知识
## 相关概念
Redis有16个数据库，默认使用的的是第0个，可以用select命令进行切换
![在这里插入图片描述](https://img-blog.csdnimg.cn/22cf1cddcc8f405385ccd89d40441289.png)
不同的数据库存储不同的值，之间互不干涉
![在这里插入图片描述](https://img-blog.csdnimg.cn/e14b87bc6c094027b598072ef2d6e49f.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA6LW1amM=,size_20,color_FFFFFF,t_70,g_se,x_16)

 - keys * 查看所有的关键字 
 - flushdb清除当前数据库 
 - flushall 清除全部数据库内容

![在这里插入图片描述](https://img-blog.csdnimg.cn/1cb9e71f843b4a5caae01f2931dd8295.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA6LW1amM=,size_20,color_FFFFFF,t_70,g_se,x_16)
## Redis是单线程的！
我们需要明白Redis是很快的，官方表示，Redis是基于内存操作，CPU不是Redis的性能瓶颈，Redis的瓶颈是根据机器的内存和网络带宽有关，既然可以使用单线程，就用单线程来实现了！
Redis是用c语言写的，官方提供的数据为1000000+的QPS，完全不比同样使用key-value的Memecache差！

**Redis为什么单线程还那么快？**

误区1：高性能服务器一定是多线程吗？
误区2：多线程（CPU会进行上下文切换）一定比单线程效率高？

核心：<code>效率：CPU > 内存 > 硬盘</code>  Redis是将所有的数据全部放在内存中，所有说使用单线程去操作效率就是最高的（多线程CPU上下文会切换，会消耗时间）对内存系统来说，如果没有上下文切换效率就是最高的！


