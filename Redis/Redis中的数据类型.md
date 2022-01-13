@[TOC](Redis学习之旅--数据类型)
# Redis-Key
以下是常见的Redis-Key的命令

```python
127.0.0.1:6379> keys * #查看所有的key
(empty list or set)
127.0.0.1:6379> set name zjc #设置key
OK
127.0.0.1:6379> set age 1
OK
127.0.0.1:6379> keys * 
1) "name"
2) "age"
127.0.0.1:6379> exists name #查看key是否存在
(integer) 1
127.0.0.1:6379> exists name1
(integer) 0
127.0.0.1:6379> move name 1	#移除key
(integer) 1
127.0.0.1:6379> keys *
1) "age"
127.0.0.1:6379> expire name 10 #设置key的到期时间
(integer) 0
127.0.0.1:6379> ttl name	#查看key的到期时间
(integer) -2
127.0.0.1:6379> ttl name
(integer) -2
127.0.0.1:6379> get name 
(nil)
127.0.0.1:6379> type name	#查看key的类型
none
127.0.0.1:6379> type age
string

```
更多命令可以查看Redis的文档：http://www.redis.cn/commands.html
# String（字符串）

```python
127.0.0.1:6379> set key1 v1  #设置值
OK
127.0.0.1:6379> get key1	#获得值
"v1"
127.0.0.1:6379> keys *	#获得所有的key
1) "key1"
127.0.0.1:6379> exists key1	#判断一个key是否存在
(integer) 1
127.0.0.1:6379> append key1 "hello" #追加字符串，若不存在则新set 可以去存储
(integer) 7
127.0.0.1:6379> get key1
"v1hello"
127.0.0.1:6379> strlen key1 #获取字符串的长度
(integer) 7
127.0.0.1:6379> append key2 "zjc"
(integer) 3
127.0.0.1:6379> keys *
1) "key1"
2) "key2"

=========================================
#自增、自减
127.0.0.1:6379> set views 0 #设置初始值为0
OK
127.0.0.1:6379> get views
"0"
127.0.0.1:6379> incr views	 #自增1
(integer) 1
127.0.0.1:6379> get views
"1"
127.0.0.1:6379> decr views 	#自减1
(integer) 0
127.0.0.1:6379> get views
"0"
127.0.0.1:6379> incrby views 10		#一次增加指定的步长
(integer) 10
127.0.0.1:6379> get views
"10"
127.0.0.1:6379> decrby views 5	#一次减少指定的步长
(integer) 5
127.0.0.1:6379> get views
"5"


=============================================

#字符串范围 range

127.0.0.1:6379> set key1 "hello,zjcjw" #设置key1的值
OK
127.0.0.1:6379> get key1  #得到key1的值
"hello,zjcjw"
127.0.0.1:6379> getrange key1 0 3 #截取字符串 [0,3]
"hell"
127.0.0.1:6379> getrange key1 0 -1 #获取全部的字符串和get key1一样
"hello,zjcjw"

#替换
127.0.0.1:6379> set key2 abcdefg
OK
127.0.0.1:6379> get key2
"abcdefg"
127.0.0.1:6379> setrange key2 1 xxx #替换指定位置开始的字符串
(integer) 7
127.0.0.1:6379> get key2
"axxxefg"

=============================================
#setex(set with expire) 设置过期时间
#setnx(set if not exist) 不存在设置（在分布式锁中会常常用到）

127.0.0.1:6379> setex key3 30 "hello" #设置key3的值为hello，30秒后过期
OK
127.0.0.1:6379> ttl key3
(integer) 25
127.0.0.1:6379> get key3
"hello"
127.0.0.1:6379> setnx key4 "redis" #如果key4不存在，创建key4（1表示成功）
(integer) 1
127.0.0.1:6379> keys *
1) "key4"
2) "key1"
3) "key2"
127.0.0.1:6379> ttl key3
(integer) -2
127.0.0.1:6379> setnx key4 "zjc"	#如果key4存在，创建失败（0表示失败）
(integer) 0


======================================================
mset 设置多个set值
mget 获取多个set值
127.0.0.1:6379> mset k1 v1 k2 v2 k3 v3  #同时设置多个值
OK
127.0.0.1:6379> keys *
1) "k3"
2) "k2"
3) "k1"
127.0.0.1:6379> mget k1 k2 k3	#同时获取多个值
1) "v1"
2) "v2"
3) "v3"
127.0.0.1:6379> msetnx k1 v1 k4 v4  #msetnx是一个原子性的操作，要么一起成功，要么一起失败！
(integer) 0
127.0.0.1:6379> get k4
(nil)
======================================
对象

127.0.0.1:6379> set user:1{name:zjc,age:3} #设置一个user：1对象  值为json字符老保存做一对象
(error) ERR wrong number of arguments for 'set' command
127.0.0.1:6379> set user:1 {name:zjc,age:3}
OK
127.0.0.1:6379> get user:1
"{name:zjc,age:3}"
127.0.0.1:6379> mset user:2:name jw user:2:age 16
OK
127.0.0.1:6379> mget user:2:name user:2:age
1) "jw"
2) "16"
127.0.0.1:6379> 

======================================
getset #先get在set
127.0.0.1:6379> getset db redis  #如果不存在值，则返回nil
(nil)
127.0.0.1:6379> get db
"redis"
127.0.0.1:6379> getset db mongdb #如果存在值，获取原来的值，并设置新的值
"redis"
127.0.0.1:6379> get db
"mongdb"

```

