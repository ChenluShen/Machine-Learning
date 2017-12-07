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
#下面是查找多个元素（这些方法将返回一个列表）：<br>
find_elements_by_name<br>
find_elements_by_xpath<br>
find_elements_by_link_text<br>
find_elements_by_partial_link_text<br>
find_elements_by_tag_name<br>
find_elements_by_class_name<br>
find_elements_by_css_selector<br>

#二、操作元素方法<br>
# 在讲述完定位对象(locate elements)之后我们需要对该已定位对象进行操作，通常所有的操作与页面交互都将通过WebElement接口，常见的操作元素方法如下：<br>
clear 清除元素的内容<br>
send_keys 模拟按键输入<br>
click 点击元素<br>
submit 提交表单<br>

#三、WebElement接口获取值<br>
##通过WebElement接口可以获取常用的值，这些值同样非常重要。<br>
size 获取元素的尺寸<br>
text 获取元素的文本<br>
get_attribute(name) 获取属性值<br>
location 获取元素坐标，先找到要获取的元素，再调用该方法<br>
page_source 返回页面源码<br>
driver.title 返回页面标题<br>
current_url 获取当前页面的URL<br>
is_displayed() 设置该元素是否可见<br>
is_enabled() 判断元素是否被使用<br>
is_selected() 判断元素是否被选中<br>
tag_name 返回元素的tagName<br>
