### 继承

# 背景

代码中创建的类, 主要是为了抽象现实中的一些**事物**(包含属性和方法).
有的时候客观事物之间就存在一些关联关系（它们中有一些相同的特征，具有一些共有的东西） 那么在表示成类和对象的时候也会存在一定的关联.

## 举例

例如, 设计一个类Animal表示动物，它有name和age两个字段，还有吃的行为。然后再新建两个Dog和Bird类（它们有name和age两个字段，还有吃的行为）

```java
class Animal{
    public String name;
    public int age;
    public void eat(){
        System.out.println("动物吃");
    }
}
class Dog {
    public String name;
    public int age;

    public void eat() {
        System.out.println("狗吃");
    }
}

class Bird {
    public String name;
    public int age;

    public void eat() {
        System.out.println("鸟吃");
    }
    public void fly() {
        System.out.println("鸟飞");
    }
}

public class Test {
    public static void main(String[] args) {
        Dog  dog=new Dog();
        dog.eat();
        System.out.println();
    }
}
输出结果为“狗吃”

```

## 分析

这个代码我们发现其中存在了大量的冗余代码.
仔细分析, 我们发现 Animal 和 Dog 以及 Bird 这几个类中存在一定的关联关系:

- 这三个类都具备相同的 name和age 属性, 而且意义是完全一样的
- 这三个类都具备一个相同的 eat 方法, 而且行为是完全一样的.
- 从逻辑上讲, Dog 和 Bird 都是一种 Animal (is - a 语义).

## 引出继承

此时我们就可以让 Dog和 Bird 分别继承 Animal 类, 来达到代码重用的效果.
此时, Animal 这样被继承的类, 我们称为 **父类 , 基类 或 超类**, 对于像 Dog 和 Bird 这样的类, 我们称为 **子类, 派生类**（和现实中的儿子继承父亲的财产类似）, 子类也会继承父类的字段和方法, 但也可以增加自己特有的行为或方法（如鸟会飞）以达到代码重用的效果.

# 语法规则

## 基本语法

```java
class 子类 extends 父类 {

}

```

- 使用 **extends**关键字指定父类
- Java 中**一个子类只能继承一个父类** (是单继承而C++/Python等语言支持多继承)，想要**多继承**的话需要使用**接口**。
- 子类会继承父类的所有 **public** 的字段和方法（类似于爸爸的钱）
- 对于父类的 **private** 的字段和方法, 子类中是无法访问的.（类似于爸爸的情人）
- **子类的实例中, 也包含着父类的实例. 可以使用 super 关键字得到父类实例的引用.**（重点）

此时我们便可以修改上面的代码了。我们删除Dog和Bird的name、age吃，然后继承Animal。但extends 英文原意指 “扩展”. 而我们所写的类的继承, 也可以理解成基于父类进行代码上的 “扩展”.例如我们写的 Bird 类, 就是在 Animal 的基础上扩展出了 ﬂy 方法.

~~~java
```java
class Animal{
    public String name;
    public int age;
    public void eat(){
        System.out.println("动物吃");
    }
}
class Dog extends Animal {
}

class Bird extends Animal{
    public void fly() {
        System.out.println("鸟飞");
    }
}
public class Test {
    public static void main(String[] args) {
        Dog  dog=new Dog();
        dog.eat();
        Bird bird=new Bird();
        bird.eat();
        bird.fly();
        System.out.println();
    }
}
输出结果为
动物吃
动物吃
鸟飞

~~~

但如果将Animal的name属性设置为private，那么在子类当中即使继承了也不能访问（会报错）

![在这里插入图片描述](https://img-blog.csdnimg.cn/20210112162723902.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQ1NjYxMTI1,size_16,color_FFFFFF,t_70)
![在这里插入图片描述](https://img-blog.csdnimg.cn/20210112162746753.png)

## protected 关键字

刚才我们发现, 如果把字段设为 private, 子类不能访问. 但是设成 public, 又违背了我们 **“封装”** 的初衷. 两全其美的办法就是 **protected** 关键字.（**protected就是用来解决不同包中的继承**）

- 对于类的**调用者**来说, protected 修饰的字段和方法是**不能访问的**
- 对于类的**子类(发生了继承）\**和 \*\*同一个包的其他类\*\*来说, protected 修饰的字段和方法是\**可以访问的**

下面结合代码来看一下，
-在**com.baidu.www**包定义的TestDemo类中的**val**的权限为**protected**
![在这里插入图片描述](https://img-blog.csdnimg.cn/20210112180036748.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQ1NjYxMTI1,size_16,color_FFFFFF,t_70)

- 它可以在**同一个包中的的不同类**中访问
  ![在这里插入图片描述](https://img-blog.csdnimg.cn/20210112180650996.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQ1NjYxMTI1,size_16,color_FFFFFF,t_70)
- 也可以在**不同包中的子类**访问（此时需要先继承父类后才使用**super**来访问（代表父类对象的引用））

![在这里插入图片描述](https://img-blog.csdnimg.cn/20210112180151948.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQ1NjYxMTI1,size_16,color_FFFFFF,t_70)

## super关键字

子类从父类中继承了**除构造方法外**的所有字段和属性。那么构造方法就需要super来解决了。

- super代表**父类对象的引用**，可以调用父类的**普通方法和属性**
- **子类继承父类时，子类构造的时候，需要先帮助父类构造，在子类的构造方法内部，显示调用父类的构造方法super（）（如果是无参构造则可以省略不写）**
- super（）必须放在子类构造方法的**第一行**
- super（）**不能在静态方法中使用它**（super代表引用，需要对象）

举例说明

```java
class Animal{
    public  String name;
    private int age;
    public Animal(){
        System.out.println(111);
    }
    public Animal(String name,int age){
        this.name=name;
        this.age=age;
      }
    public void eat(){
        System.out.println("动物吃");
    }
}
class Dog extends Animal {
    public Dog(){
        //super();
        //默认构造Animal的无参构造super（）可以省略
    }
    public Dog(String name,int age)
    {
        //显示调用有参构造
        super(name,age);
    }
}
class Bird extends Animal{
    //默认构造Animal的无参构造
        public void fly() {
        System.out.println("鸟飞");
    }
}
public class Test {
    public static void main(String[] args) {
        Animal animal=new Animal();
        Dog  dog=new Dog("旺财",16);
        System.out.println(dog.name);
        Bird bird=new Bird();
    }
}

