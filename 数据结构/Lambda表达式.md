# Lambda表达式

**背景**

**Lambda**表达式是**Java SE 8**中一个重要的新特性。lambda表达式允许你通过表达式来代替功能接口。  lambda表达式就和方法一样,它提供了一个正常的参数列表和一个使用这些参数的主体(body,可以是一个表达式或一个代码块)。 **Lambda 表达式**可以看作是一个**匿名函数**。

# 基础语法

**基本语法: (parameters) -> expression 或 (parameters) ->{ statements; }** 

**Lambda表达式由三部分组成：**

 - 1.p**aramaters**：类似方法中的形参列表，这里的参数是函数式接口里的参数。这里的参数类型可以明确的声明    也可不声明而由JVM隐含的推断。另外当只有一个推断类型时可以省略掉圆括号。
 - 2.**->**：可理解为“被用于”的意思
 - 3.**方法体**：可以是表达式也可以代码块，是函数式接口里方法的实现。代码块可返回一个值或者什么都不反  回，这里的代码块块等同于方法的方法体。如果是表达式，也可以返回一个值或者什么都不反回。

举例

```java
// 1. 不需要参数,返回值为 2
() -> 2

// 2. 接收一个参数(数字类型),返回其2倍的值
x -> 2 * x

// 3. 接受2个参数(数字),并返回他们的和
(x, y) -> x + y

// 4. 接收2个int型整数,返回他们的乘积
(int x, int y) -> x * y

// 5. 接受一个 string 对象,并在控制台打印,不返回任何值(看起来像是返回void) 
(String s) -> System.out.print(s)
```

## 函数式接口

要了解**Lambda表达式**,首先需要了解什么是**函数式接口**，函数式接口定义：一个接口有且只有一个抽象方法 。
**注意：**

 - 1.如果一个接口只有一个抽象方法，那么该接口就是一个函数式接口
 - 2.如果我们在某个接口上声明了	注解，那么编译器就会按照函数式接口的定义来要求 该接口，这样如果有两个抽象方法，程序编译就会报错的。所以，从某种意义上来说，只要你保证你的接口 
   中只有一个抽象方法，你可以不加这个注解。加上就会自动进行检测的。

**定义方式：**

```java
@FunctionalInterface
interface NoParameterNoReturn {
//注意：只能有一个方法
	void test();
}
```

但这种方式也是可以的

```java
@FunctionalInterface
interface NoParameterNoReturn { 
	void test();
	default void test2() {
		System.out.println("JDK1.8新特性，default默认方法可以有具体的实现");
	}
}
```

# Lambda表达式的基本使用

首先，我们实现准备好几个接口：

```java
//无返回值无参数
@FunctionalInterface
interface NoParameterNoReturn {
    void test();
}
//无返回值一个参数
@FunctionalInterface
interface OneParameterNoReturn {
    void test(int a);
}
//无返回值多个参数
@FunctionalInterface
interface MoreParameterNoReturn {
    void test(int a,int b);
}
    //有返回值无参数
@FunctionalInterface interface NoParameterReturn {
    int test();
}
//有返回值一个参数
@FunctionalInterface interface OneParameterReturn {
    int test(int a);
}
//有返回值多参数
@FunctionalInterface
interface MoreParameterReturn { 
    int test(int a,int b);
}
```

我们在上面提到过，**Lambda表达式本质是一个匿名函数**，函数的方法是：**返回值** **方法名** **参数列表** **方法体**。在**Lambda表达式**中我们只需要关心：**参数列表 方法体**。
具体使用见以下示例代码：

```java
public class TestDemo {
    public static void main(String[] args) {
        NoParameterNoReturn noParameterNoReturn = () -> {
            System.out.println("无参数无返回值");
        };
        
        noParameterNoReturn.test();
        OneParameterNoReturn oneParameterNoReturn = (int a) -> {
            System.out.println("无参数一个返回值：" + a);
        };
        oneParameterNoReturn.test(10);
        
        MoreParameterNoReturn moreParameterNoReturn = (int a, int b) -> {
            System.out.println("无返回值多个参数：" + a + " " + b);
        };
        moreParameterNoReturn.test(20, 30);
        NoParameterReturn noParameterReturn = () -> {
            System.out.println("有返回值无参数！");
            return 40;
        };
        //接收函数的返回值
        int ret = noParameterReturn.test();
        System.out.println(ret);
        OneParameterReturn oneParameterReturn = (int a) -> {
            System.out.println("有返回值有参数！");
            return a;
        };

        ret = oneParameterReturn.test(50);
        System.out.println(ret);

        MoreParameterReturn moreParameterReturn = (int a, int b) -> {
            System.out.println("有返回值多个参数！");
            return a + b;
        };
        ret = moreParameterReturn.test(60, 70);
        System.out.println(ret);
    }
}
```

