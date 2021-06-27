@[TOC](集合/容器)

# java 容器都有哪些？

![在这里插入图片描述](https://img-blog.csdnimg.cn/20210625100505188.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQ1NjYxMTI1,size_16,color_FFFFFF,t_70)

# Collection 和 Collections 有什么区别？

 - java.util.Collection是一个<code>接口</code>（集合类的一个顶级接口）。它提供了对集合对象进行基本操作的通用接口方法。
 - Collections则是一个<code>类</code>(工具类、帮助类），其中提供了一系列静态方法，用于对集合中元素进行排序、搜索以及线程安全等各种操作。

# List、Set、Map 之间的区别是什么？

![在这里插入图片描述](https://img-blog.csdnimg.cn/2021062510152694.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQ1NjYxMTI1,size_16,color_FFFFFF,t_70)

# HashMap 和 Hashtable 有什么区别？

 - HashMap去掉了HashTable 的contains方法，但是加上了containsValue（）和containsKey（）方法。
 - HashMap允许插入空键值，而hashTable不允许。
 - HashMap是线程不安全的。HashTable是线程安全的（但HashTable的效率低）

# 如何决定使用 HashMap 还是 TreeMap？

对于在Map中插入、删除和定位元素这类操作，HashMap是最好的选择。然而，假如你需要对一个有序的key集合进行遍历，TreeMap是更好的选择。（TreeMap底层红黑树）

# 说一下 HashMap 的实现原理？

 - 1.7是用数组+链表的方式实现的，采用的是头插法，会造成链表逆序的问题，在多线程下会产生循环链表，从而造成死循环（是线程不安全的）
 - 1.8则采用数组+链表+红黑树的方式实现的，采用的是尾插法，但在多线程下会产生是数据覆盖的问题（是线程不安全的）

当我们往Hashmap中put元素时,首先根据key的hashcode重新计算hash值,根据hash值得到这个元素在数组中的位置(下标),如果该数组在该位置上已经存放了其他元素,那么在这个位置上的元素将以链表的形式存放,如果数组中该位置没有元素,就直接将该元素放到数组的该位置上。

# 说一下 HashSet 的实现原理？

 - HashSet底层由HashMap实现
 - HashSet的值存放于HashMap的key上
 - HashMap的value统一为PRESENT

# ArrayList 和 LinkedList 的区别是什么？

 - ArrrayList底层的数据结构是数组，支持随机访问，而 LinkedList 的底层数据结构是双向循环链表，不支持随机访问
 - ArrrayList的插入时间复杂度为O（n），而linkedList的复杂度为O(1)
 - ArrrayList的查询时间复杂度为O（1），而linkedList的复杂度为O(n)

# 如何实现数组和 List 之间的转换？

 - List转换成为数组：调用ArrayList的toArray方法。
 - 数组转换成为List：调用Arrays的asList方法。

# Iterator 怎么使用？有什么特点？

Java中的Iterator功能比较简单，并且只能单向移动：

 - (1)使用方法iterator()要求容器返回一个Iterator。第一次调用Iterator的next()方法时，它返回序列的第一个元素。注意：iterator()方法是java.lang.Iterable接口,被Collection继承。
 - (2) 使用next()获得序列中的下一个元素
 - (3) 使用hasNext()检查序列中是否还有元素。
 - (4) 使用remove()将迭代器新返回的元素删除。

Iterator是Java迭代器最简单的实现，为List设计的ListIterator具有更多的功能，它可以从两个方向遍历List，也可以从List中插入和删除元素。


# ArrayList特点

ArrayList底层是数组，默认采用尾插法，再remove()元素时，由于modCount所以需要使用迭代器来删除，它允许插入null。

# LinkedList特点

LinkedList的底层结构是一个带头尾指针的双向链表，可以快速的对头、尾节点进行操作，它允许插入null。

# Stack特点

栈：一种特殊的线性表，其只允许在固定的一端进行插入和删除元素操作。进行数据插入和删除操作的一端称为栈顶，另一端称为栈底。栈中的数据元素遵守后进先出LIFO（Last In First Out）的原则。
栈底层用Vector实现的

# Queue的特点

队列：只允许在一端进行插入数据操作，在另一端进行删除操作的特殊线性表，队列具有先进先出FIFO(First In First Out)的特点
![在这里插入图片描述](https://img-blog.csdnimg.cn/20210625122106751.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQ1NjYxMTI1,size_16,color_FFFFFF,t_70)


# 在 Queue 中 poll()和 remove()有什么区别？

poll() 和 remove() 都是从队列中取出一个元素，但是 poll() 在获取元素失败的时候会返回空，但是 remove() 失败的时候会抛出异常。
