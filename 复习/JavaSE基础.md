@[TOC](基础复习)

# 面向对象编程

 - 面向过程就是分析出解决问题需要的步骤，然后用函数把这些步骤一个个实现，使用的时候依次调用，面向过程的核心是过程（C语言）
 - 面向对象就是把构成问题的事物分解成一个个对象，建立对象不是为了实现一个步骤，而是为了描述某个事物在解决问题中的行为，面向对象的核心是对象。（Java/C++）

所谓对象就是真实世界中的实体，对象与实体是一一对应的，也就是说现实世界中每一个实体都是一个对象，它是一种具体的概念。

 - 对象：**对象是类的一个实例**（对象不是找个女朋友），有状态和行为。例如，一条狗是一个对象，它的状态有：颜色、名字、品种；行为有：摇尾巴、叫、吃等。
 - 类：类是一个模板，它描述一类对象的行为和状态。


**类的基本结构**

 - 属性：对象数据的描述
 - 方法：对象的行为
 - 构造方法：用于实例化对象
 - 内部类：在类中声明的类（inner class）
 - 块：分静态块与实例块
 - 类的声明：（访问权限修饰符public.default（可忽略不写，为默认））（修饰final.abstract.synchronized）class类名{ 类体 }

类的作用：类就是一个模板，定义多个对象共同的属性和方法 如：学生类（张三，李四）　手机类（华为.oppo\苹果）

# public、private、protected和默认权限比较比较

 - private: 类内部能访问, 类外部不能访问
 - 默认(也叫包访问权限): 类内部能访问, 同一个包中的类可以访问, 其他类不能访问.
 - protected: 类内部能访问, 子类和同一个包中的类可以访问, 其他类不能访问.（用于继承）
 - public : 类内部和类的调用者都能访问

