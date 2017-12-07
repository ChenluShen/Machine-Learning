爬虫
==== 
 Selenium常见元素定位方法和操作的学习介绍
 ------- 
 http://blog.csdn.net/eastmount/article/details/48108259<br>
#一. 定位元素方法<br>
find_element_by_id<br>
find_element_by_name<br>
find_element_by_xpath<br>
find_element_by_link_text<br>
find_element_by_partial_link_text<br>
find_element_by_tag_name<br>
find_element_by_class_name<br>
find_element_by_css_selector<br>
#下面是查找多个元素（这些方法将返回一个列表）：
find_elements_by_name
find_elements_by_xpath
find_elements_by_link_text
find_elements_by_partial_link_text
find_elements_by_tag_name
find_elements_by_class_name
find_elements_by_css_selector

#二、操作元素方法
# 在讲述完定位对象(locate elements)之后我们需要对该已定位对象进行操作，通常所有的操作与页面交互都将通过WebElement接口，常见的操作元素方法如下：
clear 清除元素的内容
send_keys 模拟按键输入
click 点击元素
submit 提交表单

#三、WebElement接口获取值
##通过WebElement接口可以获取常用的值，这些值同样非常重要。
size 获取元素的尺寸
text 获取元素的文本
get_attribute(name) 获取属性值
location 获取元素坐标，先找到要获取的元素，再调用该方法
page_source 返回页面源码
driver.title 返回页面标题
current_url 获取当前页面的URL
is_displayed() 设置该元素是否可见
is_enabled() 判断元素是否被使用
is_selected() 判断元素是否被选中
tag_name 返回元素的tagName
