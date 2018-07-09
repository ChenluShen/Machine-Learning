%matplotlib inline
import sys
sys.path.append('c:/python27/lib/site-packages')
import cv2
from matplotlib import pyplot as plt
from util import createLineIterator
import numpy as np
import math
import copy

def show(img, code=cv2.COLOR_BGR2RGB):
    #cv_rgb = cv2.cvtColor(img, code)
    fig, ax = plt.subplots(figsize=(16, 10))
    ax.imshow(img)
    fig.show()

# 读取图片
img = cv2.imread('6.jpg')
# 转换成灰度图
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# 高斯模糊
img_gb = cv2.GaussianBlur(img_gray, (5, 5), 0)
# 腐蚀膨胀，开运算
# img_erosion = cv2.erode(img_gb, None)
# img_dilate = cv2.dilate(img_erosion, None)

# 边缘检测
# 使用 Canny 函数检测边缘，选择 100 和 200 作为高低阈值：
edges = cv2.Canny(img_gb, 20 , 50, 5)
# 寻找定位标记
# 通过轮廓定位图像中的二维码。二维码的 Position Detection Pattern 在寻找轮廓之后，应该是有6层（因为一条边缘会被识别出两个轮廓，外轮廓和内轮廓）
img_fc, contours, hierarchy = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# areas = [cv2.contourArea(i) for i in contours]

hierarchy = hierarchy[0]
found = []
for i in range(len(contours)):
    k = i
    c = 0
    while hierarchy[k][2] != -1:
        k = hierarchy[k][2]
        c = c + 1
    if c >= 5:
        found.append(i)

for i in found:
    img_dc = img.copy()
    cv2.drawContours(img_dc, contours, i, (0, 255, 0), 3)
    show(img_dc)

# 招定标中心点
def getcenter(contour):
    x = [i[0][0] for i in contour]
    y = [j[0][1] for j in contour]
    c_x = (max(x)-min(x))/2 + min(x)
    c_y = (max(y)-min(y))/2 + min(y)
    return c_x, c_y

c = getcenter(contours[250])

cv2.circle(img_dc, c, 3,(0, 255, 0), 3)
show(img_dc)

# 定位筛选
'''
需要 Timing Pattern 的帮助，也就是定位标记之间的黑白相间的那两条黑白相间的线。解决思路大致如下：
将4个定位标记两两配对
将他们的4个顶点两两连线，选出最短的那两根
如果两根线都不符合 Timing Pattern 的特征，则出局
'''

# 二值化
th, bi_img = cv2.threshold(img_gb, 100, 255, cv2.THRESH_BINARY)

draw_img = img.copy()
for i in found:
    # 通过 minAreaRect 函数将检查到的轮廓转换成最小矩形包围盒
    rect = cv2.minAreaRect(contours[i])
    box = cv2.boxPoints(rect)
    box = np.int0(box)
    cv2.drawContours(draw_img,[box], 0, (0,0,255), 2)
show(draw_img)

boxes = []
for i in found:
    rect = cv2.minAreaRect(contours[i])
    box = cv2.boxPoints(rect)
    box = np.int0(box)
    box = map(tuple, box)
    boxes.append(box)

# 定位标记的顶点连线
def cv_distance(P, Q):
    return int(math.sqrt(pow((P[0] - Q[0]), 2) + pow((P[1] - Q[1]),2)))

# 验证是否是 Timing Pattern
'''
验证方案是：
先除去数组中开头和结尾处连续的白色像素点。
对数组中的元素进行计数，相邻的元素如果值相同则合并到计数结果中。比如 [0,1,1,1,0,0] 的计数结果就是 [1,3,2] 。
计数数组的长度如果小于 5 ，则不是 Timing Pattern 。
计算计数数组的方差，看看分布是否离散，如果方差大于阈值，则不是 Timing Pattern 。
'''
def isTimingPattern(line):
    # 除去开头结尾的白色像素点
    while line[0] != 0:
        line = line[1:]
    while line[-1] != 0:
        line = line[:-1]
    # 计数连续的黑白像素点
    c = []
    count = 1
    l = line[0]
    for p in line[1:]:
        if p == l:
            count = count + 1
        else:
            c.append(count)
            count = 1
        l = p
    c.append(count)
    # 如果黑白间隔太少，直接排除
    if len(c) < 5:
        return False
    # 计算方差，根据离散程度判断是否是 Timing Pattern
    threshold = 5
    return np.var(c) < threshold


def check(a, b, bi_img):
    # 存储 ab 数组里最短的两点的组合
    s1_ab = ()
    s2_ab = ()
    # 存储 ab 数组里最短的两点的距离，用于比较
    s1 = np.iinfo('i').max
    s2 = s1
    for ai in a:
        for bi in b:
            d = cv_distance(ai, bi)
            if d < s2:
                if d < s1:
                    s1_ab, s2_ab = (ai, bi), s1_ab
                    s1, s2 = d, s1
                else:
                    s2_ab = (ai, bi)
                    s2 = d
    a1, a2 = s1_ab[0], s2_ab[0]
    b1, b2 = s1_ab[1], s2_ab[1]
    # 对端点坐标进行调整
    scale = 14
    a1 = (a1[0] + (a2[0]-a1[0])*1/scale, a1[1] + (a2[1]-a1[1])*1/scale)
    b1 = (b1[0] + (b2[0]-b1[0])*1/scale, b1[1] + (b2[1]-b1[1])*1/scale)
    a2 = (a2[0] + (a1[0]-a2[0])*1/scale, a2[1] + (a1[1]-a2[1])*1/scale)
    b2 = (b2[0] + (b1[0]-b2[0])*1/scale, b2[1] + (b1[1]-b2[1])*1/scale)
    # 将最短的两个线画出来
    cv2.line(draw_img, a1, b1, (0,0,255), 3)
    cv2.line(draw_img, a2, b2, (0,0,255), 3)
    # show(draw_img) ################################################
    # 获取连线上的像素值
    line1 = createLineIterator(a1, b1, bi_img)
    line2 = createLineIterator(a2, b2, bi_img)
    return isTimingPattern(line1) or isTimingPattern(line2)

# 找出错误的定位标记
valid = set()
for i in range(len(boxes)):
    for j in range(i+1, len(boxes)):
        if check(boxes[i], boxes[j],bi_img):
            valid.add(i)
            valid.add(j)
print ('valid:',valid)
# 0、1、2、3 四个定位标记，0是无效的

# 找出二维码
def findQR(valid, found):
    contour_all = []
    validlist = valid.copy()
    while len(validlist) > 0:
        c = contours[found[validlist.pop()]]
        for sublist in c:
            for p in sublist:
                contour_all.append(p)

    contour_ALL = np.array(contour_all)
    rect = cv2.minAreaRect(contour_ALL)
    box = cv2.boxPoints(rect)
    bigbox = np.array(box)
    return bigbox


# 打印结果和二维码占图比
def QRexists(validboxes, found, img):
    if len(validboxes) == 3:
        bigbox = findQR(validboxes, found)
        # 打印图片
        draw_img = img.copy()
        cv2.polylines(draw_img, np.int32([bigbox]), True, (0, 0, 255), 10)
        show(draw_img) ################################################
        # 计算占图比
        x = [i[0] for i in bigbox]
        y = [j[1] for j in bigbox]
        width = max(x)-min(x)
        height = max(y)-min(y)
        ratio = float(width*height)/float(img.shape[0]*img.shape[1])
        return ratio*100
    else:
        return False
print('ratio:',QRexists(valid, found, img))
