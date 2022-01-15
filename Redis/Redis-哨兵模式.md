@[TOC](Redis学习之旅--哨兵模式)
引入：结合上节课的主从复制，由于是我们手动选择主机所以不方便，所以引入了哨兵模式（手动选择主句）
# 相关概念
主从切换技术的方法是：当主服务器宕机后，需要手动把一台从服务器切换为主服务器，这就需要人工干预，费事费力，还会造成一段时间内服务不可用。这不是一种推荐的方式，更多时候，我们优先考虑哨兵模式。Redis从2.8开始正式提供了Sentinel（哨兵） 架构来解决这个问题。
**<code>谋朝篡位的自动版**，能够后台监控主机是否故障，如果故障了根据投票数自动将从库转换为主库。
哨兵模式是一种特殊的模式，首先Redis提供了哨兵的命令，哨兵是一个独立的进程，作为进程，它会独立运行。其原理是哨兵通过发送命令，等待Redis服务器响应，从而监控运行的多个Redis实例


![在这里插入图片描述](https://img-blog.csdnimg.cn/ccc81430170c4c1385db67e6303ee667.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA6LW1amM=,size_20,color_FFFFFF,t_70,g_se,x_16)
这里的哨兵有两个作用:

 - 通过发送命令，让Redis服务器返回监控其运行状态，包括主服务器和从服务器。
 - 当哨兵监测到master宕机，会自动将slave切换成master，然后通过发布订阅模式通知其他的从服务器，修改配置文件，让它们切换主机。

然而一个哨兵进程对Redis服务器进行监控，可能会出现问题，为此，我们可以使用多个哨兵进行监控。各个哨兵之间还会进行监控，这样就形成了多哨兵模式。
![在这里插入图片描述](https://img-blog.csdnimg.cn/b775c983c50943f28553f8b2333f7c08.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA6LW1amM=,size_20,color_FFFFFF,t_70,g_se,x_16)
假设主服务器宕机，哨兵1先检测到这个结果，系统并不会马上进行failover过程，仅仅是哨兵1主观的认为主服务器不可用，这个现象成为**主观下线**。当后面的哨兵也检测到主服务器不可用，并且数量达到一定值时，那么哨兵之间就会进行一次投票，投票的结果由一个哨兵发起，进行failover[故障转移]操作。切换成功后，就会通过发布订阅模式，让各个哨兵把自己监控的从服务器实现切换主机，这个过程称为客观下线。

#	测试
我们目前的状态是 一主二从！
1、配置哨兵配置文件 sentinel.conf

```bash
# sentinel monitor 被监控的名称 host port 1 
sentinel monitor myredis 127.0.0.1 6379 1
```
后面的这个数字1，代表主机挂了，slave投票看让谁接替成为主机，票数最多的，就会成为主机！
![在这里插入图片描述](https://img-blog.csdnimg.cn/33a0ee3c6e664b71843dc83cab25d6cc.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA6LW1amM=,size_20,color_FFFFFF,t_70,g_se,x_16)

![在这里插入图片描述](https://img-blog.csdnimg.cn/72cf5a7169af4337b7437b10f22f2eb9.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA6LW1amM=,size_20,color_FFFFFF,t_70,g_se,x_16)
2、启动哨兵！
![在这里插入图片描述](https://img-blog.csdnimg.cn/275e5e01a6ed4683a618d6f590d01f94.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA6LW1amM=,size_20,color_FFFFFF,t_70,g_se,x_16)
3，如果Master 节点断开了，这个时候就会从从机中随机选择一个服务器！ （这里面有一个投票算法！）
![在这里插入图片描述](https://img-blog.csdnimg.cn/aac81a56b4c14159935c8f15cf00dfcb.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA6LW1amM=,size_20,color_FFFFFF,t_70,g_se,x_16)

![在这里插入图片描述](https://img-blog.csdnimg.cn/e967914497f846e9b71fff185b181cd6.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA6LW1amM=,size_20,color_FFFFFF,t_70,g_se,x_16)

![在这里插入图片描述](https://img-blog.csdnimg.cn/b6b4dcb7df1949edaef499988ca48273.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA6LW1amM=,size_20,color_FFFFFF,t_70,g_se,x_16)
4.如果主机此时回来了，只能归并到新的主机下，当做从机，这就是哨兵模式的规则！
![在这里插入图片描述](https://img-blog.csdnimg.cn/bf198bb8b31f4433b95c8ab50c83f038.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA6LW1amM=,size_20,color_FFFFFF,t_70,g_se,x_16)

![在这里插入图片描述](https://img-blog.csdnimg.cn/8055c1dbdfb842e5aa6bf8022067f928.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA6LW1amM=,size_20,color_FFFFFF,t_70,g_se,x_16)
![在这里插入图片描述](https://img-blog.csdnimg.cn/cd667f5e1c1245a0a7251af39fce51fe.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA6LW1amM=,size_20,color_FFFFFF,t_70,g_se,x_16)
# 优缺点

优点：

 - 1、哨兵集群，基于主从复制模式，所有的主从配置优点，它全有
 - 2、 主从可以切换，故障可以转移，系统的可用性就会更好
 - 3、哨兵模式就是主从模式的升级，手动到自动，更加健壮！

缺点：

 - 1、Redis 不好啊在线扩容的，集群容量一旦到达上限，在线扩容就十分麻烦！
 - 2、实现哨兵模式的配置其实是很麻烦的，里面有很多选择！

# 相关配置
![在这里插入图片描述](https://img-blog.csdnimg.cn/8af1d2fd42d84b4f94c76be746bcd31f.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA6LW1amM=,size_20,color_FFFFFF,t_70,g_se,x_16)

