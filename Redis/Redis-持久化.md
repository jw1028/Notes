@[TOC](Redis学习之旅--持久化)
**Redis是内存数据库**，如归不将内存中的数据库状态保存到磁盘，那么一旦服务器进程退出，服务器中的数据库状态也会消失，所以Redis提供了持久化的功能。

# RDB（Redis DataBase）
## rdb是什么
在主从复制中，rdb就是备用了！从机上面！
![在这里插入图片描述](https://img-blog.csdnimg.cn/38f49d1eee854cf0bad69e84ab88b4eb.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA6LW1amM=,size_20,color_FFFFFF,t_70,g_se,x_16)

 - <code>核心：在指定的时间间隔内将内存中的数据集快照写入磁盘，也就是行话讲的Snapshot快照，它恢复时是将快照文件直接读到内存里。</code>
 - 详细过程：Redis会单独创建（fork）一个子进程来进行持久化，会先将数据写入到一个临时文件中，待持久化过程都结束了，再用这个临时文件替换上次持久化好的文件。整个过程中，主进程是不进行任何IO操作的。这就确保了极高的性能。如果需要进行大规模数据的恢复，且对于数据恢复的完整性不是非常敏感，那RDB方式要比AOF方式更加的高效。RDB的缺点是最后一次持久化后的数据可能丢失。我们默认的就是
   RDB，一般情况下不需要修改这个配置！
 - 有时候在生产环境我们会将这个文件进行备份！
 - rdb保存的文件是<code>dump.rdb</code> 都是在我们的配置文件中快照中进行配置的！

![在这里插入图片描述](https://img-blog.csdnimg.cn/7cbf3ae7dc4b440d957971500e842838.png)
测试：
![在这里插入图片描述](https://img-blog.csdnimg.cn/dd7bfae3a33f4a9f8710db73cbe4098f.png)

 - 先将dump.rdb文件删除，然后一分钟内修改次，查看dump.rdb是否被生成，关闭Redis后查看设置的值是否存在

![在这里插入图片描述](https://img-blog.csdnimg.cn/4a4d04b8733d44ef9df988a394542970.png)
![在这里插入图片描述](https://img-blog.csdnimg.cn/97a84493f98d4910a51bcee789d78f3b.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA6LW1amM=,size_20,color_FFFFFF,t_70,g_se,x_16)
![在这里插入图片描述](https://img-blog.csdnimg.cn/85bebfc06ffe444e81a40cb070e4bd56.png)
![在这里插入图片描述](https://img-blog.csdnimg.cn/af5a0e6016224f27927b9551a3d8fc6c.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA6LW1amM=,size_20,color_FFFFFF,t_70,g_se,x_16)

 - 使用flushall生成dump.rdb文件
![在这里插入图片描述](https://img-blog.csdnimg.cn/9513638f999744629a41386be1a3511f.png)
![在这里插入图片描述](https://img-blog.csdnimg.cn/0420e7a7a8eb4441869f659000fa3c5f.png)
![在这里插入图片描述](https://img-blog.csdnimg.cn/a5623ec16d534aee889dcc493823e5d3.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA6LW1amM=,size_20,color_FFFFFF,t_70,g_se,x_16)

## 触发机制

 - 1、save的规则满足的情况下，会自动触发rdb规则
 - 2、执行 flushall 命令，也会触发我们的rdb规则！
 - 3、退出redis，也会产生 rdb 文件！

## 如何恢复rdb文件

 - 1、只需要将rdb文件放在我们redis启动目录就可以，redis启动的时候会自动检查dump.rdb 恢复其中的数据！
 - 2、查看需要存在的位置

```bash
127.0.0.1:6379> config get dir 
1) "dir" 
2) "/usr/local/bin" # 如果在这个目录下存在 dump.rdb 文件，启动就会自动恢复其中的数据
```
## 优缺点
优点：

 - 1、适合大规模的数据恢复！
 - 2、对数据的完整性要不高！（60分钟5次修改，如果59分钟的时候宕机了，最后一次的修改的数据就获取不到了）
 
缺点
 - 1、需要一定的时间间隔进程操作！如果redis意外宕机了，这个最后一次修改数据就没有的了！
 - 2、fork进程的时候，会占用一定的内容空间！！

# AOF（Append Only File）
## aof是什么

 - 原理图

![在这里插入图片描述](https://img-blog.csdnimg.cn/7db646cd80844c1ba0b9a237a229b0ce.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA6LW1amM=,size_20,color_FFFFFF,t_70,g_se,x_16)

 - <code>核心：将我们的所有命令都记录下来，history，恢复的时候就把这个文件全部在执行一遍！
 - 以日志的形式来记录每个写操作，将Redis执行过的所有指令记录下来（读操作不记录），只许追加文件
 - 但不可以改写文件，redis启动之初会读取该文件重新构建数据，换言之，redis重启的话就根据日志文件的内容将写指令从前到后执行一次以完成数据的恢复工作
 - <code>aof保存的是 appendonly.aof 文件
 
## 相关配置
 - 是否开启aof

![在这里插入图片描述](https://img-blog.csdnimg.cn/c47f87849a384545a03a9edbf75a6531.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA6LW1amM=,size_20,color_FFFFFF,t_70,g_se,x_16)


![在这里插入图片描述](https://img-blog.csdnimg.cn/48a84c8391c045008898414f8af6654c.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA6LW1amM=,size_20,color_FFFFFF,t_70,g_se,x_16)
默认是不开启的，我们需要手动进行配置！我们只需要将 appendonly 改为yes就开启了 aof！
重启，redis 就可以生效了！
![在这里插入图片描述](https://img-blog.csdnimg.cn/56832a9c91e6403ab3e6203b6fe6af6d.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA6LW1amM=,size_20,color_FFFFFF,t_70,g_se,x_16)
![在这里插入图片描述](https://img-blog.csdnimg.cn/11d6610e4910490cb7b1f2678998e8da.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA6LW1amM=,size_20,color_FFFFFF,t_70,g_se,x_16)


 - 一些写入的策略

![在这里插入图片描述](https://img-blog.csdnimg.cn/dddd975e3b174cee8b97ae328c267160.png)
![在这里插入图片描述](https://img-blog.csdnimg.cn/f82a9b585f9240a8b25efcfce901b81a.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA6LW1amM=,size_20,color_FFFFFF,t_70,g_se,x_16)


 - 重写的规则
 aof 默认就是文件的无限追加，文件会越来越大！
 如果 aof 文件大于 64m，太大了！ fork一个新的进程来将我们的文件进行重写！
![在这里插入图片描述](https://img-blog.csdnimg.cn/90a7ecf7fc3743459d32b67135670622.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA6LW1amM=,size_20,color_FFFFFF,t_70,g_se,x_16)


## 容错机制
如果这个 aof 文件有错位，这时候 redis 是启动不起来的吗，我们需要修复这个aof文件
redis 给我们提供了一个工具 redis-check-aof --fix

 - 修改appendonly.aof

![在这里插入图片描述](https://img-blog.csdnimg.cn/66997a58f8014823828c1162f0e330b5.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA6LW1amM=,size_20,color_FFFFFF,t_70,g_se,x_16)

 - 重启服务报错

![在这里插入图片描述](https://img-blog.csdnimg.cn/19a4e706fb4d43828f69a318de4a7d32.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA6LW1amM=,size_20,color_FFFFFF,t_70,g_se,x_16)

 - 用redis-check-aof --fix工具修复

![在这里插入图片描述](https://img-blog.csdnimg.cn/5bc95d8f97474a579b5fa33f886a5d76.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA6LW1amM=,size_20,color_FFFFFF,t_70,g_se,x_16)

 - 查看修复结果

![在这里插入图片描述](https://img-blog.csdnimg.cn/89d361cbf1174b53b7c8f6d4622e6bbc.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA6LW1amM=,size_20,color_FFFFFF,t_70,g_se,x_16)
## 优缺点

```bash
# appendfsync always # 每次修改都会 sync。消耗性能 
appendfsync everysec # 每秒执行一次 sync，可能会丢失这1s的数据！
# appendfsync no # 不执行 sync，这个时候操作系统自己同步数据，速度最快！
```
优点：

 - 1、每一次修改都同步，文件的完整会更加好！
 - 2、每秒同步一次，可能会丢失一秒的数据
 - 3、从不同步，效率最高的！

缺点：

 - 1、相对于数据文件来说，aof远远大于 rdb，修复的速度也比 rdb慢！
 - 2、Aof 运行效率也要比 rdb 慢，所以我们redis默认的配置就是rdb持久化！

# 扩展
1、RDB 持久化方式能够在指定的时间间隔内对你的数据进行快照存储
2、AOF 持久化方式记录每次对服务器写的操作，当服务器重启的时候会重新执行这些命令来恢复原始的数据，AOF命令以Redis 协议追加保存每次写的操作到文件末尾，Redis还能对AOF文件进行后台重写，使得AOF文件的体积不至于过大。
<code>3、只做缓存，如果你只希望你的数据在服务器运行的时候存在，你也可以不使用任何持久化

4、同时开启两种持久化方式

 - 在这种情况下，当redis重启的时候会优先载入AOF文件来恢复原始的数据，因为在通常情况下AOF文件保存的数据集要比RDB文件保存的数据集要完整。
 - RDB的数据不实时，同时使用两者时服务器重启也只会找AOF文件，那要不要只使用AOF呢？作者建议不要，因为RDB更适合用于备份数据库（AOF在不断变化不好备份），快速重启，而且不会有AOF可能潜在的Bug，留着作为一个万一的手段。

5、性能建议

 - 因为RDB文件只用作后备用途，建议只在Slave上持久化RDB文件，而且只要15分钟备份一次就够了，只保留 save 900 1
   这条规则。
 - 如果Enable AOF
   ，好处是在最恶劣情况下也只会丢失不超过两秒数据，启动脚本较简单只load自己的AOF文件就可以了，代价一是带来了持续的IO，二是AOF
   rewrite 的最后将 rewrite 过程中产生的新数据写到新文件造成的阻塞几乎是不可避免的。只要硬盘许可，应该尽量减少AOFrewrite的频率，AOF重写的基础大小默认值64M太小了，可以设到5G以上，默认超过原大小100%大小重写可以改到适当的数值。
 - 如果不Enable AOF ，仅靠 Master-Slave Repllcation实现高可用性也可以，能省掉一大笔IO，也减少了rewrite时带来的系统波动。代价是如果Master/Slave同时倒掉，会丢失十几分钟的数据，启动脚本也要比较两个 Master/Slave 中的 RDB文件，载入较新的那个，微博就是这种架构。
