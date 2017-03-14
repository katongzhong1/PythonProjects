# -*- coding: utf-8 -*-
# ---------------------------------------
#   程序：MNIST数据集
#   版本：1.0
#   作者：zhong
#   日期：2017-03-08
#   语言：Python 2.7
#   操作：
#   功能：
# ---------------------------------------


from __future__ import print_function
import tensorflow as tf
import input_data

# 60000行的训练数据集（mnist.train）和10000行的测试数据集（mnist.test)
mnist = input_data.read_data_sets("MNIST_data/", one_hot=True)


def weight_variable(shape):
    initial = tf.truncated_normal(shape, stddev=0.1)
    return tf.Variable(initial)


def bias_variable(shape):
    initial = tf.constant(0.1, shape=shape)
    return tf.Variable(initial)


def conv2d(x, W):
    return tf.nn.conv2d(x, W, strides=[1, 1, 1, 1], padding='SAME')


def max_pool_2x2(x):
    return tf.nn.max_pool(x, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')

# 为输入图像和目标输出类别创建节点，开始构建计算图 （都为占位符）
#==> 2维的浮点数张量 784 代表一张展平的 MNIST图片的维度，None代指 batch的大小
x = tf.placeholder("float", shape=[None, 784])
#==> 2维张量 其中每一行为一个10维的one—hot向量，代表对应某一 MNIST图片的类别
##==> 此处代表0,1,2,3,4,5,6,7,8,9
y_ = tf.placeholder("float", shape=[None, 10])


W_conv1 = weight_variable([5, 5, 1, 32])
b_conv1 = bias_variable([32])

x_image = tf.reshape(x, [-1, 28, 28, 1])

h_conv1 = tf.nn.relu(conv2d(x_image, W_conv1) + b_conv1)
h_pool1 = max_pool_2x2(h_conv1)

W_conv2 = weight_variable([5, 5, 32, 64])
b_conv2 = bias_variable([64])

h_conv2 = tf.nn.relu(conv2d(h_pool1, W_conv2) + b_conv2)
h_pool2 = max_pool_2x2(h_conv2)

W_fc1 = weight_variable([7 * 7 * 64, 1024])
b_fc1 = bias_variable([1024])

h_pool2_flat = tf.reshape(h_pool2, [-1, 7*7*64])
h_fc1 = tf.nn.relu(tf.matmul(h_pool2_flat, W_fc1) + b_fc1)

keep_prob = tf.placeholder("float")
h_fc1_drop = tf.nn.dropout(h_fc1, keep_prob)

W_fc2 = weight_variable([1024, 10])
b_fc2 = bias_variable([10])

# 回归模型
#==> 向量化的图片x和权重矩阵W相乘加上偏值b, 然后计算每个分类的 softmax概念值
y_conv = tf.nn.softmax(tf.matmul(h_fc1_drop, W_fc2) + b_fc2)

#训练和评估模型
# 交叉熵 (为训练过程指定最小化误差用的损失函数，是目标类别和预测类别之间的交叉熵)
cross_entropy = -tf.reduce_sum(y_ * tf.log(y_conv))
# ADAM优化器来做梯度最速下降
#==> 往计算图中添加一个新的操作, 其中包括计算梯度，计算每个参数的步长变化，并且计算出新的参数值
#===> 返回操作对象，运行时会使用梯度下降来更新参数
train_step = tf.train.AdamOptimizer(1e-4).minimize(cross_entropy)
# 评估
#===> tf.argmax 能给出某个tensor在某一维上的其数据最大值所在的索引值
correct_prediction = tf.equal(tf.argmax(y_conv, 1), tf.argmax(y_, 1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, "float"))

sess = tf.InteractiveSession()
sess.run(tf.global_variables_initializer())


for i in range(20000):
    batch = mnist.train.next_batch(50)
    if i % 100 == 0:
        train_accurary = accuracy.eval(feed_dict={x: batch[0], y_: batch[1], keep_prob: 1.0})
        print("step %d, training accurary %g" % (i, train_accurary))
    sess.run(train_step, feed_dict={x: batch[0], y_: batch[1], keep_prob: 1.0})

print("test accuracy %g" % accuracy.eval(feed_dict={x: mnist.test.images, y_: mnist.test.labels, keep_prob: 1.0}))