**语法精简**

 - 1.参数类型可以省略，如果需要省略，每个参数的类型都要省略。
 - 2.参数的小括号里面只有一个参数，那么小括号可以省略
 - 3.如果方法体当中只有一句代码，那么大括号可以省略
 - 4.如果方法体中只有一条语句，其是return语句，那么大括号可以省略，且去掉return关键字。

举例

```java
  public static void main(String[] args) {
        MoreParameterNoReturn moreParameterNoReturn = (a, b) -> {
            System.out.println("无返回值多个参数，省略参数类型：" + a + " " + b);
        };
        moreParameterNoReturn.test(20, 30);

        OneParameterNoReturn oneParameterNoReturn = a -> {
            System.out.println("无参数一个返回值,小括号可以胜率：" + a);
        };
        oneParameterNoReturn.test(10);

        NoParameterNoReturn noParameterNoReturn = () ->
                System.out.println("无参数无返回值，方法体中只有一行代码");
        noParameterNoReturn.test();

        //方法体中只有一条语句，且是return语句
        NoParameterReturn noParameterReturn = () -> 40;
        int ret = noParameterReturn.test();
        System.out.println(ret);
    }
```

# 变量的捕获

**Lambda** 表达式中存在变量捕获 ，了解了变量捕获之后，我们才能更好的理解Lambda 表达式的作用域 。**Java当中的匿名类中，会存在变量捕获。**

## 匿名类中的变量捕获

```java
class Test {
    public void func(){ System.out.println("func()");
    }
}
public class TestDemo {
    public static void main(String[] args) { 
        int a = 100;
        new Test(){
        //a=99  err
            @Override
            public void func() {
                System.out.println("我是内部类，且重写了func这个方法！"); System.out.println("我是捕获到变量 a == "+a
                        +" 我是一个常量，或者是一个没有改变过值的变量！");
            }
        };
    }
}
```

在上述代码当中的变量**a**就是，捕获的变量。**这个变量要么是被ﬁnal修饰，如果不是被ﬁnal修饰的 你要保证在使用之前，没有修改。如下代码就是错误的代码。**


## Lambda中的变量捕获

在**Lambda**当中也可以进行变量的捕获，具体我们看一下代码。

```java
public static void main(String[] args) { 
    int a = 10;
    NoParameterNoReturn noParameterNoReturn = ()->{
        // a = 99; error 
     System.out.println("捕获变量："+a);
        };
        noParameterNoReturn.test();
    }
}
```

# Lambda在集合当中的使用

为了能够让**Lambda**和**Java**的集合类集更好的一起使用，集合当中，也新增了部分接口，以便与Lambda表达式对接。
![在这里插入图片描述](https://img-blog.csdnimg.cn/20210305183322140.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQ1NjYxMTI1,size_16,color_FFFFFF,t_70)


 - Collection接口foreach（）方法演示


```java
public static void main(String[] args) { 
    ArrayList<String> list = new ArrayList<>(); 
        list.add("Hello");
        list.add("bit");
        list.add("hello");
        list.add("lambda");
//表示调用一个，不带有参数的方法，其执行花括号内的语句，为原来的函数体内容。
        list.forEach(s -> {
        System.out.println(s);
        });
}
```

 - List中sort（）方法演示


```java
public static void main(String[] args) { 
    ArrayList<String> list = new ArrayList<>(); 
        list.add("Hello");
        list.add("bit");
        list.add("hello");
        list.add("lambda");
//调用带有2个参数的方法，且返回长度的差值
     list.sort((str1,str2)-> str1.length()-str2.length()); 
     System.out.println(list);
}
```

 - HashMap中的foreach（）演示


```java
public static void main(String[] args) { 
    HashMap<Integer, String> map = new HashMap<>(); 
        map.put(1, "hello");
        map.put(2, "bit");
        map.put(3, "hello");
        map.put(4, "lambda");
        map.forEach((k,v)-> System.out.println(k + "=" + v));
}
```

# Lambda的优点和缺点

**优点：**

 - 1.代码简洁，开发迅速
 - 2.方便函数式编程
 - 3.非常容易进行并行计算
 - 4.Java 引入 Lambda，改善了集合操作

**缺点：**

 - 1.代码可读性变差
 - 2.在非并行计算中，很多计算未必有传统的 for 性能要高
 - 3.不容易进行调试