String类似的使用场景：value除了是我们的字符串还可以是我们的数字！

 - ·计数器 
 - ·统计多单位的数量
 - ·粉丝数 ·
 - 对象缓存存储

# list（列表）
在Redis里面，我们可以将list玩成栈、队列、阻塞队列！
所有的list命令都是以l开头的

```python
#push
127.0.0.1:6379> lpush list 1 #将一个值或者多个值插入到链表的头部（左）
(integer) 1
127.0.0.1:6379> lpush list 2
(integer) 2
127.0.0.1:6379> lpush list 3
(integer) 3
127.0.0.1:6379> lrange list 0 1 #获取指定区间的值
1) "3"
2) "2"
127.0.0.1:6379> lrange list 0 -1  #获取list中的所有值
1) "3"
2) "2"
3) "1"
127.0.0.1:6379> rpush list 4
(integer) 4
127.0.0.1:6379> lrange list 0 -1 #将一个值或者多个值插入到链表的尾部（右）
1) "3"
2) "2"
3) "1"
4) "4"


========================================================
#pop
127.0.0.1:6379> lrange list 0 -1
1) "3"
2) "2"
3) "1"
4) "4"
127.0.0.1:6379> lpop list  #移除list的第一个元素
"3"
127.0.0.1:6379> rpop list  #移除list的最后一个元素
"4"
127.0.0.1:6379> lrange list 0 -1
1) "2"
2) "1"


============================================
#index len
127.0.0.1:6379> lrange list 0 -1   #通过下标获取列表的值
1) "2"
2) "1"
127.0.0.1:6379> lindex list 1
"1"
127.0.0.1:6379> lindex list 0
"2"
127.0.0.1:6379> llen list   #获取列表的长度
(integer) 2

===========================================
#lrem
127.0.0.1:6379> lrem list 1 1  #移除list集合中指定个数的value，精确匹配
(integer) 1
127.0.0.1:6379> lrange list 0 -1
1) "4"
2) "4"
3) "3"
4) "2"
127.0.0.1:6379> lrem list 2 4
(integer) 2
127.0.0.1:6379> lrange list 0 -1
1) "3"
2) "2"


===========================================================

#trim 修剪

127.0.0.1:6379> lpush list "hello1"
(integer) 1
127.0.0.1:6379> lpush list "hello2"
(integer) 2
127.0.0.1:6379> lpush list "hello3"
(integer) 3
127.0.0.1:6379> lpush list "hello4"
(integer) 4
127.0.0.1:6379> ltrim list 1 2  #通过下标截取指定的长度 这个list已经被改变了，截断了只剩下未被截取的部分了
OK
127.0.0.1:6379> lrange list 0 -1
1) "hello3"
2) "hello2"


===================================================
#rpoplpush  #移除列表的最后一个元素，将他们移动到新的列表中！

127.0.0.1:6379> rpush list1 "hello1"
(integer) 1
127.0.0.1:6379> rpush list1 "hello2"
(integer) 2
127.0.0.1:6379> rpush list1 "hello3"
(integer) 3
127.0.0.1:6379> rpoplpush list1 list2   #移除列表的最后一个元素，将他们移动到新的列表中！
"hello3"
127.0.0.1:6379> lrange list1 0 -1   #查看原来的列表
1) "hello1"
2) "hello2"
127.0.0.1:6379> lrange list2 0 -1  #查看目标的列表中，确实存在该值！
1) "hello3"



===========================================================
#lset 将列表中指定下标的值替换为另一个值
127.0.0.1:6379> exists list	#判断这个列表是否存在
(integer) 0
127.0.0.1:6379> lpush list value1   
(integer) 1
127.0.0.1:6379> lrange list 0 -1
1) "value1"
127.0.0.1:6379> lset list 0 value0  #如果存在，更新当前下标的值
OK
127.0.0.1:6379> lrange list 0 -1
1) "value0"
127.0.0.1:6379> lset list 1 value2	#如果不存在，我们更新的话会报错
(error) ERR index out of range


======================================================
#linsert #将某个具体的value插入到列表中某个元素的前边或者后边
127.0.0.1:6379> rpush list hello
(integer) 1
127.0.0.1:6379> rpush list world
(integer) 2
127.0.0.1:6379> linsert list before hello zjc #将某个具体的value插入到列表中某个元素的前边
(integer) 3
127.0.0.1:6379> lrange list 0 -1
1) "zjc"
2) "hello"
3) "world"
127.0.0.1:6379> linsert list after world jw #将某个具体的value插入到列表中某个元素的后边
(integer) 4
127.0.0.1:6379> lrange list 0 -1
1) "zjc"
2) "hello"
3) "world"
4) "jw"

```

