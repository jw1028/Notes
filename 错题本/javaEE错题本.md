                                              **JavaEE错题本**

1.下面有关JAVA异常类的描述，说法错误的是？

A. 异常的继承结构：基类为Throwable，Error和Exception继承Throwable，RuntimeException和IOException等继承Exception

B.非RuntimeException一般是外部错误(非Error)，其必须被 try{}catch语句块所捕获

C. Error类体系描述了Java运行系统中的内部错误以及资源耗尽的情形，Error不需要捕捉

D.RuntimeException体系包括错误的类型转换、数组越界访问和试图访问空指针等等，必须被 try{}catch语句块所捕获

解析：

B编译时期异常不一定要用try{}catch捕获（例如cloneable）也可以用throws显示，在后续的代码中使用try{}catch处理，但也可以交给jvm来处理。但要处理异常的话一定要用try{}catch来捕获。

D可以不用被try{}catch捕获，可以交给jvm来处理

2.指出下列程序运行的结果（）

```
public class Example{
    String str = new String("good");
    char[ ] ch = { 'a' , 'b' , 'c' };
    public static void main(String args[]){
        Example ex = new Example();
        ex.change(ex.str,ex.ch);
        System.out.print(ex.str + " and ");
        System.out.print(ex.ch);
    }
    public void change(String str,char ch[ ]){
        str = "test ok";
        ch[0] = 'g';
    }
}
```

解析：画图解决，change（）只要传值传参

![image-20210121155147680](C:\Users\86131\AppData\Roaming\Typora\typora-user-images\image-20210121155147680.png)

3、下面代码将输出什么内容：false

```
public class SystemUtil{
	public static boolean isAdmin(String userId){
		return userId.toLowerCase()=="admin";
	}
	public static void main(String[] args){
		System.out.println(isAdmin("Admin"));
	}
}
```

解析：toLowerCase新new一个String返回   admin在字符常量池，而返回在堆上

4、下面代码将输出什么内容 true false

```java
   public static void main(String[] args) {
        Integer a = 100;
        Integer b = 100;
        Integer c = 200;
        Integer d = 200;
        System.out.println(a == b);
        System.out.println(c == d);
    }
    输出结果为
    true
    false

```

Interger自动装包的底层会调用Integer.valueOf()，Integer.valueOf()底层代码如下，如果传入的i值大于等于-128小于等于127时会返回数组中的值。如果不是的话会new一个新的对象将其存储然后返回。所以上面的ab在范围内，返回的都是 数组中得引用，所以相同，二cd超出了范围，所以分别new了两个新的对象，所以不同。
![在这里插入图片描述](https://img-blog.csdnimg.cn/20210121193218314.png)

5.用命令方式运行以下代码的运行结果是 C

命令: java f a b c 

```java
public class f{
   public static void main(String[] args){
   String foo1 = args[1];
   String foo2 = args[2];
   String foo3 = args[3];
 }
}
```

A 程序编译错误 

B a b c

 C 程序运行错误 

D f

解析：编译时不会到错，但运行时会报错（数组下标越界）从0开始存

6.选项中的哪一行代码可以替换题目中的   A

```c
publicat abstract class MyClass{
	public int constint = 5;
	// add code here
	public void method(){
	}
}

```

A、public abstract void method(int a);

B、constint = constint + 5；

C、public int method()；

D、public abstract void anotherMethod(){};

解析：A：该方法是抽象方法，所以没有方法体，和题目中的method()方法构成了方法重载（方法名一致，参数不一致），所以是正确的，A项正确

B：类体中只能定义变量和方法，不能有其他语句，所以B项错误

C：选项中的方法和类中的方法重复，所以会发生编译异常，所以C项错误

D：该项方法有abstract修饰，所以是抽象方法，由于抽象方法不能有方法体，所以D项错误

7.下列对泛型的理解错误的是  D

```html
A  虚拟机中没有泛型，只有普通类和普通方
B  所有泛型类的类型参数在编译时都会被擦除
C  创建泛型对象时请指明类型，让编译器尽早的做参数检查
D  泛型的类型擦除机制意味着不能在运行时动态获取List<T>中T的实际类型
```

解析：A虚拟机中没有泛型，只有普通类和普通方法

B.所有泛型类的类型参数在编译时都会被擦除

C.创建泛型对象的时候，一定要指出类型变量T的具体类型。争取让编译器检查出错误，而不是留给JVM运行的时候抛出类不匹配的异常

D.可以通过反射机制获得

8.以下抽象类定义中的错误是什么  C

```java
abstract class xy
{
    abstract sum (int x, int y) { }
}

```

A.没有错误  

B.类标题未正确定义

 C.方法没有正确定义 

D.没有定义构造函数 

解析： 抽象方法不能有函数体（具体实现）  缺少返回值

9.阅读下列哪些是正确的    CDE

```java
Integer s=new Integer(9);
Integer t=new Integer(9);
Long u=new Long(9);
```

```
A.（s==u)
B.(s==t)
C.(s.equals(t))
D.(s.equals(9))
E.(s.equals(new Integer(9))
```

解析：主要说下E吧 直接创建了一个新的 Integer 实例，但且值也为 9 ，所以，满足条件，返回真。

10.下列程序的输出结果为 false true

```java
Integer a = 1000, b = 1000; 
System.out.println(a == b);//1 false
Integer c = 100, d = 100; 
System.out.println(c == d);//2 true
```

解析：Integer a = 1000 它的内部就是这样的：  Integer i = Integer.valueOf(1000);

而valueOf方法内部会去取缓存（**默认范围 [-128, 127]**） ，不会创建新对象。看Integer源码

11.下面的switch语句中，x可以是哪些类型的数据：BD

```
switch(x)
{
	default:
	System.out.println("Hello");
}
```

```
A.long B.char C.float D.byte E.double F.Object
```

解析：以java8为准，switch支持10种类型 基本类型：**byte char short in**t 对于包装类 ：**Byte,Short,Character,Integer String** enum



