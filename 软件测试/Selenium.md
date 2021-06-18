@[TOC](selenium)
# 什么是自动化测试
自动化测试指软件测试的自动化，在预设状态下运行应用程序或者系统，预设条件包括正常和异常，最后评估运行结果。将人为驱动的测试行为转化为机器执行的过程。
# 自动化测试的适用对象
实施自动化测试的前提条件：**需求变动不频繁、项目周期足够长、自动化测试脚本可重复使用**

 - 1需求变动频繁的项目，自动化脚本不能重复使用，维护成本太大，性价比低
 - 2项目周期短，自动化脚本编制完成后使用次数不多，性价比低
 - 3交互型较强的项目，需要人工干预的项目，自动化无法实施
# 自动化测试的分类
 - **UI自动化**
项目比较稳定，界面要稳定，在项目后期做UI自动化测试、用例维护量大
 - **接口自动化**
项目前期就可以介入
测试用例维护量较少
接口稳定
 - **性能自动化**

# 如何实施自动化测试
 - **分析**：总体把握系统逻辑，分析出系统的核心体系架构。
 - **设计**：设计测试用例，测试用例要足够明确和清晰，覆盖面广而精
 - **实现**：实现脚本，有两个要求一是断言，二是合理的运用参数化。
 - **执行**：执行脚本远远没有我们想象中那么简单。脚本执行过程中的异常需要我们仔细的去分析原因。
 - **总结**：测试结果的分析，和测试过程的总结是自动化测试的关键。
 - **维护**：自动化测试脚本的维护是一个难以解决但又必须要解决的问题。
 - **分析**：在自动化测试过程中深刻的分析自动化用例的覆盖风险和脚本维护的成本
 
# 什么是selenium
Selenium是ThroughtWorks公司一个强大的**开源Web功能测试工具系列**，支持多平台、多浏览器、多语言去实现自动化测试，Selenium2将浏览器原生的API封装成WebDriver API，可以直接操作浏览器页面里的元素，甚至操作浏览器本身（截屏，窗口大小，启动，关闭，安装插件，配置证书之类的）,所以就像真正的用户在操作一样。

<code>selenium是工具集，包括selenium1.0和selenium2.0</code>
Selenium已经从之前的1.0(RC)进化到了现在Selenium2(Selenium1+WebDriver)。

