# coding=utf-8
import numpy as np 
from keras.models import Sequential
from keras.layers import Dense, Activation,Dropout,Flatten
from tensorflow.examples.tutorials.mnist import input_data
from keras.optimizers import SGD,adam

#加载数据———分为训练集和测试集
#55000个训练样本：X_train、Y_train
#10000个测试样本：X_test、Y_test
mnist = input_data.read_data_sets('MNIST_data',one_hot=True)
X_train = mnist.train.images
Y_train = mnist.train.labels
X_test = mnist.test.images
Y_test = mnist.test.labels

batch_size=100
nb_epoch=10

#搭建全连接网络
# 784-500-10
model = Sequential()
#第一层全连接，输入维数24*24，输出维数500
model.add(Dense(input_dim = 784,output_dim = 500))
model.add(Activation('relu'))
model.add(Dropout(0.5))
#第二层全连接
model.add(Dense(output_dim = 500))
model.add(Activation('relu'))
model.add(Dropout(0.5))
#第三层全连接，输出维数10，再分类
model.add(Dense(output_dim = 10))
model.add(Activation('softmax'))

#训练
#选择crossentropy作为loss函数
model.compile(loss = 'categorical_crossentropy',optimizer='SGD',metrics=['accuracy'])
model.fit(X_train,Y_train,batch_size,nb_epoch,shuffle=True)

#评估
cost = model.evaluate(X_test,Y_test)
print('/n/n')
print('Loss: %.3f' %cost[0] , 'Accuracy: %.3f' % cost[1])

Y_pred = model.predict(X_test)

# 加载图片
import matplotlib.pyplot as plt
import matplotlib.cm as cm
def display(img):
    one_image = img.reshape(28,28)    
    plt.axis('off')
    plt.imshow(one_image, cmap=cm.binary)
    plt.show()

def predict(x):
     re = np.where(x == np.max(x))
     return re

def show(num):
     #原图片
     display(X_test[num])
     #预测的数字
     print('预测的数字为：\t',predict(Y_pred[num])[0][0])

#show(1)
#括号内输入0-9999、查看图片预测结果