```

## final关键字（密封类）

如果想从语法上进行限制继承, 就可以使用 **ﬁnal** 关键字

- 曾经我们学习过 ﬁnal **关键字**, 修饰一个**变量或者字段**的时候, 表示 **常量** (不能修改).

```java
final int a = 10;
 a = 20;	// 编译出错
12
```

- ﬁnal 关键字也能修饰**类**, 此时表示被修饰的类就**不能被继承**.

```java
final public class Animal {
...
}

public class Bird extends Animal {
...
}

// 编译出错
Error:java: 无法从最终com.bit.Animal进行继承

```

我们平时是用的 String 字符串类, 就是用 ﬁnal 修饰的, 不能被继承.

# 继承中代码的执行顺序

还是先执行父类在执行子类，**但静态代码块只执行一次**。

举例

```java
class Animal{
    public  String name;
    private int age;
    static {
        System.out.println("Animal::static{}静态代码块");
    }
    {
        System.out.println("Animal::{}实例代码块");
    }

    public Animal(){
        System.out.println("Animal()不带参数的构造方法");
    }
    public Animal(String name,int age){
        this.name=name;
        this.age=age;
        System.out.println("Animal(String，int)带参数的构造方法");
      }
    public void eat(){
        System.out.println("动物吃");
    }
}
class Dog extends Animal {

    static {
        System.out.println("Dog::static{}静态代码块");
    }
    {
        System.out.println("Dog::{}实例代码块");
    }
    public Dog(){
        System.out.println("Dog()不带参数的构造方法");
        //super();
        //默认构造Animal的无参构造super（）可以省略
    }
    public Dog(String name,int age)
    {
        //显示调用有参构造
        super(name,age);
        System.out.println("Dog(String，int)带参数的构造方法");
    }
}
class Bird extends Animal{
    static {
        System.out.println("Bird::static{}静态代码块");
    }
    {
        System.out.println("Bird::{}实例代码块");
    }

    //默认构造Animal的无参构造

    public Bird() {
        System.out.println("Bird()不带参数的构造方法");
    }

    public Bird(String name, int age) {
        super(name, age);
        System.out.println("Bird(String，int)带参数的构造方法");
    }

    public void fly() {
        System.out.println("鸟飞");
    }
}
public class Test {
    public static void main(String[] args) {

        Dog  dog=new Dog();
        System.out.println("________________");
        Bird bird=new Bird();
        System.out.println("________________");
    }
}

```

输出结果为
![在这里插入图片描述](https://img-blog.csdnimg.cn/20210113141850476.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQ1NjYxMTI1,size_16,color_FFFFFF,t_70)

# 多层继承

刚才我们的例子中, 只涉及到 Animal, Dog 和 Bird 三种类. 但是如果情况更复杂一些呢?
![在这里插入图片描述](https://img-blog.csdnimg.cn/20210112183308455.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQ1NjYxMTI1,size_16,color_FFFFFF,t_70)
如上图针对 Cat 这种情况, 我们可能还需要表示更多种类的猫，这个时候使用继承方式来表示,我们成为**多层继承** 就会变得非常复杂。但我们并不希望类之间的继承层次太复杂. 一般我们不希望出现超过**三层**的**继承关系**. 如果继承层次太多, 就需要考虑对代码进行重构了.

# 组合

和继承类似, 组合也是一种表达类之间关系的方式, 也是能够达到代码重用的效果.
例如表示一个学校:

```java
public class Student {
...
}

public class Teacher {
...
}

public class School {
public Student[] students;
public Teacher[] teachers;
}

```

组合没有涉及到特殊的语法(诸如 **extends** 这样的关键字), **仅仅是将一个类的实例作为另外一个类的字段.** 这是我们设计类的一种常用方式之一.

- 组合表示 has - a 语义在刚才的例子中, 我们可以理解成一个学校中 “包含” 若干学生和教师.
- 继承表示 is - a 语义在上面的 “动物和猫” 的例子中, 我们可以理解成一只猫也 “是” 一种动物.

大家要注意体会两种语义的区别.

# Java 中对于字段和方法共有四种访问权限小结

- private: 类内部能访问, 类外部不能访问
- 默认(也叫包访问权限): 类内部能访问, 同一个包中的类可以访问, 其他类不能访问.
- protected: 类内部能访问, 子类和同一个包中的类可以访问, 其他类不能访问.
- public : 类内部和类的调用者都能访问

![在这里插入图片描述](https://img-blog.csdnimg.cn/20210112175015881.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQ1NjYxMTI1,size_16,color_FFFFFF,t_70)
**什么时候下用哪一种呢?**
我们希望类要尽量做到 “**封装**”, 即隐藏内部实现细节, 只暴露出 **必要** 的信息给类的调用者.因此我们在使用的时候应该尽可能的使用 比较严格 的访问权限. 例如如果一个方法能用 private, 就尽量不要用public.**我们写代码的时候认真思考, 该类提供的字段方法到底给 “谁” 使用(是类内部自己用, 还是类的调用者使用, 还是子类使用).**