## Selenium1.0
Selenium1.0包括Selenium IDE（自动化脚本录制工具） Selenium GRID （分布式测试） Selenium RC

 Selenium RC包括  Selenium Service 和Client Libraries
 ![在这里插入图片描述](https://img-blog.csdnimg.cn/20210617230000496.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQ1NjYxMTI1,size_16,color_FFFFFF,t_70)
 Selenium RC工作流程
 ![在这里插入图片描述](https://img-blog.csdnimg.cn/20210617230154437.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQ1NjYxMTI1,size_16,color_FFFFFF,t_70)

 ## Seleniu2.0
Seleniu2.0是在Seleniu1.0的基础上加了个webdriver（浏览器驱动，根据不同的浏览器定制）绕过了JavaScript环境沙箱问题

webdriver原理![在这里插入图片描述](https://img-blog.csdnimg.cn/2021061723050549.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQ1NjYxMTI1,size_16,color_FFFFFF,t_70)
![在这里插入图片描述](https://img-blog.csdnimg.cn/2021061723054857.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQ1NjYxMTI1,size_16,color_FFFFFF,t_70)
# webdriverAPI
一个简单脚本：

```cpp
# coding = utf-8
from selenium import webdriver 
import time

driver = webdriver.Chrome() (浏览器第一个字母一定要大写)
time.sleep(3) 
driver.get("http://www.baidu.com") time.sleep(3)
driver.find_element_by_id("kw").send_keys("selenium") 
time.sleep(3)
driver.find_element_by_id("su").click()
driver.quit()
```

脚本解析

 - coding = utf-8

可加可不加，开发人员喜欢加一下，防止乱码。

 - from selenium import webdriver

要想使用selenium 的webdriver 里的函数，首先把包导进来

 - driver = webdriver.Chrome()

我们需要操控哪个浏览器呢？Chrome ，当然也可以换成Ie 或Firefox。driver 可以随便取，但后面要用它操纵各种函数执行。

 - driver .ﬁnd_element_by_id("kw").send_keys("selenium")

一个控件有若干属性id 、name、（也可以用其它方式定位），百度输入框的id叫kw ，我要在输入框里输入selenium 。

 - driver .ﬁnd_element_by_id("su").click()

搜索的按钮的id 叫su,我需要点一下按钮（ click() ）。

 - driver .quit()

退出并关闭窗口的每一个相关的驱动程序。

 - driver .close()

关闭当前窗口。close方法关闭当前的浏览器窗口，quit方法不仅关闭窗口，还会彻底的退出webdriver，释放与driver  server之间的连接。所以简单来说quit是更加彻底的close，quit会更好的释放资源(建议使用quit())
## 元素的定位
对象的定位应该是自动化测试的核心，要想操作一个对象，首先应该识别这个对象。一个对象就是一个人一样，他 会有各种的特征（属性），如比我们可以通过一个人的身份证号,姓名，或者他住在哪个街道、楼层、门牌找到这 个人。

那么一个对象也有类似的属性，我们可以通过这个属性找到这对象。**注意：不管用那种方式，必须保证页面上该属性的唯一性**

webdriver 提供了一系列的对象定位方法，常用的有以下几种

 - id  （常用如果有id那么一定唯一）
 - name 
 
id 和name 是我们最最常用的定位方式，因为大多数控件都有这两个属性，而且在对控件的id 和name 命名时一般使其有意义也会取不同的名字。通过这两个属性使我们找一个页面上的属性变得相当容易。
 - class name  
 - link text (有时候不是一个输入框也不是一个按钮，而是一个文字链接，我们可以通过link text来定位） 
 - link text partial（通过部分链接定位，这个有时候也会用到）
 - tag name  
 - xpath (可以唯一确定一个元素)
 - css  selector

```cpp
#coding=utf-8
from selenium import webdriver import time
driver = webdriver.Chrome()
driver.get("http://www.baidu.com") #########百度输入框的定位方式########## 
#通过id 方式定位
driver.find_element_by_id("kw").send_keys("selenium") 
#通过name 方式定位
driver.find_element_by_name("wd").send_keys("selenium") 
#通过tag name 方式定位
driver.find_element_by_tag_name("input").send_keys("selenium") 不能成功，因为input太多了不唯一。
#通过class name 方式定位
driver.find_element_by_class_name("s_ipt").send_keys("selenium")  
#通过CSS 方式定位driver.find_element_by_css_selector("#kw").send_keys("selenium")

#通过xphan 方式定位
driver.find_element_by_xpath("//*[@id='kw']").send_keys("selenium") ############################################
driver.find_element_by_id("su").click() time.sleep(3)
driver.quit()
```

## 操作测试对象
前面讲到了不少知识都是定位元素，定位只是第一步，定位之后需要对这个原素进行操作。鼠标点击呢还是键盘输  入，这要取决于我们定位的是按钮还输入框。
一般来说，webdriver 中比较常用的操作对象的方法有下面几个：

 - **click** 点击对象
 - **send_keys** 在对象上模拟按键输入
 - **clear** 清除对象的内容，如果可以的话
 - **submit** 清除对象的内容，如果可以的话
 - **text** 用于获取元素的文本信息

## 添加等待
定时等待
我们需要引入time 包，就可以在脚本中自由的添加休眠时间了

```cpp
import time 
time.sleep(3)
```
智能等待
通过添加**implicitly_wait()**  方法就可以方便的实现智能等待；implicitly_wait(30)的用法应该比time.sleep()   更智能，前者等到则直接继续向下执行，后者则必须等满这个时间
## 打印信息

```cpp
print(driver.title)
print(driver.current_url)
```
## 浏览器的操作

 - 浏览器最大化

```cpp
driver.maximize_window() #将浏览器最大化显示
```

 - 设置浏览器宽、高

```cpp
driver.set_window_size(480, 800)
```

 - 操作浏览器的前进、后退

```cpp
driver.back()
driver.forward()
```

 - 控制浏览器滚动条

```cpp
#将页面滚动条拖到底部
js="var q = document.documentElement.scrollTop=10000" driver.execute_script(js)
time.sleep(3)
#将滚动条移动到页面的顶部
js="var q = document.documentElement.scrollTop=0" driver.execute_script(js)
```
## 键盘事件

 - 键盘按键用法

```python
 #需要引入keys 包
from selenium.webdriver.common.keys import Keys
import os,time

#tab 的定位相当于清除了密码框的默认提示信息，等同上面的clear()
driver.find_element_by_id("account").send_keys(Keys.TAB) time.sleep(3)
#通过定位密码框，enter（回车）来代替登陆按钮
driver.find_element_by_name("password").send_keys(Keys.ENTER) '''
#也可定位登陆按钮，通过enter（回车）代替click()
driver.find_element_by_id("login").send_keys(Keys.ENTER) 
```
通过send_keys()调用按键： send_keys(Keys.TAB) # TAB send_keys(Keys.ENTER) # 回 车

 - 键盘组合键用法

```python
#输入框输入内容
driver.find_element_by_id("kw").send_keys("selenium") 
time.sleep(3)
#ctrl+a 全选输入框内容
driver.find_element_by_id("kw").send_keys(Keys.CONTROL,'a') 
time.sleep(3)
#ctrl+x 剪切输入框内容
driver.find_element_by_id("kw").send_keys(Keys.CONTROL,'x') 
```
## 键盘事件
ActionChains 类

 - context_click() 右击
 - double_click() 双击
 - drag_and_drop() 拖动
 - move_to_element() 移动

```python
ActionChains(driver).context_click(qqq).perform() #右键
ActionChains(driver).double_click(qqq).perform() #双击

#定位元素的原位置
element = driver.find_element_by_id("s_btn_wr")
 #定位元素要移动到的目标位置
target = driver.find_element_by_class_name("btn") 
#执行元素的移动操作
ActionChains(driver).drag_and_drop(element, target).perform()
```
**ActionChains(driver)**
生成用户的行为。所有的行动都存储在actionchains 对象。通过perform()存储的行为。
**move_to_element(menu)**
移动鼠标到一个元素中，menu 上面已经定义了他所指向的哪一个元素
**perform()**
执行所有存储的行为
## 定位一组元素
webdriver 可以很方便的使用ﬁndElement 方法来定位某个特定的对象，不过有时候我们却需要定位一组对象，这时候就需要使用ﬁndElements 方法。

定位一组对象一般用于以下场景：

 - 批量操作对象，比如将页面上所有的checkbox 都勾上
 - 先获取一组对象，再在这组对象中过滤出需要具体定位的一些对象。比如定位出页面上所有的checkbox，然后选择最后一个

![在这里插入图片描述](https://img-blog.csdnimg.cn/20210617234645960.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQ1NjYxMTI1,size_16,color_FFFFFF,t_70)


```python
#coding=utf-8
from selenium import webdriver import time
import os
driver= webdriver.Chrome()

file_path = 'file:///' + os.path.abspath('checkbox.html') 
driver.get(file_path)

# 选择页面上所有的input，然后从中过滤出所有的checkbox 并勾选之

inputs = driver.find_elements_by_tag_name('input') 
for input in inputs:
	if input.get_attribute('type') == 'checkbox': 
		input.click()
time.sleep(2) 
driver.quit()
```

## 多层框架/窗口定位
多层框架或窗口的定位：

 - switch_to_frame()
 - switch_to_window()

有时候我们定位一个元素，定位器没有问题，但一直定位不了，这时候就要检查这个元素是否在一个frame 中，seelnium webdriver 提供了一个switch_to_frame 方法，可以很轻松的来解决这个问题。

```python
switch_to_frame(name_or_id_or_frame_element)：
```

```python
从frame中嵌入的页面里跳出，跳回到最外面的原始页面中。
switch_to_default_content：
```
![在这里插入图片描述](https://img-blog.csdnimg.cn/20210617235118445.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQ1NjYxMTI1,size_16,color_FFFFFF,t_70)

```python
#先找到到ifrome1（id = f1）
driver.switch_to_frame("f1")
##再找到其下面的ifrome2(id =f2) 
driver.switch_to_frame("f2") 
#下面就可以正常的操作元素了
driver.find_element_by_id("kw").send_keys("selenium") driver.find_element_by_id("su").click()
```

## 下拉框处理

下拉框是我们最常见的一种页面元素，对于一般的元素，我们只需要一次就定位，但下拉框里的内容需要进行两次  定位，先定位到下拉框，再定位到下拉框内里的选项。
![在这里插入图片描述](https://img-blog.csdnimg.cn/20210617235348411.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQ1NjYxMTI1,size_16,color_FFFFFF,t_70)

```python
#先定位到下拉框
m = driver.find_element_by_id("ShippingMethod") 
#再点击下拉框下的选项
m.find_element_by_xpath("//option[@value='10.69']").click() 
```
这里可能和之前的操作有所不同，首先要定位到下拉框的元素，然后选择下拉列表中的选项进行点击操作。
## alert、conﬁrm、prompt 的处理

 - text 返回alert/conﬁrm/prompt 中的文字信息
 - accept 点击确认按钮
 - dismiss 点击取消按钮，如果有的话
 - send_keys 输入值，这个alert\conﬁrm 没有对话框就不能用了，不然会报错

注**意：switch_to_alert()只能处理原生的alert** 

```python
# 点 击 “ 请 点 击 ” 
driver.find_element_by_xpath("html/body/input").click()  
#输入内容
driver.switch_to_alert().send_keys('webdriver') 
driver.switch_to_alert().accept()
```
## DIV对话框的处理
更多的时候我们在实际的应用中碰到的并不是简单警告框，而是提供更多功能的会话框。

![在这里插入图片描述](https://img-blog.csdnimg.cn/20210617235813293.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQ1NjYxMTI1,size_16,color_FFFFFF,t_70)

```python
# 打开对话框
driver.find_element_by_id('show_modal').click() 
sleep(3)
# 点击对话框中的链接
link=driver.find_element_by_id('myModal').find_element_by_id('click') link.click()
#dr.execute_script('$(arguments[0]).click()', link) sleep(4)
# 关闭对话框
buttons = dr.find_element_by_class_name('modal-footer').find_elements_by_tag_name('button') buttons[0].click()
```
## 上传文件操作
文件上传操作也比较常见功能之一，上传过程一般要**打开一个本地窗口，从窗口选择本地文件添加**。所以，一般会卡在如何操作本地窗口添加上传文件。其实，在selenium webdriver 没我们想的那么复杂；只要定位上传按钮，通过send_keys  添加本地文件路径就可以了。绝对路径和相对路径都可以，关键是上传的文件存在。

```python
#定位上传按钮，添加本地文件
driver.find_element_by_name("file").send_keys('D:\\PycharmProjects\\test\\upload.txt') 
```
