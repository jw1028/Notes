@[TOC](这里写目录标题)
之前讲解了selenium的脚本录制和api。在进行脚本录制导出的脚本中，我们发现其中多了很多代码，这些代码正    是unittest测试框架。
# unittest框架解析
unittest 是python 的单元测试框架， unittest 单元测试提供了创建测试用例，测试套件以及批量执行的方案， unittest 在安装pyhton 以后就直接自带了，直接import unittest 就可以使用。
作为单元测试的框架，  **unittest 也是可以对程序最小模块的一种敏捷化的测试**。在自动化测试中，我们虽然不需要做白盒测试，但是必须需要知道所使用语言的单元测试框架。利用单元测试框架，创建一个类，该类继承unittest 的TestCase，这样可以把每个case看成是一个最小的单元，由测试容器组织起来，到时候直接执行，同时引入测试报告。

unittest 各组件的关系为：
![在这里插入图片描述](https://img-blog.csdnimg.cn/20210620093137882.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQ1NjYxMTI1,size_16,color_FFFFFF,t_70)

 - **test ﬁxture**：初始化和清理测试环境，比如创建临时的数据库，文件和目录等，其中 setUp() 和 setDown()是最常用的方法
 - **test case**：单元测试用例，TestCase 是编写单元测试用例最常用的类
 - **<code>test suite**：单元测试用例的集合，TestSuite 是最常用的类
 - **test runne**r：执行单元测试
 - **test report**：生成测试报告

```python
   author = 'sunraylily' # -*-
   		 coding: utf-8 -*-
        from selenium import webdriver
        from selenium.webdriver.common.by import By 
        from selenium.webdriver.common.keys import Keys
        from selenium.webdriver.support.ui import Select
        from selenium.common.exceptions import NoSuchElementException 
        from selenium.common.exceptions import NoAlertPresentException import unittest, time, re

        class Baidu1(unittest.TestCase):

        def setUp(self):
        self.driver = webdriver.Firefox() self.driver.implicitly_wait(30) self.base_url = "http://www.baidu.com/" self.verificationErrors = [] self.accept_next_alert = True
        def test_baidusearch(self): driver = self.driver
        driver.get(self.base_url + "/") driver.find_element_by_id("kw").click()
        driver.find_element_by_id("kw").clear()
       driver.find_element_by_id("kw").send_keys(u"测试") driver.find_element_by_id("su").click()
        def test_hao(self): driver = self.driver
        driver.get(self.base_url + "/")
        driver.find_element_by_link_text("hao123").click() self.assertEqual(u"hao123_上网从这里开始", driver.title)

        def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what) except NoSuchElementException as e: return False return True
#判断alert是否存在，可删除
        def is_alert_present(self):
        try: self.driver.switch_to_alert()
        except NoAlertPresentException as e: return False return True

        def close_alert_and_get_its_text(self): try:
        alert = self.driver.switch_to_alert() alert_text = alert.text
        if self.accept_next_alert: alert.accept()
else:
        alert.dismiss() return alert_text
finally: self.accept_next_alert = True #test fixture，清除环境
        def tearDown(self): self.driver.quit()
        self.assertEqual([], self.verificationErrors) if name == " main ":
        unittest.main()

        '''
        可以增加verbosity参数，例如unittest.main(verbosity=2)
        在主函数中，直接调用main() ，在main中加入verbosity=2 ，这样测试的结果就会显示的更加详细。这里的verbosity 是一个选项, 表示测试结果的信息复杂度，有三个值:
        0( 静默模式): 你只能获得总的测试用例数和总的结果比如总共100个失败,20 成功80
        1( 默认模式): 非常类似静默模式只是在每个成功的用例前面有个“ . ” 每个失败的用例前面有个“F”
        2( 详细模式): 测试结果会显示每个测试用例的所有相关的信息
```

# 批量执行脚本
## 构建测试套件
完整的单元测试很少只执行一个测试用例，开发人员通常都需要编写多个测试用例才能对某一软件功能进行比较完 整的测试，这些相关的测试用例称为一个测试用例集，在unittest中是用TestSuite 类来表示的。
## addTest（） 的应用
当有多个或者几百测试用例的时候，这样就需要一个测试容器( 测试套件) ，把测试用例放在该容器中进行执行， unittest  模块中提供了TestSuite  类来生成测试套件，使用该类的构造函数可以生成一个测试套件的实例，该类提供了addTest来把每个测试用例加入到测试套件中。

```python
def createSuite():
    suite = unittest.TestSuite()
    suite.addTest(test001.testCase1("test_baidu1"))
    suite.addTest(test001.testCase1("test_baidu2"))
    suite.addTest(test002.testCase2("test_baidu1"))
    suite.addTest(test002.testCase2("test_baidu2"))
if __name__=="__main__":
```

上述做法有两个不方便的地方，阻碍脚本的快速执行，必须每次修改runall.py：     

 - 1）需要导入所有的py文件，比如import testbaidu1，每新增一个需要导入一个
 - 2）addTest需要增加所有的testcase，如果一个py文件中有10个case，就需要增加10次

## makeSuite（）和TestLoader()的应用
在unittest  框架中提供了makeSuite()  的方法，**makeSuite可以实现把测试用例类内所有的测试case组成的测试套件TestSuite** ，unittest 调用makeSuite的时候，只需要把测试类名称传入即可。
TestLoader  用于创建类和模块的测试套件，一般的情况下，使TestLoader().loadTestsFromTestCase(TestClass) 来加载测试类。

```python
def createSuite():
    suite = unittest.TestSuite()
    suite.addTest(test001.testCase1("test_baidu1"))
    suite.addTest(test001.testCase1("test_baidu2"))
    suite.addTest(test002.testCase2("test_baidu1"))
    suite.addTest(test002.testCase2("test_baidu2"))
    # makeSuite
    suite.addTest(unittest.makeSuite(test001.testCase1))
    suite.addTest(unittest.makeSuite(test002.testCase2))
    return suite
    # TestLoader
    suite1 = unittest.TestLoader.loadTestsFromTestCase(test001.testCase1)
    suite2 = unittest.TestLoader.loadTestsFromTestCase(test002.testCase2)
    suite.addTest([suite1, suite2])
    return suite
if __name__=="__main__":
```

经过makeSuite（）和TestLoader（）的引入，我们不用一个py文件测试类，只需要导入一次即可。    那么能不能测试类也不用每次添加指定呢？
## discover（）的应用
discover 是通过递归的方式到其子目录中从指定的目录开始， 找到所有测试模块并返回一个包含它们对象的TestSuite ，然后进行加载与模式匹配唯一的测试文件，discover 参数分别为discover(dir,pattern,top_level_dir=None)

```python
def createSuite():
  
    discover = unittest.defaultTestLoader.discover('../src202105', pattern='test00*.py', top_level_dir=None)
    print(discover)
    return discover
if __name__=="__main__":
```

# 用例的执行顺序
unittest 框架默认加载测试用例的顺序是根据ASCII 码的顺序，数字与字母的顺序为： 0-9,A-Z，a-z
所以， TestAdd 类会优先于TestBdd 类被发现， test_aaa() 方法会优先于test_ccc() 被执行。对于测试目录与测试文件来说， unittest 框架同样是按照这个规则来加载测试用例。
而addTest（）方法按照增加顺序来执行。
# 忽略用例执行

```python
@unittest.skip("skipping")
```

# unittest断言
自动化的测试中， 对于每个单独的case来说，一个case的执行结果中， 必然会有期望结果与实际结果， 来判断该case是通过还是失败，在unittest  的库中提供了大量的实用方法来检查预期值与实际值，  来验证case的结果，  一般来说， 检查条件大体分为等价性， 逻辑比较以及其他， 如果给定的断言通过， 测试会继续执行到下一行的代码， 如果断言失败， 对应的case测试会立即停止或者生成错误信息( 一般打印错误信息即可) ，但是不要影响其他的case

```python
    def test_1baidu1(self):
        driver=self.driver
        url=self.url
        driver.get(url)
        driver.find_element_by_id("kw").send_keys("小樽")
        driver.find_element_by_id("su").click()
        time.sleep(6)
        print(driver.title)
        self.assertNotEqual(driver.title, "百度搜索", msg="not equal!")
        self.assertTrue(1 == 2, msg="not equal!")
```

unittest 的单元测试库提供了标准的xUnit 断言方法。下面是一些常用的断言
![在这里插入图片描述](https://img-blog.csdnimg.cn/20210620095814850.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQ1NjYxMTI1,size_16,color_FFFFFF,t_70)

# HTML报告生成
脚本执行完毕之后，还需要看到HTML报告，下面我们就通过HTMLTestRunner.py 来生成测试报告。

```python
def createSuite():
    discover = unittest.defaultTestLoader.discover('../src202105', pattern='test00*.py', top_level_dir=None)

    print(discover)
    return discover

if __name__=="__main__":
    #获取当前文件所在的文件路径
    curpath = sys.path[0]
    print(curpath)
    if not os.path.exists(curpath+"/resultReport"):
        os.makedirs(curpath+"/resultReport")
    now = time.strftime("%Y-%m-%d-%H %M %S", time.localtime(time.time()))
    filename = curpath+"/resultReport/"+now+"-"+"resultReport.html"
    with open(filename, 'wb') as fp:
        runner = HTMLTestRunner.HTMLTestRunner(stream=fp, title=u"测试报告",
                                               description=u"测试用例执行的结果", verbosity=2)
        suite = createSuite()
        runner.run(suite)
```

# 异常捕捉与错误截图
用例不可能每一次运行都成功，肯定运行时候有不成功的时候。如果可以捕捉到错误，并且把错误截图保存，这将  是一个非常棒的功能，也会给我们错误定位带来方便。

例如编写一个函数，关键语句为save_error_image

```python
    def test_baidu(self):
        driver = self.driver
        self.driver.get(self.url)
        #判断到底有没有打开百度页面
        try:
            self.assertEqual(driver.title, "百度，你就知道", msg="判断失败，没有打开百度搜索页面")
        except:
            self.save_error_image(driver, "baidu.png")
        time.sleep(6)

    def save_error_image(self, driver, name):
        if not os.path.exists("./errorImage"):
            os.makedirs("./errorImage")
        now = time.strftime("%Y%m%d-%H%M%S", time.localtime(time.time()))
        driver.get_screenshot_as_file('./errorImage/'+now+"-"+name)
```

# 数据驱动
之前我们的case都是数据和代码在一起编写。考虑如下场景：

需要多次执行一个案例，比如baidu搜索，分别输入中文、英文、数字等进行搜索，这时候需要编写3个案例吗？有没有版本一次运行？

python的unittest 没有自带数据驱动功能。所以如果使用unittest，同时又想使用数据驱动，那么就可以使用DDT 来完成。

 - dd.ddt：

装饰类，也就是继承自TestCase的类。

 - ddt.data：

装饰测试方法。参数是一系列的值。

 - ddt.ﬁle_data：

装饰测试方法。参数是文件名。文件可以是json 或者 yaml类型。
注意，如果文件以”.yml”或者”.yaml”结尾，ddt会作为yaml类型处理，其他所有文件都会作为json文件处理。如果文件中是列表，每个列表的值会作为测试用例参数，同时作为测试用例方法名后缀显示。
如果文件中是字典，字典的key会作为测试用例方法的后缀显示，字典的值会作为测试用例参数。

 - ddt.unpack：

传递的是复杂的数据结构时使用。比如使用元组或者列表，添加unpack之后，ddt会自动把元组或者列表对应到多个参数上。字典也可以这样处理。

```python
from selenium import webdriver
import unittest
import time
from ddt import ddt,file_data,unpack,data


@ddt
class testCase1(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.url = "https://www.baidu.com/"
        self.driver.maximize_window()
        time.sleep(3)

    def tearDown(self):
        self.driver.quit()

    # @data("孔刘", "Lisa", "腾讯新闻", "阿里巴巴")
    #@file_data('test_baidu_data.json')
    @data(["Jolin", "Jolin_百度搜索"],["周深", "周深_百度搜索"],["中概股", "中概股_百度搜索"])
    @unpack
    def test_baidu1(self, value1, value2):
        driver = self.driver
        driver.get(self.url)
        driver.find_element_by_id("kw").send_keys(value1)
        driver.find_element_by_id("su").click()
        time.sleep(6)
        print(driver.title)
        self.assertEqual(driver.title, value2,msg="fail!!!!")
        time.sleep(6)

    if __name__ == "__main__":
        unittest.main(verbosity=0)
```
```python
# -*- coding: utf-8 -*-
from selenium import webdriver
import unittest
import time
from ddt import ddt, unpack, data, file_data
import sys, csv

def getCsv(file_name):
    rows=[]
    path=sys.path[0]

    with open(path+'/data/'+file_name, 'rt') as f:
        readers = csv.reader(f, delimiter=',', quotechar='|')
        next(readers, None)
        for row in readers:
            # [周迅，周迅_百度搜索]
            temprows=[]
            for i in row:
                temprows.append(i)
            rows.append(temprows)
        # ([周迅,周迅_百度搜索],[张国荣,张国荣_百度搜索],[张一山,张一山_百度搜索])
        return rows

@ddt
class Baidu1(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(30)
        self.base_url = "http://www.baidu.com/"
        self.driver.maximize_window()

    def tearDown(self):
        self.driver.quit()

    @data(*getCsv('test_baidu_data.txt'))
    # ([周迅,周迅_百度搜索],[张国荣,张国荣_百度搜索],[张一山,张一山_百度搜索])
    @unpack
    def test_baidu2(self, value, expected_value):
        driver = self.driver
        driver.get(self.base_url + "/")
        driver.find_element_by_id("kw").clear()
        driver.find_element_by_id("kw").send_keys(value)
        driver.find_element_by_id("su").click()
        driver.maximize_window()
        time.sleep(6)
        # 判断搜索网页的title和我们期望的是否一致
        print(expected_value)
        print(driver.title)
        self.assertEqual(expected_value, driver.title, msg="和预期搜索结果不一致！")
        time.sleep(6)

if __name__ == '__main__':
    unittest.main()
```

