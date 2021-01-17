在了解多态之前我们需要先了解一些相关的知识：向上转型，运行时绑定。
# 向上转型
## 什么是向上转型？
**向上转型**：通俗点来说就**父类引用**“**引用**“”**子类对象**（我是这样理解的：因为是把子类给父类，把小给大，所以是向上层转变呢）
**注意**：向上转型后，父类只能访问自己的属性和方法，而不能访问子类特有的属性字段和方法。
**举例**：

```java
class Animal{
    public  String name;
    private int age;
    public Animal(){
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
    public  int leg;
    public Dog(){
    }
    public Dog(String name,int age)
    {
        super(name,age);
    }
    public void wangwang(){
        System.out.println("汪汪叫！");
    }
}
public class Test{
    public static void main(String[] args) {
        Dog dog=new Dog();
        dog.wangwang();//可以正常访问
        Animal animal=new Dog();//父类引用引用子类对象（发生了向上转型）
        animal.name="dsda";//可以正常访问
        animal.leg=4;//error 报错（leg为Dog类自己特有的属性）
        animal.wangwang();//error 报错（wangwang为Dog类自己特有的方法）

    }
}
```
## 什么时候发生向上转型？

 - 直接赋值
```java
 Animal animal=new Dog();
```
 - 方法传参

```java
 public static void func(Animal animal){
        System.out.println("传参发生了向上转型");
    }

 func(new Dog());
```

 - 方法返回值

```java
public static Animal func1(){
        return new Dog();
    }
 Animal animal2=func1();
```