小结

 - ·他实际上是一个链表，before Node after，left，right 都可以插入值 ·
 - 如果key不存在，创建新的链表
 - 如果key存在，新增内容
 - ·如果移除了所有值，空链表，也代表不存在！ ·在两边插入或者改动值，效率最高！中间元素，相对来说效率会低一点

list功能：消息排队！消息队列（Lpush Rpop），栈（Lpush Lpop）
# Set（集合）
set无序不重复集合

```python
127.0.0.1:6379> sadd set hello 	#往set集合中添加值
(integer) 1
127.0.0.1:6379> sadd set zjc
(integer) 1
127.0.0.1:6379> sadd set jw
(integer) 1
127.0.0.1:6379> smembers set  #查看置顶set的所有值
1) "hello"
2) "jw"
3) "zjc"
127.0.0.1:6379> sismember set hello 	#判断某一个值是不是在set集合当中（1为成功，0为失败）
(integer) 1
127.0.0.1:6379> sismember set world
(integer) 0
==============================================
127.0.0.1:6379> scard set  #查看set集合中元素的个数
(integer) 3
127.0.0.1:6379> smembers set
1) "hello"
2) "jw"
3) "zjc"
127.0.0.1:6379> srem set hello	#移除set集合中指定元素
(integer) 1
127.0.0.1:6379> smembers set
1) "jw"
2) "zjc"

==========================================
#srandmember 随机从set中抽取一个元素
127.0.0.1:6379> smembers set  #查看set集合中的所有元素
1) "2"
2) "1"
3) "jw"
4) "zjc"
5) "3"
127.0.0.1:6379> srandmember set  #所及抽选出一个元素
"jw"
127.0.0.1:6379> srandmember set
"3"
127.0.0.1:6379> srandmember set 2	#所及抽选出指定个数的元素
1) "2"
2) "1"
127.0.0.1:6379> srandmember set 2
1) "zjc"
2) "1"
=================================
#spop 删除随机的key
127.0.0.1:6379> smembers set
1) "jw"
2) "zjc"
3) "2"
4) "3"
5) "1"
127.0.0.1:6379> spop set #所及删除set中的元素
"jw"
127.0.0.1:6379> spop set
"3"
127.0.0.1:6379> smembers set
1) "zjc"
2) "2"
3) "1"

===================================
#smove 讲一个集合中指定的值移动到另一个集合当中
127.0.0.1:6379> smembers set
1) "zjc"
2) "2"
3) "1"
127.0.0.1:6379> sadd set2 set2
(integer) 1
127.0.0.1:6379> sadd set2 jw
(integer) 1
127.0.0.1:6379> smembers set2
1) "set2"
2) "jw"
127.0.0.1:6379> smove set set2 zjc   #讲一个集合中指定的值移动到另一个集合当中
(integer) 1
127.0.0.1:6379> smembers set
1) "2"
2) "1"
127.0.0.1:6379> smembers set2
1) "set2"
2) "zjc"
3) "jw"

================================================
数学集合 差集 sdiff 交集sinter 并集sunion
127.0.0.1:6379> sadd set1 a
(integer) 1
127.0.0.1:6379> sadd set1 b
(integer) 1
127.0.0.1:6379> sadd set1 c
(integer) 1
127.0.0.1:6379> sadd set2 c
(integer) 1
127.0.0.1:6379> sadd set2 d
(integer) 1
127.0.0.1:6379> sadd set2 e
(integer) 1
127.0.0.1:6379> smembers set1
1) "b"
2) "c"
3) "a"
127.0.0.1:6379> smembers set2
1) "e"
2) "d"
3) "c"
127.0.0.1:6379> sdiff set1 set2 #差集
1) "b"
2) "a"
127.0.0.1:6379> sinter set1 set2	#交集
1) "c"
127.0.0.1:6379> sunion set1 set2	#并集
1) "b"
2) "c"
3) "a"
4) "e"
5) "d"
```

