#coding:utf-8

import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Conv2D, MaxPooling2D,Dropout, Activation, Flatten
from keras.datasets import mnist
from tensorflow.examples.tutorials.mnist import input_data
from keras.optimizers import SGD, Adadelta, Adagrad
from keras.utils import np_utils
from keras import backend as K
K.set_image_dim_ordering('th')
#超参数
batch_size=100
nb_epoch=30
#加载数据,60000个训练样本：X_train、Y_train;10000个测试样本：X_test、Y_test
(X_train,Y_train),(X_test,Y_test) = mnist.load_data()
#reshape to be [samples][pixels][width][height]

X_train = X_train.reshape(X_train.shape[0],1,28,28).astype('float32')
X_test = X_test.reshape(X_test.shape[0],1,28,28).astype('float32')
X_train = X_train/255
X_test = X_test/255
Y_train = np_utils.to_categorical(Y_train)
Y_test = np_utils.to_categorical(Y_test)

#生成一个序贯型model
model = Sequential()
#第一个卷积层，6个卷积核，每个卷积核大小5*5。采用maxpooling，poolsize为(2,2),横纵各压为原来一半
model.add(Conv2D(6,(5,5), input_shape=(1,28,28),activation='relu'))
model.add(MaxPooling2D(pool_size=(2,2)))
#第二个卷积层，16个卷积核，每个卷积核大小3*3。6表示输入的特征图个数，等于上一层的卷积核个数
model.add(Conv2D(16, (3,3),activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
#全连接层，先将前一层输出的二维特征图flatten为一维的。
model.add(Flatten())
model.add(Dense(128,activation='relu')) #input_dim=16*3*3, output_dim=128
#Softmax分类，输出是10类别
model.add(Dense(10))
model.add(Activation('softmax'))
#model.compile里的参数loss就是损失函数(目标函数)
#sgd = SGD(l2=0.0,lr=0.05, decay=1e-6, momentum=0.9, nesterov=True)
model.compile(loss='categorical_crossentropy', optimizer='SGD',metrics=['accuracy'])
#调用fit方法，就是一个训练过程. 训练的epoch数设为10，batch_size为100．数据经过随机打乱shuffle=True。
model.fit(X_train,Y_train, batch_size,nb_epoch,shuffle=True)
cost = model.evaluate(X_test,Y_test)
print('Loss: %.3f' %cost[0], 'Accuracy: %.3f' % cost[1])
