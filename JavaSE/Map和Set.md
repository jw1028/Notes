- 1. - **                                                                                  Map和Set**
  
     
  
     # 概念和场景
  
     Map和Set是一种专门用来进行**搜索**的容器或者数据结构，其搜索的效率与其具体的实例化子类有关。
     以前常见的 搜索方式有：
  
     - 1.直接遍历，时间复杂度为O(N)，元素如果比较多效率会非常慢
     - 2.二分查找，时间复杂度为O(log2n) ,但搜索前必须要求序列是有序的
  
     上述排序比较适合**静态类型的查找**，即一般不会对区间进行插入和删除操作了，而现实中的查找比如：
  
     - 1.根据姓名查询考试成绩
     - 2.通讯录，即根据姓名查询联系方式
     - 3.不重复集合，即需要先搜索关键字是否已经在集合中
  
     **可能在查找时进行一些插入和删除的操作**，即**动态**查找，那上述两种方式就不太适合了，就需要**Map和Set**来解决了，一种适合**动态查找**的集合容器。
  
     # 两种模型
  
     一般把搜索的数据称为**关键字（Key）**，和关键字对应的称为**值（Value）**，将其称之为Key-value的键值对，所以 模型会有两种：
  
     - 1.**纯 key 模型**，比如：有一个英文词典，快速查找一个单词是否在词典中或者快速查找某个名字在不在通讯录中
     - 2.**Key-Value 模型**，比如：统计文件中每个单词出现的次数，统计结果是每个单词都有与其对应的次数：<单词，单词出现的次数>
  
     **而Map中存储的就是key-value的键值对，Set中只存储了Key**
  
     # Map
  
     Map是一个**接口类**，该类没有继承自Collection，该类中存储的是<K,V>结构的键值对，**并且K一定是唯一的，不能重复，但value可以重复**。
  
     **Map的常用方法**
  
     ![在这里插入图片描述](https://img-blog.csdnimg.cn/20210206204843890.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQ1NjYxMTI1,size_16,color_FFFFFF,t_70)
     **注意事项**
  
     - 1.**Map**是一个**接口**，**不能直接实例化对象**，如果要实例化对象只能实例化其实现类TreeMap或者HashMap
     - 2.Map中存放键值对的**Key**是**唯一**的，**value**是**可以重复**的
     - 3.在Map中插入键值对时，**key和value可以为空**
     - 4.Map中的Key可以全部分离出来，存储到Set中来进行访问(因为Key不能重复)。
     - 5.Map中的value可以全部分离出来，存储在Collection的任何一个子集合中(value可能有重复)。
     - 6.Map中键值对的Key不能直接修改，value可以修改，如果要修改key，只能先将该key删除掉，然后再来进行 重新插入。
     - 7.TreeMap和HashMap的区别
       ![在这里插入图片描述](https://img-blog.csdnimg.cn/20210206205100782.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQ1NjYxMTI1,size_16,color_FFFFFF,t_70)
  
     # Set
  
     Set与Map主要的不同有两点：**Set**是**继承**自**Collection**的接口类，**Set中只存储了Key。**
  
     **Set常用方法**
     ![在这里插入图片描述](https://img-blog.csdnimg.cn/20210206205738817.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQ1NjYxMTI1,size_16,color_FFFFFF,t_70)
     **注意事项**
  
     - 1.Set是**继承**自**Collection**的一个接口类
     - 2.Set中只存储了key，并且要求key一定要**唯一**
     - 3.Set的底层是使用Map来实现的，其使用key与Object的一个默认对象作为键值对插入到Map中的
     - 4.Set最大的功能就是对集合中的元素进行**去重**
     - 5.实现Set接口的常用类有TreeSet和HashSet
     - 6.Set中的Key不能修改，如果要修改，先将原来的删除掉，然后再重新插入
     - 7.Set中可以插入null的key。
     - 8.TreeSet和HashSet的区别
       ![在这里插入图片描述](https://img-blog.csdnimg.cn/20210206205957132.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQ1NjYxMTI1,size_16,color_FFFFFF,t_70)
       
  
     