# Hash（哈希）
Map集合，key-map！这个时候值是一个map集合！本质上和String类型没有太大的区别，还是一个简单的kay-value键值对（不过这个value是一个key-value）
```python
127.0.0.1:6379> flushdb
OK
127.0.0.1:6379> hset hash1 f1 zjc #set一个具体的key-value
(integer) 1
127.0.0.1:6379> hget hash1 f1 #获取一个字段的值
"zjc"
127.0.0.1:6379> hmset hash1 f1 hello f2 jw #set多个key-value
OK
127.0.0.1:6379> hmget hash1 f1 f2	#获取多个字段值
1) "hello"
2) "jw"
127.0.0.1:6379> hgetall hash1 	#获取全部的数据
1) "f1"
2) "hello"
3) "f2"
4) "jw"
127.0.0.1:6379> hdel hash1 f1	#删除hash指定key字段！对应value值也就消失了！
(integer) 1
127.0.0.1:6379> hgetall hash1
1) "f2"
2) "jw"
127.0.0.1:6379> hgetall hash1
1) "f1"
2) "hello"
3) "f2"
4) "jw"
127.0.0.1:6379> hdel hash1 f1  #删除hash中特定的值
(integer) 0
127.0.0.1:6379> hgetall hash1
1) "f2"
2) "jw"

=================================================
#heln hexists
127.0.0.1:6379> hgetall hash1
1) "f2"
2) "jw"
3) "f1"
4) "zjc"
127.0.0.1:6379> hlen hash1	#获取hash表的字段数量
(integer) 2
127.0.0.1:6379> hexists hash1 f1 #判断hash中指定字段是否存在
(integer) 1
127.0.0.1:6379> hexists hash1 f3
(integer) 0


================================
#hkeys hvals hincrby hsetnx
127.0.0.1:6379> hkeys hash1 #只获得所有的key
1) "f2"
2) "f1"
127.0.0.1:6379> hvals hash1	#只获得所有的value
1) "jw"
2) "zjc"
127.0.0.1:6379> hset hash1 f3 5	
(integer) 1
127.0.0.1:6379> hget hash1 f3
"5"
127.0.0.1:6379> hincrby hash1 f3 1	#指定增量
(integer) 6
127.0.0.1:6379> hget hash1 f3
"6"
127.0.0.1:6379> hsetnx hash1 f4 hello #设置指定的值，如果不存在则创建并设置
(integer) 1
127.0.0.1:6379> hsetnx hash1 f4 world	 #设置指定的值，如果存在则不能设置
(integer) 0
127.0.0.1:6379> hget hash1 f4
"hello"


```
# Zset（有序集合）
在set的基础上，增加了一个值，set k1 v1 zset k1 score v1