# 向下转型
向下转型：就是将**子类对象** **引用** **父类对象**<u>（但不安全，我们一般不使用）</u>
例如下面的代码，并不是所有的动物都会飞。如果强行使用的话需要加上**instanceof**关键字，否则会报**类型转换**的错误。
```java
public class Test {
    public static void main(String[] args) {
        Animal animal1 = new Animal();
        Bird bird = (Bird) animal1;
        bird.fly();
         /* if (animal1 instanceof Bird) {
            Bird bird = (Bird) animal1;
            bird.fly();
        }*/
    }
}
error：ClassCastException: Animal cannot be cast to Bird
```
![在这里插入图片描述](https://img-blog.csdnimg.cn/20210113162605122.png)

#运行时绑定（动态绑定）

当子类和父类中出现同名方法的时候, 再去调用会出现什么情况呢?
对前面的代码稍加修改, 给 Dog 类也加上同名的 eat 方法, 并且在两个 eat 加以区分。


```java
class Animal{
    public  String name;
    private int age;
    public Animal(){
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
    public  int leg;
    public Dog(){
        //super();
        //默认构造Animal的无参构造super（）可以省略
    }
    public Dog(String name,int age)
    {
        //显示调用有参构造
        super(name,age);
    }
    public void eat(){
        System.out.println("狗吃");
    }
    public void wangwang(){
        System.out.println("汪汪叫！");
    }
}

public class Test{
    public static void main(String[] args) {
        Animal animal1=new Dog();
        Animal animal2=new Animal();
        animal1.eat();
        animal2.eat();
    }
}
运行结果为
狗吃
动物吃
```
此时, 我们发现:
animal1 和 animal2 虽然都是 Animal 类型的引用, 但是animal1 指向Dog 类型的实例. animal2 指向 Animal 类型的实例, 针对 animal1 和 animal2 分别调用 eat 方法, 发现animal1.eat() 实际调用了子类的方法.而 animal2.eat() 实际调用了父类的方法, 
因此, 在 Java 中, 调用某个类的方法, 究竟执行了哪段代码 (是父类方法的代码还是子类方法的代码) , 要看究竟这个引用指向的是父类对象还是子类对象. 这个过程是程序运行时决定的(而不是编译期), 因此称为 动态绑定.我们可以看一下编译的代码，发现都是Animal的eat，所以说明是在**运行时绑定**的。
![在这里插入图片描述](https://img-blog.csdnimg.cn/20210113181715821.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQ1NjYxMTI1,size_16,color_FFFFFF,t_70)

# 重写（覆盖、重载）
针对刚才的eat方法来说：子类实现父类的同名方法，并且参数的类型和个数完全相同，这种情况称为**重写、覆盖、覆写。**
## 注意事项


 - **重写**和**重载**完全不一样，**不要混淆**
 - 普通方法可以重写，**static**修饰的静态方法**不能重写**
 - 重写中子类的方法的访问权限**大于**父类的访问权限（**public可以相同**）
 - 重写的方法返回值不一定和父类的方法相同（但建议写成相同的，不同时子类和父类的返回值要构成**继承关系**这种称为**协同类型**）

 ## @Override

 -  针对重写的方法, 可以使用 **@Override** 注解来**显式指定**.有了这个注解能帮我们进行一些合法性校验. 例如不小心将方法名字拼写错了 (比如写成 aet), 那么此时编译器就会发现父类中没有 aet 方法, 就会编译报错, 提示**无法构成重写.**
 - 我们推荐在代码中进行重写方法时显式加上 @Override 注解. 
```java
class Bird extends Animal { 
@Override
private void eat(String food)
  {
  }
}

```
 ## 在构造方法中调用重写方法的（一个坑）
 来看下面一段代码


```java
class B {
    public B() {
       func();
    }
    public void func() {
        System.out.println("B.func()");
    }
}
class D extends B {
    private int num = 1;
    @Override
    public void func() {
        System.out.println("D.func() " + num);
    }
}
public class Test {
    public static void main(String[] args) {
        B b = new D();
    }
}
输出结果为 
D:func 0
```
为什么会这样呢，我们来分析一下

 - 构造 D 对象的同时, 会调用 B 的构造方法.
 - **B 的构造方法中**调用了 **func** 方法, 此时会触发**动态绑定**, 会调用到 **D 中的 func**
 - 此时 D 对象自身还没有构造, 此时 num 处在未初始化的状态, 值为 0.

结论:  尽量不要在构造器中调用方法(如果这个方法被子类重写, 就会触发动态绑定, 但是此时子类对象还没构造完成), 可能会出现一些隐藏的但是又极难发现的问题.


# 多态
## 多态的含义
通俗点来说：**多态**就是**同一个父类引用**可以**引用不同的子类对象**，可以调用一个**同名**的方法，而产生**不同的行为**（多态是一种思想）
## 举例
理解了**向上转型、方法重写和运行时绑定**之后我们来看看多态，我们用一段代码来理解。

```java
//每一个class文件单独创建一个class类
public class Shape {
    public void draw(){
        System.out.println("什么都不干");
    }
}

public class Circle extends Shape {
    @Override
    public void draw() {
        System.out.println("●");
    }
}

public class Rect extends Shape {
    @Override
    public  void draw(){
        System.out.println("♦");
    }
}
public class FLower extends Shape{
}

/////////////////////////////我是分割线//////////////////////

// Test.java
public class Test {
    public static void drawMap(Shape shape){
        shape.draw();
    }
    public static void main(String[] args) {
        Shape shape=new Shape();
        Rect rect=new Rect();
        Circle circle=new Circle();
        FLower flower=new FLower();
        drawMap(shape);
        drawMap(rect);
        drawMap(circle);
        drawMap(flower);
    }
}

```
运行结果：
![在这里插入图片描述](https://img-blog.csdnimg.cn/20210117151326468.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQ1NjYxMTI1,size_16,color_FFFFFF,t_70)

 - 这段代码子类Circle和Rect分别**重写**了父类的**draw**方法，在用方法传参时（drawMap）发生了**向上转型**，然后父类引用（shape）分别前后引用了circle和rect，此时在调用draw时便会调用相应**子类中重写的draw**，而Flow虽然继承了Shape但没有重写其draw方法，所以调用的还是其父类Shape的draw方法。
 - 在这个代码中, 分割线上方的代码是 **类的实现者** 编写的, 分割线下方的代码是 **类的调用者** 编写的.当类的调用者在编写 drawMap 这个方法的时候, 参数类型为 Shape (父类), 此时在该方法内部并不知道, 也不关注当前的 shape 引用指向的是哪个类型(哪个子类)的实例. 此时 shape 这个引用调用 draw 方法可能会有**多种不同的表现(**和 shape 对应的实例相关rect或circle), 这种行为就称为 多态.



## 多态的好处

 1. 类调用者对**类的使用成本降低**（多态可以让类的调用者连这个类的类型都不必知道是什么，只需要知道这个对象有某个方法即可）
 2. 能都**降低**代码的“**圈复杂度**”，避免大量的使用if-else
如果我们打印的不是一个形状而是多个的话，如果不基于多态的话，代码如下

```java
public static void drawShapes() { 
    Rect rect = new Rect();
    Cycle cycle = new Cycle(); 
    Flower flower = new Flower();
    String[] shapes = {"cycle", "rect", "cycle", "rect", "flower"};
        for (String shape : shapes)
        {
            if (shape.equals("cycle")) 
            { 
                cycle.draw();
            } 
            else if (shape.equals("rect")) 
            { 
                rect.draw();
            } 
            else if (shape.equals("flower")) 
            { 
                flower.draw();
            }
        }
} 
```
而使用多态的话便会简洁许多

```java
public static void drawShapes() {
// 我们创建了一个 Shape 对象的数组.
        Shape[] shapes = {new Cycle(), new Rect(), new Cycle(),new Rect(), new Flower()};
       for(Shape shape:shapes)
        {
            shape.draw();
        }
}
```
圈复杂度是一种描述一段代码复杂程度的方式. 一段代码如果平铺直叙, 那么就比较简单容易理解. 而如果有很多的条件分支或者循环语句, 就认为理解起来更复杂.因此我们可以简单粗暴的计算一段代码中**条件语句**和**循环语句**出现的**个数**, 这个个数就称为 "圈复杂度". 如果一个方法的圈复杂度太高, 就需要考虑重构.

 **3. 可扩展性强**
 如果要新增一种新的形状，使用多态的方式代码改动的成本低。（比如新增一个画三角形的方法）

```java
class Triangle extends Shape { @Override
public void draw() { 
    System.out.println("△");
   }
}

```
# 总结
多态是**面向对象程序设计**中比较难理解的部分. 多态通常配合**抽象类、接口、继承**使用，我们需要加深理解才能熟练使用。