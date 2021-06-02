@[TOC](JVM万字详解)

JVM主要从五方面来看，下面来一次详解
![在这里插入图片描述](https://img-blog.csdnimg.cn/20210531232720677.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQ1NjYxMTI1,size_16,color_FFFFFF,t_70)

# JVM基本概念及内存区域
## 基本概念
JVM是**Java Virtual Machine**（Java虚拟机）的缩写，JVM是一种用于计算设备的规范，它是一个虚构出来的计算机，是通过在实际的计算机上仿真模拟各种计算机功能来实现的。引入Java语言虚拟机后，**Java语言在不同平台上运行时不需要重新编译**。JVM帮我们处理了不同硬件之间的差异，使得Java语言编译程序只需生成在Java虚拟机上运行的目标代码（字节码），就可以在多种平台上不加修改地运行。（<code>一次编译到处运行）
## 运行过程
 - Java 源文件（.java）--->编译器--->字节码文件(.class)--->JVM--->机器码(可以在不同的平台上到处跑）

每一种平台的**解释器是不同的**，但是实现的**虚拟机是相同的**，这也就是 Java 为什么能够跨平台的原因了 ，当一个程序从开始运行，这时虚拟机就开始实例化了，多个程序启动就会存在多个虚拟机实例。程序退出或者关闭，则虚拟机实例消亡，多个虚拟机实例之间数据不能共享。
## 内存区域
JVM 内存区域主要分为<code>虚拟机栈、本地方法栈、程序计数器、方法区、堆，</code>其中程序计数器、虚拟机栈和本地方法栈为线程私有，堆和方法区为线程共有。

 - **线程私有**数据区域生命周期与线程相同, 依赖用户线程的启动/结束 而创建/销毁(在 Hotspot VM 内,每个线程都与操作系统的本地线程直接映射, 因此这部分内存区域的存/否跟随本地线程的生/死对应)。
 - **线程共享**区域随虚拟机的启动/关闭而创建/销毁。

![在这里插入图片描述](https://img-blog.csdnimg.cn/20210601084526105.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQ1NjYxMTI1,size_16,color_FFFFFF,t_70)

###  堆 （线程共享）
![在这里插入图片描述](https://img-blog.csdnimg.cn/20210601091420908.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQ1NjYxMTI1,size_16,color_FFFFFF,t_70)

堆主要用于存放各种类的实例对象和数组。堆是JVM中最大的一块内存。在java中被分为两个区域：年轻代和老年代。

 - **新生代**：新创建的数据会在新生代，当经历一定次数的GC后活下来的数据，会移动到老年代（HotSpot默认的垃圾回收是15次）
   新生代又分为三个区域：Eden、S0、S1（Eden经常和S0或S1中的一个配合使用）垃圾回收的时候会将 Endn 中存活的对象放到⼀个未使⽤的 Survivor 中，并把当前的 Endn 和正在使⽤ 的 Survivor 清楚掉。
 - **老年代**：存放的是经过了一定次数还存活的对象和大对象（因为大对象的创建和销毁所需要的时间比较多，如果放在新生代，可能会频繁的创建和销毁，从而导致性能比较慢，JVM运行效率降低，所以直接将大对象放在老年代）
Java虚拟机规范规定，Java堆可以处于物理上不连续的内存空间中，只要逻辑上是连续的即可。也就是说堆的内存是一块块拼凑起来的。要增加堆空间时，往上“拼凑”（可扩展性）即可，但当堆中没有内存完成实例分配，并且堆也无法再扩展时，将会抛出**OutOfMemoryErro**r异常。
### Java虚拟机栈 （线程私有）
**栈是描述 java 方法执行的内存模型**，每个方法在执行的同时都会创建一个**栈帧（Stack Frame）** 用于存储局部变量表、操作数栈、动态链接、方法出口等信息。每一个方法从调 用直至执行完成的过程，就对应着一个栈帧在虚拟机栈中入栈到出栈的过程
![在这里插入图片描述](https://img-blog.csdnimg.cn/2021060109060959.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQ1NjYxMTI1,size_16,color_FFFFFF,t_70)
 - **栈帧**(StackFrame)是用于支持虚拟机进行方法调用和方法执行的数据结构。栈帧存储了方法的局部变量表、操作数栈、动态连接和方法返回地址等信息。每一个方法从调用至执行完
   成的过程，都对应着一个栈帧在虚拟机栈里从入栈到出栈的过程。
 - **局部变量表**(Local Variable Table)是一组变量值存储空间，用于存放方法参数和方法内定义的局部变量。包括8种基本数据类型、对象引用（reference类型）和returnAddress类型 （指向一条字节码指令的地址）。如果线程请求的栈深度大于虚拟机所允许的深度，将抛出StackOverflowError异常；如果虚拟机栈动态扩展时无法申请到足够的内存时会抛出OutOfMemoryError异常。
 - **操作数栈**(Operand Stack)也称作操作栈，是一个后入先出栈(LIFO)。随着方法执行和字节码指令的执行，会从局部变量表或对象实例的字段中复制常量或变量写入到操作数栈，再随着计算的进行将栈中元素出栈到局部变量表或者返回给方法调用者，也就是出栈/入栈操 作。
 - **动态链接**，Java虚拟机栈中，每个栈帧都包含一个指向运行时常量池中该栈所属方法的**符号引用**，持有这个引用的目的是为了支持方法调用过程中的动态链接(Dynamic Linking)。
 - **方法返回地址**，无论方法是否正常完成，都需要返回到方法被调用的位置，程序才能继续进行

### 程序计数器 （线程私有）
程序计数器是线程私有、占用内存较小、没有OOM异常，主要用于指令切换。
![在这里插入图片描述](https://img-blog.csdnimg.cn/20210601091809369.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQ1NjYxMTI1,size_16,color_FFFFFF,t_70)
程序计数器的作用可以看做是**当前线程所执行的字节码的行号指示器**，字节码解释器工作时就是通过改变计数器的值来选取下一条字节码指令。其中，分支、循环、跳转、异常处理、线程恢复等基础功能都需要依赖计数器来完成。 Java虚拟机的多线程是通过线程轮流切换并分配处理器执行时间的方式来实现的，在任何一个确定的时刻，一个处理器（对于多核处理器来说是一个内核）只会执行一条线程中的指令。因此，为了线程切换后能恢复到正确的执行位置，每条线程都需要有一个独立的程序计 数器，各条线程之间的计数器互不影响，独立存储，我们称这类内存区域为“线程私有”的 内存。
### 本地方法栈 （线程私有的）
和虚拟机栈类似，只不过 Java 虚拟机栈是给 JVM 使⽤的（执行Java方法（字节码）服务），⽽本地⽅法栈是给本地⽅法使⽤的（C/C++）（Native方法服务。）

### 方法区 （线程共享）
方法区也是线程共有的，存储的内容主要有常量、静态变量和类信息。
![在这里插入图片描述](https://img-blog.csdnimg.cn/20210601093800363.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQ1NjYxMTI1,size_16,color_FFFFFF,t_70)
**方法区**即我们常说的**永久代**(Permanent Generation), 用于存储被 JVM 加载的类信息、常量、静态变量、即时编译器编译后的代码等数据. JDK8 已经被元空间取代。

 - **运⾏时常量池**： 运⾏时常量池是⽅法区的⼀部分，Class 文件中除了有 类的版本、字段、方法、接口等描述等信息外，还有一项信息是常量池，用于存放编译期生成的各种字面量和符号引用，这部分内容将在类加载后存放到方法区的运行时常量池中
 - **字⾯量** : 字符串(JDK 8 移动到堆中)、final常量、基本数据类型的值。 
 - **符号引⽤** : 类和结构的完全限定名、字段的名称和描述符、⽅法的名称和描述符。
 
元空间是JDK1.8之后的叫法，<code>元空间存储在本地,而不在虚拟经济当中</code>，并将字符串常量池放到了堆中。
### 内存布局小结
![在这里插入图片描述](https://img-blog.csdnimg.cn/20210601094703942.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQ1NjYxMTI1,size_16,color_FFFFFF,t_70)

# JVM运行时内存结构
# JVM类加载机制
## JVM类加载过程
JVM 类加载机制分为五个部分：加载，验证，准备，解析，初始化，下面我们就分别来看 一下这五个过程。
加载（loading） -> 验证 -> 准备 -> 解析 -> 初始化 -> 使⽤ -> 卸载
![在这里插入图片描述](https://img-blog.csdnimg.cn/2021060110015333.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQ1NjYxMTI1,size_16,color_FFFFFF,t_70)
① **加载** “加载”（Loading）阶段是整个“类加载”（Class Loading）过程中的⼀个阶段。在加载阶段，Java虚拟 机需要完成以下三件事情：

 - 1）通过⼀个类的全限定名来获取定义此类的⼆进制字节流。
 - 2）将这个字节流所代表的静态存储结构转化为⽅法区的运⾏时数据结构。
 - 3）在内存中⽣成⼀个代表这个类的java.lang.Class对象，作为⽅法区这个类的各种数据的访问⼊⼝。

 ② **验证**： 验证是连接阶段的第⼀步，这⼀阶段的⽬的是**确保Class⽂件的字节流中包含的信息符合《Java虚拟机规 范》的全部约束要求**，保证这些信息被当作代码运⾏后不会危害虚拟机⾃身的安全。
验证选项： 
 - ⽂件格式验证
 - 字节码验证
 - 符号引⽤验证...

③ **准备**: 准备阶段是**正式为类中定义的变量（即静态变量，被static修饰的变量）分配内存并设置类变量初始值的阶段**。⽐如此时有这样⼀⾏代码： public static int value = 123;它是初始化 value 的 int 值为 0，⽽⾮ 123。
 ④ **解析**: 解析阶段是 **Java 虚拟机将常量池内的符号引⽤替换为直接引⽤的过程**，也就是初始化常量的过程。 
 ⑤ **初始化**: 初始化阶段，Java 虚拟机真正开始执⾏类中编写的 Java 程序代码，**将主导权移交给应⽤程序。初始化阶段就是执⾏类构造器⽅法的过程。**
 ## 类加载器
虚拟机设计团队把加载动作放到 JVM 外部实现，以便让应用程序决定如何获取所需的类，Java 源程序（.java 文件）在经过 Java 编译器编译之后就被转换成 Java 字节代码（.class 文件） 类加载器负责读取 Java 字节代码，并转换成 java.lang.Class 类的一个实例。 JVM 提供了 3 种类加载器：
![在这里插入图片描述](https://img-blog.csdnimg.cn/20210601192114217.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQ1NjYxMTI1,size_16,color_FFFFFF,t_70)


 - **引导类加载器BootStrap ClassLoader**：负责加载支撑JVM运行的位于JRE的lib目录下核 心类库，比如rt.jar、charsets.jar等
 - **扩展类加载器Extension ClassLoader**：负责加载支撑JVM运行的位于JRE的lib目录下的 ext扩展目录中的JAR类包
 - **应用类加载器Application ClassLoader**：负责加载ClassPath路径下的类包，主要就是加 载你自己写的那些类
 
 ## 双亲委派 
 当一个类收到了类加载请求，他首先不会尝试自己去加载这个类，而是把这个请求委派 给父类去完成，（<code>坑爹</code>)每一个层次类加载器都是如此，因此所有的加载请求都应该传送到引导类加载其中， 只有当父类加载器反馈自己无法完成这个请求的时候 （在它的加载路径下没有找 到所需加载的 Class），子类加载器才会尝试自己去加载。
 优点：
 - **唯一性**：采用双亲委派的一个好处是比如加载位于 rt.jar 包中的类java.lang.Object，不管是哪个加载器加载这个类，最终都是委托给顶层的引导类加载器进行加载，这样就保证了使用不同的类加载器最终得到的都是同样一个 Object 对象
 - **安全性**：自己写的java.lang.String.class类不会被加载，这样便可以防止核心API库被随意篡改

 ## 破坏双亲委派 
 双亲委派模型被破坏总共发⽣过 3 次：
  1. 第⼀次是 JDK 1.2 引⼊双亲委派模型的时候，因为之前在 JDK 就存在了 ClassLoad 代码，所以在 JDK 1.2 为了兼容⽼代码也做过⼀些妥协破坏了双亲委派模型。
  2. 第⼆次是⾃⼰的问题所导致的，当⽗类想要调⽤⼦类的⽅法时，使⽤双亲委派模型就没办法调⽤，这是 第⼆次破坏。 
  3. 第三次是最近⼏年对“热”更新和“热”部署的追求，说⽩了就是希望 Java 应⽤程序能像我们的电脑外设 那样，接上⿏标、U盘，不⽤重启机器就能⽴即使⽤，⿏标有问题或要升级就换个⿏标，不⽤关机也不 ⽤重启对于个⼈电脑来说，重启⼀次其实没有什么⼤不了的，但对于⼀些 ⽣产系统来说，关机重启 ⼀次可能就要被列为⽣产事故，这种情况下热 部署就对软件开发者，尤其是⼤型系统或企业级软件开发者具有很⼤的吸引⼒。
# 垃圾回收与算法
**垃圾回收**（**GC**）是JVM的一大杀器，它使程序员可以更高效地专注于程序的开发设计，而 不用过多地考虑对象的创建销毁等操作。但是这并不是说程序员不需要了解GC。**GC只是 Java编程中一项自动化工具**，任何一个工具都有它适用的范围，当超出它的范围的时候，可 能它将不是那么自动，而是需要人工去了解与适应地适用。
java运行时内存的各个区域。对于程序计数器、虚拟机栈、本地方法栈这三部分区域而言， 其生命周期与相关线程有关，随线程而生，随线程而灭。并且这三个区域的内存分配与回收具有确定性，因为当方法结束或者线程结束时，内存就自然跟着线程回收了。**内存分配和回收关注的为Java堆与方法区这两个区域。**

<code>垃圾回收需要完成的三件事：</code>
**哪些内存需要回收？---如何确定垃圾？**（引用计数法、可达性分析算法）
 **如何回收？**——垃圾回收算法（标记复制（新生代）、标记清除（几乎不用）、标记整理 （老年代）、分代收集）
  **何时回收？**
## 如何判断一个对象"死亡"
### 引用计数法
引用计数描述的算法为: 给对象增加一个<code>引用计数器</code>，每当有一个地方引用它时，计数器就+1；当引用失效时，计数器就-1；任何时刻计数器为0的对象就是不能再被使用的，即对象已"死"。引用计数法实现简单，判定效率也比较高，在大部分情况下都是一个不错的算法。但是，在主流的JVM中没有选用引用计数法来管理内存，**最主要的原因就是引用计数法无法解决对象的循环引用问题**

```cpp
public class test {
        public Object instance = null;
        private byte[] bigSize = new byte[2 * 1024 * 1024];
        public static void testGC() {
            test test1 = new test();
            test test2 = new test();
            test1.instance = test2;
            test2.instance = test1;
            test1 = null;
            test2 = null;
        // 强制jvm进行垃圾回收
            System.gc();
        }
        public static void main(String[] args) {
            testGC();
        }
    }
```
结果如下：
```cpp
[GC	(System.gc())	6092K->856K(125952K),	0.0007504	secs]
```
从结果可以看出，GC日志包含" 6092K->856K(125952K)"，意味着虚拟机并没有因为这两个对象互相引用就不回收他们。即JVM并不使用引用计数法来判断对象是否存活。
### 可达性分析算法（重要）
将“GC Roots” 对象作为起点，从这些节点开始向下搜索引用的对象，找到的对象都标记为非垃圾 对象，其余未标记的对象都是垃圾对象。
![在这里插入图片描述](https://img-blog.csdnimg.cn/20210601142550308.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQ1NjYxMTI1,size_16,color_FFFFFF,t_70)
对象Object5-Object7之间虽然彼此还有关联，但是它们到GC Roots是不可达的，因此他们会被判定为可回收对象。

**在Java语言中，可作为GC Roots的对象包含下面几种:（两个栈，一个方法区）**
 - 1.虚拟机栈(栈帧中的本地变量表)中引用的对象
 - 2.方法区中静态属性引用的对象
 - 3.方法区中常量引用的对象
 - 4.本地方法栈中JNI(Native方法)引用的对象
**生存还是死亡?**
即使在可达性分析算法中不可达的对象，也并非"非死不可"的，这时候他们暂时处在"缓刑"阶段。要宣告一个对象的真正死亡，至少要经历两次标记过程 : 如果对象在进行可达性分析之后发现没有与GC Roots 相连接的引用链，**那它将会被第一次标记并且进行一次筛选**，**筛选的条件是此对象是否有必要执行finalize()方法**。
 - 当对象没有覆盖finalize()方法或者finalize()方法已经被JVM调用过，虚拟机会将这两种情况都视为"没有必要执行"，此时的对象才是真正"死"的对象。
 - 如果这个对象被判定为有必要执行finalize()方法，那么这个对象将会被放置在一个叫做F-Queue的队列之中，并在稍后由一个虚拟机自动建立的、低优先级的Finalizer线程去执行它（这里所说的执行指的是虚拟机会触发finalize()方法）。finalize()方法是对象逃脱死亡的最后一次机会，稍后GC将对F-Queue中的对象进行第二次小规模标记，如果对象在finalize()中成功拯救自己(只需要重新与引用链上的任何一个对象建立起关联关系即可)，那在第二次标记时它将会被移除出"即将回收"的集合；如果对象这时候还是没有逃脱，那基本上它就是真的被回收了。
 - 
**范例:对象自我拯救**
```cpp
public class test {
    public static test test; 
    public void isAlive() {
        System.out.println("I am alive :)");
    }
    @Override
    protected void finalize() throws Throwable { super.finalize();
        System.out.println("finalize method executed!");
        test = this;
    }
    public static void main(String[] args)throws Exception {
        test = new test();
        test = null; System.gc();
        Thread.sleep(500);
        if (test != null) {
            test.isAlive();
        }else {
            System.out.println("no,I am dead :");
        }
        // 下面代码与上面完全一致，但是此次自救失败
        test = null; System.gc();
        Thread.sleep(500);
        if (test != null) {
            test.isAlive();
        }else {
            System.out.println("no,I am dead :");
        }
    }
}
```
从上面代码示例我们发现，finalize方法确实被JVM触发，并且对象在被收集前成功逃脱。
但是从结果上我们发现，两个完全一样的代码片段，结果是一次逃脱成功，一次失败。这是因为，任何一个对象的finalize()方法都只会被系统自动调用一次，如果相同的对象在逃脱一次后又面临一次回收， 它的finalize()方法不会被再次执行，因此第二段代码的自救行动失败。
![在这里插入图片描述](https://img-blog.csdnimg.cn/20210601145431426.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQ1NjYxMTI1,size_16,color_FFFFFF,t_70)
### 常见引用类型有哪些？
 - **强引用**在 Java 中最常见的就是强引用，把一个对象赋给一个引用变量，这个引用变量就是一个强引用。当一个对象被强引用变量引用时，它处于可达状态，它是不可能被垃圾回收机制回收的，即使该对象以后永 远都不会被用到 JVM也不会回收。因此强引用是造成 Java 内存泄漏的主要原因之 一。

```cpp
public static User user = new User();
```

 - **软引用**是用来描述一些还有用但是不是必须的对象。对于软引用关联着的对象，在系统将要发生内存溢出之前，会把这些对象列入回收范围之中进行第二次回收。如果这次回收还是没有足够的内存，才会抛出内存溢出异常。在JDK1.2之后，提供了SoftReference类来实现软引用。
 - **弱引用**将对象用WeakReference弱引用类型的对象包裹，弱引用跟没引用差不多，在下一次的GC会直接回收掉，很少用。
 - **虚引用** : 虚引用也被称为幽灵引用或者幻影引用，它是最弱的一种引用关系。一个对象是否有虚引用的存在，完全不会对其生存时间构成影响，也无法通过虚引用来取得一个对象实例。为一个对象设置虚引用的唯一目的就是能在这个对象被收集器回收时收到一个系统通知（创建及消亡，它的价值只是在垃圾回收的时候触发一个回调方法）。在JDK1.2之后，提供了PhantomReference类来实现虚引用。

## 垃圾回收算法
### 标记-清除算法（不推荐使用）
算法分为“**标记**”和“**清除**”阶段：标记存活的对象， 统一回收所有未被标记的对象(一般选择这种)；也可以反过来，标记出所有需要回收的对象，在标记完成后统一回收所有被标记的对象 。它是最基础的收集算法，比较简单。
![在这里插入图片描述](https://img-blog.csdnimg.cn/2021060115073156.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQ1NjYxMTI1,size_16,color_FFFFFF,t_70)
存在的问题：
 - **效率问题** (如果需要标记的对象太多，效率不高)
 - **空间问题**（标记清除后会产生大量不连续的碎片）内存碎片的问题
### 复制算法(新生代回收算法)
为了解决效率问题，“复制”收集算法出现了。它可以将内存分为大小相同的两块，每次使用其中的一 块。当这一块的内存使用完后，就将还存活的对象复制到另一块去，然后再把使用的空间一次清理掉。这样就使每次的内存回收都是对内存区间的一半进行回收。
![在这里插入图片描述](https://img-blog.csdnimg.cn/20210601150547792.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQ1NjYxMTI1,size_16,color_FFFFFF,t_70)
<code>优点是性能⾼，但内存利⽤率不⾼。

优化：
### 标记-整理算法(老年代回收算法)
**根据老年代的特点特出的一种标记算法**，标记过程仍然与“标记-清除”算法一样，但后续步骤不是直接对可回收对象回收，而是让所有存活的对象向一端移动，然后直接清理掉端边界以外的内存。
![在这里插入图片描述](https://img-blog.csdnimg.cn/20210601151228572.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQ1NjYxMTI1,size_16,color_FFFFFF,t_70)
<code>优点：不会产生内存碎片
### 分代收集算法
分代收集（Generational Collector）算法的将堆内存划分为新生代、老年代和永久代。新生代又被 进一步划分为 Eden 和 Survivor 区，其中 Survivor 由FromSpace（Survivor0）和ToSpace（Survivor1）组成。
通过new创建的对象的内存都在堆中分配，其大小可以通过-Xmx和-Xms来控制。分代收集，是基于 这样一个事实：不同的对象的生命周期是不一样的。因此，可以将不同生命周期的对象分代，不同的代采 取不同的回收算法进行垃圾回收，以便提高回收效率。

 - 当前虚拟机的垃圾收集都采用分代收集算法，这种算法没有什么新的思想，**只是根据对象存活周期的不同将内存分为几块**。一般将java堆分为新生代和老年代，这样我们就可以根据各个年代的特点选择合适的垃圾收集算法。
 - 比如在新生代中，每次收集都会有大量对象(近99%)死去，所以可以选择标记-复制算法，只需要付出少量对象的复制成本就可以完成每次垃圾收集。而老年代的对象存活几率是比较高的，而且没有额外的空间对它进行分配担保，所以我们必须选择“标记-清除”或“标记-整理”算法进行垃圾收集。注意，<code>“标记-清除”或“标记-整理”算法会比复制算法慢10倍以上。</code>
 - 
特别地，在分代收集算法中，对象的存储具有以下特点： 
 - 1、对象优先在 Eden 区分配。 
 -  2、大对象直接进入老年代。
 - 3、长期存活的对象将进入老年代，默认为 15 岁。
## 何时回收
**何时回收之前，先了解一下几种 GC。**
 - **Minor GC**：该 GC 会清理年轻代的内存，因为Java对象大多都会快速销毁的特性，因此Minor GC(采用复制算法)非常频繁，一般回收速度也比较快。GC 时会触发 "全世界的暂停"。
 - **Major GC/Full GC**：指发生在老年代的垃圾收集。出现了Major GC，经常会伴随至少一次的Minor GC(并非绝对，在Parallel Scavenge收集器中就有直接进行Full GC的策略选择过程)。Major GC的速度一般会比Minor GC慢10倍以上。
**如下是几种 GC 的触发场景：** 
 - 执行 system.gc() 的时候
 - 老年代空间不足，GC 之后，空间不足会触发 outofmemoryError
 - 永久代空间不足，GC 之后，空间不足会触发 java.outofMemory PerGen Space
 - Minor GC之后 Survior放不下，放入老年代，老年代也放不下，触发
 - FullGC，或者新生代 有对象放入老年代，老年代放不下，触发FullGC
   新生代晋升为老年代时候，老年代剩余空间低于新生代晋升为老年代的速率，会触发老年代回收
 - new 一个大对象，新生代放不下，直接到老年代，空间不够，触发FullGC

# GC垃圾收集器
Java 堆内存被划分为新生代和年老代两部分，新生代主要使用标记-复制和标记-清除 垃圾回收算法； 年老代主要使用标记-整理垃圾回收算法，因此 java 虚拟中针对新生代和 年老代分别提供了多种不同的垃圾收集器，JDK Sun HotSpot 虚拟机的垃圾收集器如下：
![在这里插入图片描述](https://img-blog.csdnimg.cn/20210601153207891.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQ1NjYxMTI1,size_16,color_FFFFFF,t_70)
上图展示了7种作用于不同分代的收集器，如果两个收集器之间存在连线，就说明他们之间可以搭配使用。所处的区域，表示它是属于新生代收集器还是老年代收集器。在讲具体的收集器之前我们先来明确三个概念:

 - **并行**(Parallel) : 指多条垃圾收集线程并行工作，用户线程仍处于等待状态
 - **并发**(Concurrent) :指用户线程与垃圾收集线程同时执行(不一定并行，可能会交替执行)，用户程序继续运行，而垃圾收集程序在另外一个CPU上。
 - **吞吐量**:就是CPU用于运行用户代码的时间与CPU总消耗时间的比值。吞吐量 = 运行用户代码时间 - 垃圾收集时间
## 串行垃圾回收器
在JDK1.3.1之前，单线程回收器是唯一的选择。它的单线程意义不仅仅是说它只会使用 一个CPU或一个收集线程去完成垃圾收集工作。而且它进行垃圾回收的时候，必须暂停其他 所有的工作线程（Stop The World,STW），直到它收集完成。它适合Client模式的应用，在单CPU环境下，它简单高效，由于没有线程交互的开销，专心垃圾收集自然可以获得最高的单线程效率。
串行的垃圾收集器有两种，**Serial**与**Serial Old**，一般两者搭配使用。**新生代采用 Serial，是利用复制算法；老年代使用Serial Old采用标记-整理算法**
Client应用或者命令行程序可以，通过<code>-XX:+UseSerialGC</code>可以开启上述回收模式。下 图是其运行过程示意图。
![在这里插入图片描述](https://img-blog.csdnimg.cn/20210601154248553.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQ1NjYxMTI1,size_16,color_FFFFFF,t_70)
## 并行垃圾回收器
整体来说，并行垃圾回收相对于串行，是通过多线程运行垃圾收集的。也会stop-the- world。适合Server模式以及多CPU环境。一般会和jdk1.5之后出现的CMS搭配使用。并行的垃圾回收器有以下几种
 - **ParNew**：Serial收集器的多线程版本，默认开启的收集线程数和cpu数量一样，运行数量可以通过修改ParallelGCThreads设定。用于新生代收集，<code>复制算法</code>。使用<code>- XX:+UseParNewGC </code>和 SerialOld收集器组合进行内存回收。如下图所示。
![在这里插入图片描述](https://img-blog.csdnimg.cn/20210601154628127.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQ1NjYxMTI1,size_16,color_FFFFFF,t_70)
 - **Parallel Scavenge**: **关注吞吐量,吞吐量优先**，吞吐量=代码运行时间/(代码运行时间+垃圾收集时间),也就是高效率利用cpu时间，尽快完成程序的运算任务可以设置最大停顿 时间MaxGCPauseMillis以及，吞吐量大小GCTimeRatio。如果设置XX:+UseAdaptiveSizePolicy参数，则随着GC,会动态调整新生代的大小，Eden,Survivor比例等，以提供最合适的停顿时间或者最大的吞吐量。用于新生代收集，复制算法。通过-XX:+UseParallelGC参数，Server模式下默认提供了其和SerialOld进行搭配的分代收集方式。
 - **Parllel Old**：Parallel Scavenge的老年代版本。JDK 1.6开始提供的。在此之前 ParallelScavenge的地位也很尴尬，而有了Parllel Old之后，通过</code>- XX:+UseParallelOldGC</code>参数使用ParallelScavenge + Parallel Old器组合进行内存回收， 如下图所示。
![在这里插入图片描述](https://img-blog.csdnimg.cn/20210601154855149.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQ1NjYxMTI1,size_16,color_FFFFFF,t_70)

## Serial收集器 （单线程+复制算法）
Serial收集器是最基本、发展历史最悠久的收集器，曾经（在JDK 1.3.1之前）是虚拟机新生代收集的唯一选择。
**特性：**
这个收集器是一个**单线程的收集器**，但它的“单线程”的意义并不仅仅说明它只会使用一个CPU或一条收集线程去完成垃圾收集工作，更重要的是在它进行垃圾收集时，必须暂停其他所有的工作线 程，直到它收集结束(Stop The World).
**应用场景:**
Serial收集器是虚拟机运行在Client模式下的默认新生代收集器。
**优势:**
简单而高效（与其他收集器的单线程比），对于限定单个CPU的环境来说，Serial收集器由于没有线程交互的开销，专心做垃圾收集自然可以获得最高的单线程收集效率。 实际上到现在为止 : 它依然是虚拟机运行在Client模式下的默认新生代收集器
## Serial Old收集器（单线程+标记-整理算法）
Serial Old是Serial收集器的老年代版本，它同样是一个单线程收集器，使用标记－整理算法。
![在这里插入图片描述](https://img-blog.csdnimg.cn/20210601233236764.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQ1NjYxMTI1,size_16,color_FFFFFF,t_70)

**应用场景：**

 - Serial Old收集器的主要意义也是在于给Client模式下的虚拟机使用。
 - 如果在Server模式下，那么它主要还有两大用途：一种用途是在JDK 1.5以及之前的版本中与ParallelScavenge收集器搭配使用，另一种用途就是作为CMS收集器的后备预案，在并发收集发生Concurrent Mode Failure时使用。

## ParNew收集器 （多线程+Serial）
ParNew 垃圾收集器其实是 Serial 收集器的多线程版本，也使用复制算法，除了使用多线程进行垃圾 收集之外，其余的行为和 Serial 收集器完全一样，ParNew 垃圾收集器在垃圾收集过程中同样也要暂停所 有其他的工作线程。

**对比分析: 与Serial收集器对比:**

 - ParNew收集器在单CPU的环境中绝对不会有比Serial收集器更好的效果，甚至由于存在线程交互的开销，该收集器在通过超线程技术实现的两个CPU的环境中都不能百分之百地保证可以超越Serial收集器。然而，随着可以使用的CPU的数量的增加，它对于GC时系统资源的有效利用还是很有好处的。
![在这里插入图片描述](https://img-blog.csdnimg.cn/20210601234047620.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQ1NjYxMTI1,size_16,color_FFFFFF,t_70)

<code>ParNew收集器是许多运行在Server模式下的虚拟机首选的新生代收集器，其中一个原因是，除了 Serial收集器之外，目前只有ParNew收集器能与CMS收集器配合工作</code>

**为什么只有ParNew能与CMS收集器配合？**

 - CMS是HotSpot在JDK1.5推出的第一款真正意义上的并发（Concurrent） 收集器，第一次实现了让垃圾收集线程与用户线程（基本上）同时工作；
 - CMS作为老年代收集器，但却无法与JDK1.4已经存在的新生代收集器Parallel Scavenge配合工作
 - 因为Parallel Scavenge（以及G1）都没有使用传统的GC收集器代码框架，而另外独立实现；而其余几种收集器则共用了部分的框架代码

## <code>CMS收集器（并发）
Concurrent mark sweep(CMS)收集器是一种年老代垃圾收集器，其最主要目标是获取最 短垃圾回收停顿时间，和其他年老代使用标记-整理算法不同，它使用多线程的标记-清除算 法。最短的垃圾收集停顿时间可以为交互比较高的程序提高用户体验。
<code>缩短回收停顿时间为目标、注重用户体验；真正意义并发收集器、让垃圾收集线程与用户线程（基本上） 同时工作。
![在这里插入图片描述](https://img-blog.csdnimg.cn/20210601234810376.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQ1NjYxMTI1,size_16,color_FFFFFF,t_70)

CMS收集器是基于“标记—清除”算法实现的，它的运作过程相对于前⾯⼏种收集器来说更复 杂⼀些，整个过程分为4个步骤：

 - **初始标记**（CMS initial mark）初始标记仅仅只是标记⼀下GC Roots能直接关联到的对 象，速度很快，需要“Stop The
   World”。
 - **并发标记**（CMS concurrent mark）并发标记阶段就是进⾏GC Roots Tracing的过程。
 - **重新标记**（CMS remark）重新标记阶段是为了修正并发标记期间因⽤户程序继续运作⽽导致标记产⽣变动的那⼀部分对象的标记记录，这个阶段的停顿时间⼀般会⽐初始标记阶 段稍⻓⼀些，但远⽐并发标记的时间短，仍然需要“StopThe World”。
 - **并发清除**（CMS concurrent sweep）并发清除阶段会清除对象。

**特点** 
 - 针对老年代；
 - 基于"标记-清除"算法(不进行压缩操作，会产生内存碎片)；
 - 以获取最短回收停顿时间为目标；
 - 并发收集、低停顿； 需要更多的内存；
 - CMS是HotSpot在JDK1.5推出的第一款真正意义上的并发（Concurrent）收集器； 第一次实现了让垃圾收集线程与用户线程（基本上）同时工作。
   **应用场景**
 - 与用户交互较多的场景；（如常见WEB、B/S-浏览器/服务器模式系统的服务器上的应用）
 - 希望系统停顿时间最短，注重服务的响应速度；
 - 以给用户带来较好的体验。


<code>优点：并发收集、低停顿。 
缺点： 一：CMS收集器对CPU资源非常敏感。二.CMS收集器无法处理浮动垃圾
## Parallel Scavenge收集器 （多线程+标记-复制算法、高效）
Parallel Scavenge收集器是一个新生代收集器，它也是使用复制算法的收集器，又是并行的多线程收集器。
Parallel Scavenge收集器使用两个参数控制吞吐量：
 - XX:MaxGCPauseMillis控制最大的垃圾收集停顿时间
 - XX:GCRatio 直接设置吞吐量的大小

直观上，只要最大的垃圾收集停顿时间越小，吞吐量是越高的，但是GC停顿时间的缩短是以牺牲吞吐量和新生代空间作为代价的。比如原来10秒收集一次，每次停顿100毫秒，现在变成5秒收集一次，每次停
顿70毫秒。停顿时间下降的同时，吞吐量也下降了。

**应用场景：**
停顿时间越短就越适合需要与用户交互的程序，良好的响应速度能提升用户体验，而高吞吐量则可以高效率地利用CPU时间，尽快完成程序的运算任务，主要适合在后台运算而不需要太多交互的任务。
**对比分析：**

 - Parallel Scavenge收集器 VS CMS等收集器：

Parallel Scavenge收集器的特点是它的关注点与其他收集器不同，CMS等收集器的关注点是尽可能地缩短垃圾收集时用户线程的停顿时间，而Parallel Scavenge收集器的目标则是达到一个可控制的吞吐量（Throughput）。由于与吞吐量关系密切，Parallel Scavenge收集器也经常称为“吞吐量优先”收集器。

 - Parallel Scavenge收集器 VS ParNew收集器：

Parallel Scavenge收集器与ParNew收集器的一个重要区别是它具有自适应调节策略。
**GC自适应的调节策略：**
Parallel Scavenge收集器有一个参数- XX:+UseAdaptiveSizePolicy 。当这个参数打开之后，就不需要手工指定新生代的大小、Eden与Survivor区的比例、晋升老年代对象年龄等细节参数了，虚拟机会根据当前系统的运行情况收集性能监控信息，动态调整这些参数以提供最合适的停顿时间或者最大的吞吐量，这种调节方式称为GC自适应的调节策略（GC Ergonomics）。
## Parallel Old收集器 （多线程+标记-整理算法）
Parallel Old 收集器是 Parallel Scavenge 的年老代版本，使用多线程的标记-整理算 法，在 JDK1.6 才开始提供。
 在 JDK1.6 之前，新生代使用 ParallelScavenge 收集器只能搭配年老代的 Serial Old 收集器，只 能保证新生代的吞吐量优先，无法保证整体的吞吐量，Parallel Old 正是为了 在年老代同样提供吞吐量优先的垃圾收集器，如果系统对吞吐量要求比较高，可以优先考虑 新生代 Parallel Scavenge 和年老代 Parallel Old 收集器的搭配策略
![在这里插入图片描述](https://img-blog.csdnimg.cn/20210601234432856.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQ1NjYxMTI1,size_16,color_FFFFFF,t_70)
**特点** 

 - 针对老年代；
 - 采用"标记-整理"算法；
 - 多线程收集。

 **应用场景** 
 - JDK1.6及之后用来代替老年代的Serial Old收集器；
 - 特别是在Server模式，多CPU的情况下；
 - 这样在注重吞吐量以及CPU资源敏感的场景，就有了Parallel Scavenge（新生 代）加Parallel Old（老年代）收集器的"给力"应用组合。

## <code>G1收集器
Garbage first 垃圾收集器是目前垃圾收集器理论发展的最前沿成果，相比与 CMS 收集器，G1 收 集器两个最突出的改进是：会进行压缩
 - 基于标记-整理算法，不产生内存碎片。
 - 可以非常精确控制停顿时间，在不牺牲吞吐量前提下，实现低停顿垃圾回收。

G1（Garbage First）垃圾回收器是用在heap memory很大的情况下，把heap划分为很多很多的region块，然后并行的对其进行垃圾回收。
G1垃圾回收器在清除实例所占用的内存空间后，还会做内存压缩。
G1垃圾回收器回收region的时候基本不会STW，而是基于 most garbage优先回收(整体来看是基于"标记-整理"算法，从局部(两个region之间)基于"复制"算法) 的策略来对region进行垃圾回收的。无论如何，G1收集器采用的算法都意味着一个region有可能属于Eden，Survivor或者Tenured内存区域。图中的E表示该region属于Eden内存区域，S表示属于Survivor内存区域，T表示属于Tenured内存区域。图中空白的表示未使用的内存空间。    G1垃圾收集器还增加了一种新的内存区域，叫做Humongous内存区域，如图中的H块。这种内存区域主要用于存储大对象-即大小超过一个region大小的50%的对象
![在这里插入图片描述](https://img-blog.csdnimg.cn/20210601235631565.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQ1NjYxMTI1,size_16,color_FFFFFF,t_70)
**年轻代垃圾收集**

在G1垃圾收集器中，年轻代的垃圾回收过程使用复制算法。把Eden区和Survivor区的对象复制到新的Survivor区域。
![在这里插入图片描述](https://img-blog.csdnimg.cn/20210601235732405.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQ1NjYxMTI1,size_16,color_FFFFFF,t_70)
**老年代垃收集**
对于老年代上的垃圾收集，G1垃圾收集器也分为4个阶段，基本跟CMS垃圾收集器一样，但略有不同：

 - **初始标记**(Initial Mark)阶段 - 同CMS垃圾收集器的InitialMark阶段一样，G1也需要暂停应用程序的执行，它会标记从根对象出发，在根对象的第一层孩子节点中标记所有可达的对象。 但是G1的垃圾收集器的Initial  Mark阶段是跟minor gc一同发生的。也就是说，在G1中，你不用像在CMS那样，单独暂停应用程序的执行来运行InitialMark阶段，而是在G1触发minor gc的时候一并将年老代上的Initial Mark给做了。
 - **并发标记**(Concurrent Mark)阶段 -在这个阶段G1做的事情跟CMS一样。但G1同时还多做了一件事情，就是如果在Concurrent Mark阶段中，发现哪些Tenuredregion中对象的存活率很小或者基本没有对象存活，那么G1就会在这个阶段将其回收掉，而不用等到后面的cleanup阶段。这也是Garbage First名字的由来。同时,在该阶段，G1会计算每个 region的对象存活率，方便后面的cleanup阶段使用 。
 - **最终标记**(CMS中的Remark阶段) - 在这个阶段G1做的事情跟CMS一样, 但是采用的算法不同，G1采用一种叫做SATB(snapshot-at-the-begining)的算法能够在Remark阶段更快的标记 可达对象。
 - **筛选回收**(Clean up/Copy)阶段 - 在G1中，没有CMS中对应的Sweep阶段。相反 它有一个 Clean  up/Copy阶段，在这个阶段中,G1会挑选出那些对象存活率低的region进行回收，这个阶段也是和minorgc一同发生的,如下图所示：
![在这里插入图片描述](https://img-blog.csdnimg.cn/20210602000023964.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQ1NjYxMTI1,size_16,color_FFFFFF,t_70)
G1（Garbage-First）是一款面向服务端应用的垃圾收集器。HotSpot开发团队赋予它的使命是未来可以    替换掉JDK 1.5中发布的CMS收集器。 如果你的应用追求低停顿，G1可以作为选择；如果你的应用追求吞吐量，G1并不带来特别明显的好处。