```python
127.0.0.1:6379> zadd set1 1 one		#添加一个值
(integer) 1
127.0.0.1:6379> zadd set1 2 two 	
(integer) 1
127.0.0.1:6379> zadd set1 3 three
(integer) 1
127.0.0.1:6379> zrange set1 0 -1	获取zset集合中的值
1) "one"
2) "two"
3) "three"

==================================================
127.0.0.1:6379> zadd socre 5000 zjc  #添加三个用户
(integer) 1
127.0.0.1:6379> zadd socre 2500 jw
(integer) 1
127.0.0.1:6379> zadd socre 100 ly
(integer) 1
127.0.0.1:6379> zrangebyscore socre -inf +inf #显示全部的用户，从小到大
1) "ly"
2) "jw"
3) "zjc"
127.0.0.1:6379> zrevrange socre 0 -1 #显示全部的用户，从大到小排序
1) "jw"
2) "ly"
127.0.0.1:6379> zrangebyscore socre -inf +inf withscores 	#显示全部的用户并且附带成绩
1) "ly"
2) "100"
3) "jw"
4) "2500"
5) "zjc"
6) "5000"
127.0.0.1:6379> zrangebyscore socre -inf 2500 withscores	#显示指定区间的用户并升序排序
1) "ly"
2) "100"
3) "jw"
4) "2500"

==============================================
#zrem zcard
127.0.0.1:6379> zrange socre 0 -1
1) "ly"
2) "jw"
3) "zjc"
127.0.0.1:6379> zrem socre zjc 	#移除有序集合中指定元素
(integer) 1
127.0.0.1:6379> zrange socre 0 -1
1) "ly"
2) "jw"
127.0.0.1:6379> zcard socre	#获取有序集合中的个数
(integer) 2

================================================
#zcount
127.0.0.1:6379> zadd myset 1 hello
(integer) 1
127.0.0.1:6379> zadd myset 2 world
(integer) 1
127.0.0.1:6379> zadd myset 3 zjc
(integer) 1
127.0.0.1:6379> zcount myset 1 3 	#获取指定区间成员数量
(integer) 3
127.0.0.1:6379> zcount myset 1 2
(integer) 2
```
案例思路：set排序 存储班级成绩表  工资表排序
普通消息1  重要消息 2带权重进行判断
排行榜应用 取Top测试！

# geospatial
朋友的定位，附近的人，打车距离计算？
Redis的Geo在Redis3.2版本就推出了！这个功能可以推算地理位置的信息，两地之间的距离，方圆几里的人！
可以查询一些测试数据：https://www.china95.net/paipan/jingdu/index.asp
规则：https://www.redis.net.cn/order/3685.html
 - getadd添加地理位置
 