![在这里插入图片描述](https://img-blog.csdnimg.cn/20210626100828251.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQ1NjYxMTI1,size_16,color_FFFFFF,t_70)

# 什么是封装？

在我们写代码的时候经常会涉及两种角色: 类的实现者和类的调用者.
封装的本质就是让类的调用者不必太多的了解类的实现者是如何实现类的, 只要知道如何使用类就行了.
这样就降低了类使用者的学习和使用成本, 从而降低了代码复杂程度。
使用 private 封装属性，并提供 public 方法供类的调用者使用（Setter、Getter）

# 什么是继承？

代码中创建的类, 主要是为了抽象现实中的一些事物(包含属性和方法).
有的时候客观事物之间就存在一些关联关系（它们中有一些相同的特征，具有一些共有的东西） 那么在表示成类和对象的时候也会存在一定的关联.

 - 使用 **extends**关键字指定父类
 - Java 中是单继承的，想要多继承的话需要使用接口。
 - 子类会继承父类的所有 public 的字段和方法
 - 子类从父类中继承了**除构造方法外**的所有字段和属性（但是只能根据访问修饰限定符来访问能访问的字段）而构造方法就需要super来解决了。

**super关键字**
子类从父类中继承了除构造方法外的所有字段和属性。那么构造方法就需要super来解决了。

 - super代表父类对象的引用，可以调用父类的普通方法和属性
 - 子类继承父类时，子类构造的时候，需要先帮助父类构造，在子类的构造方法内部，显示调用父类的构造方法super（）（如果是无参构造则可以省略不写）
 - super（）必须放在子类构造方法的第一行
 - super（）不能在静态方法中使用它（super代表引用，需要对象）

**不想被继承就用final关键字来修饰**

**继承中代码的执行顺序**
父类的静态变量–>父类的静态代码块–>
子类的静态变量–>子类的静态代码块–>
父类的非静态变量–>父类的普通代码块–>父类的构造方法–>
子类的非静态变量–>子类的普通代码块–>子类的构造方法

# 什么是多态？

通俗点来说：多态就是同一个父类引用可以引用不同的子类对象，可以调用一个同名的方法，而产生不同的行为（多态是一种思想）

**多态的优势**

 - 使代码变得简洁，类的调用者对类的使用成本降低
 - 降低圈复杂度（避免大量的使用if-else） 
 - 可扩展性强

向上转型：父类引用 引用 子类对象（直接赋值、方法传参、返回值会发生向上转型）
动态绑定（运行时绑定）看父类引用到底指向哪一个实例，如果指向子类的实例（则调用子类的同名方法），如果执行自己父类的实例（则调用自己的同名方法），而这个过程是程序运行起来之后才决定的（而非编译时期），所以称为运行时绑定
![在这里插入图片描述](https://img-blog.csdnimg.cn/20210626104513141.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQ1NjYxMTI1,size_16,color_FFFFFF,t_70)
重写（Override）

 - 针对重写的方法, 可以使用 @Override 注解来显式指定（合法性的校验）
 - 重写和重载完全不一样，不要混淆
 - 普通方法可以重写，static修饰的静态方法不能重写
 - 重写中子类的方法的访问权限<code>大于</code>父类的访问权限（public可以相同）
 - 重写的方法返回值不一定和父类的方法相同（但建议写成相同的，不同时子类和父类的返回值要构成继承关系这种称为协同类型）
 - <code>不要再构造方法中调用重写方法


# 抽象类

包含抽象方法（抽象方法没有具体的实现）的类我们称为 抽象类(abstract class).没有什么实际的作用，被其他类所继承

 - 抽象类不能实例化（可以简单地理解为抽象抽象肯定不能实例化啦）
 - 在抽象类中可以拥有和普通类一样的属性和方法
 - 抽象类可以被继承（不然要你干啥）可以说抽象类的的最大意义就是为了继承（但子类必须要重写抽象类的抽象方法）
 - 抽象方法不能是private的（废话，因为你抽象方法就是要被重写的，你设成private还怎么重写，因为重写方法的话的话子类的访问权限要大于父类的访问权限）

# 接口

接口是抽象类的更进一步，抽象类中还可以包含非抽象的方法和字段，而接口中包含的方法都是抽象方法，字段也只能静态常量。

 - 接口当中的方法都是抽象方法（默认为public absyract可以省略）
 - 接口中的方法默认使用 public 修饰
 - 接口当中的成员变量默认为public static final(定义的同时初始化)
 - 接口不可以进行实例化
 - 一个类只能继承一个抽象类或普通类，但可以继承多个接口（解决了Jave不能多继承的限制）

# 接口和抽象类有什么区别？

 - **实现**：抽象类的子类使用 extends 来继承；接口必须使用 implements 来实现接口。
 - **构造函数**：抽象类可以有构造函数；接口不能有。
 - **main** 方法：抽象类可以有 main 方法，并且我们能运行它；接口不能有 main 方法。
 - **实现数量**：类可以实现很多个接口；但是只能继承一个抽象类。
 - **访问修饰符**：接口中的方法默认使用 public 修饰；抽象类中的方法可以是任意访问修饰符。

# == 和 equals 的区别是什么？

== 解读

对于基本类型和引用类型 == 的作用效果是不同的，如下所示：要注意下面程序结果为true
![在这里插入图片描述](https://img-blog.csdnimg.cn/20210626152552806.png)


 - **基本类型**：比较的是值是否相同
 - **引用类型**：比较的是引用是否相同

equals解读

 - equals 默认情况下是引用比较，只是很多类重新了 equals 方法，比如 String、Integer 等把它变成了值比较，所以一般情况下 equals 比较的是值是否相等

# 两个对象的 hashCode()相同，则 equals()也一定为 true，对吗？

不对，两个对象的 hashCode()相同，equals()不一定 true。例如hashmap的哈希冲突。

# java 中的 Math.round(-1.5) 等于多少？

先加0.5，在向下取整等于-1

# String 属于基础的数据类型吗？

String不属于基础的数据类型

# String String 类的常用方法都有那些？

 - indexOf()：返回指定字符的索引。
 - charAt()：返回指定索引处的字符。
 - replace()：字符串替换。
 - trim()：去除字符串两端空白。
 - split()：分割字符串，返回一个分割后的字符串数组。
 - getBytes()：返回字符串的 byte 类型数组。
 - length()：返回字符串长度。
 - toLowerCase()：将字符串转成小写字母。
 - toUpperCase()：将字符串转成大写字符。
 - substring()：截取字符串。
 - equals()：字符串比较。
 - toCharArray（）：将字符串变为数组

# String str="abc"与 String str=new String("abc")一样吗？

不一样，因为内存的分配方式不一样。String str="abc"的方式，java 虚拟机会将其分配到常量池中；而 String str=new String("abc") 则会被分到堆内存中。

# java 中操作字符串都有哪些类？它们之间有什么区别？

操作字符串的类有：String、StringBuffer、StringBuilder。

 - StringBuffer、StringBuilder有reverse()方法
 - String 声明的是不可变的对象，每次操作都会生成新的 String 对象，然后将指针指向新的 String 对象（<code>String的拼接 + 会被优化 优化为StringBuilder . append了</code>），而StringBuffer、StringBuilder 可以在原有对象的基础上进行操作，所以在经常改变字符串内容的情况下最好不要使用 String。 
 - StringBuffer 和 StringBuilder 最大的区别在于，StringBuffer 是线程安全的，而StringBuilder 是非线程安全的，但 StringBuilder 的性能却高于
   StringBuffer，所以在单线程环境下推荐使用 StringBuilder，多线程环境下推荐使用 StringBuffer。

# BIO、NIO、AIO 有什么区别？

 - **BIO**：Block IO 同步阻塞式 IO，就是我们平常使用的传统 IO，它的特点是模式**简单使用方便，并发处理能力低。**
 - **NIO**：New IO 同步非阻塞 IO，是传统 IO 的升级，客户端和服务器端通过 Channel（通道）通讯，实现了**多路复用**。
 - **AIO**：Asynchronous IO 是 NIO 的升级，也叫 NIO2，实现了异步非堵塞 IO ，异步 IO的操作基于事件和回调机制。

# 什么是异常

异常，就是不正常的意思。指的是程序在执行过程中，出现的非正常的情况，最终会导致JVM的非正常停止。

 - 在Java等面向对象的编程语言中，异常本身是一个类，产生异常就是创建异常对象并抛出了一个异常对象。Java处理异常的方式是中断处理
 - 异常指的并不是语法错误.语法错了,编译不通过,不会产生字节码文件,根本不能运行。但异常可以在运行时产生

# 异常体系

![在这里插入图片描述](https://img-blog.csdnimg.cn/20210626155425223.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQ1NjYxMTI1,size_16,color_FFFFFF,t_70)
**Throwable体系：**
异常的根类是**java.lang.Throwable**，其下有两个子类：java.lang.Error（错误）与java.lang.Exception（异常），平常所说的异常java.lang.Exception。

 - Error:错误，无法处理纠正的错误，只能事先避免，好比绝症。
 - Exception:异常，异常产生后程序员可以通过代码的方式纠正，使程序继续运行。好比感冒。

比较通俗易懂的方法是，你把代码写出来之后，有红色波浪线提示你抛出或捕获异常，这个时候正处于编译阶段，所以是编译时异常

# 异常的分类

我们平常说的异常就是指Exception，因为这类异常一旦出现，我们就要对代码进行更正，修复程序。

异常(Exception)的分类:根据在编译时期还是运行时期可分为编译时异常，和运行时异常。

编译时期异常:（受查异常）在编译时期,就会检查,如果没有处理异常,则编译失败。(如输入输出、类型转换异常) <code>比较通俗易懂的方法是，你把代码写出来之后，有红色波浪线提示你抛出或捕获异常，这个时候正处于编译阶段，所以是编译时异常</code>

 - 1.FileNotFoundException
 - 2.ClassNotFoundException
 - 3.SQLException
 - 4.NoSuchMethodException
 - IOException

运行时期异常:（非受查异常）在编译时期,不会报错，在运行时期会报错.。(如数学异常)

 - 1.NullPointerException
 - 2.ArithmeticException(当出现异常的运算条件时，抛出此异常)
 - 3.ClassCastException
 - 4.ArrayIndexOutOfBoundsException
 - 5.StringIndexOutOfBoundsException

#  throw 和 throws 的区别？

throw：

 - 表示方法内抛出某种异常对象
 - 如果异常对象是非 RuntimeException 则需要在方法申明时加上该异常的抛出 即需要加上throws 语句 或者在方法体内try catch 处理该异常，否则编译报错
 - <code>执行到 throw 语句则后面的语句块不再执行

 throws：

 - 方法的定义上使用 throws 表示这个方法可能抛出某种异常
 - throws是将异常声明但是不处理，而是将异常往上传，需要由方法的调用者进行异常处理

# try-catch-finally 中，如果 catch 中 return 了，finally 还会执行吗？

 - finally 执行的时机是在方法返回之前(try 或者 catch 中如果有 return 会在这个 return 之前执行finally). 但是如果finally 中也存在 return 语句, 那么就会执行 finally 中的 return,从而不会执行到 try 中原有的 return.
 - <code>一般我们不建议在 finally 中写 return (被编译器当做一个警告)

# 异常处理的流程

 - 程序先执行 try 中的代码
 - 如果 try 中的代码出现异常, 就会结束 try 中的代码, 看和 catch 中的异常类型是否匹配（找匹配）.
 - 如果找到匹配的异常类型, 就会执行 catch 中的代码
 - 如果没有找到匹配的异常类型, 就会将异常向上传递到上层调用者.
 - 无论是否找到匹配的异常类型, finally 中的代码都会被执行到(在该方法结束之前执行).
 - 如果上层调用者也没有处理的了异常, 就继续向上传递. 一直到 main 方法也没有合适的代码处理异常, 就会交给 JVM 来进行处理,此时程序就会异常终止（jvm保底）