```python
#geoadd 添加地理位置
#规则：两级无法直接添加，我们一般会下载城市数据，直接通过
java程序一次性导入
有效的经度从-180度到180度。
有效的纬度从-85.05112878度到85.05112878度。
当坐标位置超出上述指定范围时，该命令将会返回一个错误。
#参数 key 值（维度、经度、名称）
127.0.0.1:6379> geoadd china:city 116.40 39.90 beijing
(integer) 1
127.0.0.1:6379> geoadd china:city 121.47 31.23 sahnghai
(integer) 1
127.0.0.1:6379> geoadd china:city 106.50 29.56 chongqing
(integer) 1
127.0.0.1:6379> geoadd china:city 114.05 22.52 shenzhen
(integer) 1
127.0.0.1:6379> geoadd china:city 120.16 30.24 hangzhou
(integer) 1
127.0.0.1:6379> geoadd china:city 108.96 34.26 xian
(integer) 1

```

 - geopos获取当前定位：一定是一个坐标值！

```python
127.0.0.1:6379> geopos china:city 北京 	#获取指定城市的经度和纬度
1) 1) "116.39999896287918091"
   2) "39.90000009167092543"
127.0.0.1:6379> geopos china:city 深圳 西安
1) 1) "114.04999762773513794"
   2) "22.5200000879503861"
2) 1) "108.96000176668167114"
   2) "34.25999964418929977"
```

 - geodis：两人之间的距离

单位：如果两个位置之间的其中一个不存在， 那么命令返回空值。指定单位的参数 unit 必须是以下单位的其中一个：
 - m 表示单位为米。
 - km 表示单位为千米。
 - mi 表示单位为英里。
 - ft 表示单位为英尺。

```python
127.0.0.1:6379> geodist china:city 深圳 重庆	#查看深圳到重庆的直线距离
"1086757.1868"
127.0.0.1:6379> geodist china:city 上海 西安 km	#查看上海西安的直线距离
"1216.9307
```

 - georadius以给定的经纬度为中心，找出某一半径内的元素
 
 我附近的人？（获取所有附近的人的地址、定位）通过半径来查询，所有的数据都录入：china：city

```python
127.0.0.1:6379> georadius china:city 110 30 1000 km #以100,30这个经纬度为中心，方圆1000km的城市
1) "chongqing"
2) "xian"
3) "shenzhen"
4) "hangzhou"
127.0.0.1:6379> georadius china:city 110 30 500 km
1) "chongqing"
2) "xian"
127.0.0.1:6379> georadius china:city 110 30 500 km withdist	#显示到中心距离的位置
1) 1) "chongqing"
   2) "341.3933"
2) 1) "xian"
   2) "483.8340"
127.0.0.1:6379> georadius china:city 110 30 500 km withcoord	#显示定位信息
1) 1) "chongqing"
   2) 1) "106.49999767541885376"
      2) "29.56000053864853072"
2) 1) "xian"
   2) 1) "108.96000176668167114"
      2) "34.25999964418929977"
127.0.0.1:6379> georadius china:city 110 30 500 km withcoord count 2	#筛选出指定的结果
1) 1) "chongqing"
   2) 1) "106.49999767541885376"
      2) "29.56000053864853072"
2) 1) "xian"
   2) 1) "108.96000176668167114"
      2) "34.25999964418929977"
127.0.0.1:6379> georadius china:city 110 30 500 km withcoord count 1
1) 1) "chongqing"
   2) 1) "106.49999767541885376"
      2) "29.56000053864853072"

```

 - georadiusbymember找出指定元素周围的其他元素

和上面不同的是这个是通过元素来找，上面是通过定位来找

```python
127.0.0.1:6379> georadius china:city 110 30 500 km withcoord count 1	找出指定元素周围的其他元素
1) 1) "chongqing"
   2) 1) "106.49999767541885376"
      2) "29.56000053864853072"
127.0.0.1:6379> georadiusbymember china:city beijing 1000 km
1) "beijing"
2) "xian"
127.0.0.1:6379> georadiusbymember china:city sahnghai 400 km
1) "hangzhou"
2) "sahnghai"
```

 - geohash：将二维的经纬度转换为一维的字符串，如果两个字符串越接近的话，那么距离就越近

```python
127.0.0.1:6379> geohash china:city beijing chongqing
1) "wx4fbxxfke0"
2) "wm78pmnzmz0"

```
geo的底层实现原理其实是Zset！我们可以使用Zset的命令来操作geo！

```python
127.0.0.1:6379> zrange china:city 0  -1	#查看地图元素
1) "chongqing"
2) "xian"
3) "shenzhen"
4) "hangzhou"
5) "sahnghai"
6) "beijing"
127.0.0.1:6379> zrem china:city beijing 
(integer) 1
127.0.0.1:6379> zrange china:city 0  -1	#移除元素
1) "chongqing"
2) "xian"
3) "shenzhen"
4) "hangzhou"
5) "sahnghai"
```

# hyperloglog
基数：不重复的元素，比如{1.3.5.7.8}为5，可以接收误差

Redis 2.8.9版本就更新了Hyperloglog数据结构！
Redis Hyperloglog基数统计的算法！
优点：<code>占用的内存是固定，2/64不同的元素的技术，只需要废12KB内有！如果要从内存角度来比较的话Hyperloglog首选！</code>
***网页的UV（一个人访问一个网站多次，但是还是算作一个人！）****
传统的方式，set保存用户的id，然后就可以统计 set中的元素数量作为标准判断！
这个方式如果保存大量的用户id，就会比较麻烦！我们的目的是为了计数，而不是保存用户id；
```python
127.0.0.1:6379> pfadd key1 a b c d e f g h i j  #创建第一组元素 key1
(integer) 1
127.0.0.1:6379> pfcount key1	#统计 key1元素的基数信息
(integer) 10
127.0.0.1:6379> pfadd key2 i j z x c b n m
(integer) 1
127.0.0.1:6379> pfcount key2	#统计第二组 key2元素的基数
(integer) 8
127.0.0.1:6379> pfmerge key3 key1 key2	#合并两组  key1 key2  到 key3
OK
127.0.0.1:6379> pfcount key3	#查看并集的数量
(integer) 14

```
如果允许容错，那么一定使用 Hyperloglog！
如果不允许容错，就使用 set 挥着自己的数据类型即可！
# bitmaps

 - 位存储

统计用户信息，活跃，不活跃！登录、未登录！打卡，365打卡！两个状态的，都可以使用Bitmaps！
Bitmaps位图，数据结构！都是操作二进制位来进行记录，就只有0和1两个状态！
365天=365bit 1字节=8bit 46个字节左右！

 - 用bitmaps来记录周一到周日的打开情况！

周一：1 周二：0.................

```python
127.0.0.1:6379> setbit sign 0 1
(integer) 0
127.0.0.1:6379> setbit sign 1 0 
(integer) 0
127.0.0.1:6379> setbit sign 2 0
(integer) 0
127.0.0.1:6379> setbit sign 3 1
(integer) 0
127.0.0.1:6379> setbit sign 4 1
(integer) 0
127.0.0.1:6379> setbit sign 5 0
(integer) 0
127.0.0.1:6379> setbit sign 6 0
(integer) 0

```

 - 获取某一天的打卡情况
 

```python
127.0.0.1:6379> getbit sign 3
(integer) 1
127.0.0.1:6379> getbit sign 5
(integer) 0
```

 - 统计打卡天数

```python
127.0.0.1:6379> bitcount sign
(integer) 3
```
