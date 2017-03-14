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


from tensorflow.examples.tutorials.mnist import input_data
import tensorflow as tf


mnist = input_data.read_data_sets("Mnist_data/", one_hot=True)


#create model
with tf.name_scope('input'):
    x = tf.placeholder(tf.float32, [None, 748], name='x_input')
    y_ = tf.placeholder(tf.float32, [None, 10], name='y_input')

with tf.name_scope('layer'):
    with tf.name_scope('W'):
        W = tf.Variable(tf.zeros([784, 10], name='Weights'))
    with tf.name_scope('b'):
        b = tf.Variable(tf.zeros([10]), name='biases')
    with tf.name_scope('W_p_b'):
        Wx_plus_b = tf.add(tf.matmul(x, W), b, 'Wx_plus_b')

    y = tf.nn.softmax(Wx_plus_b, name='final_result')
    print(y)

#define loss and optimizer
with tf.name_scope('loss'):
    loss = -tf.reduce_sum(y_ * tf.log(y))
with tf.name_scope('train_step'):
    train_step = tf.train.GradientDescentOptimizer(0.01).minimize(loss)
    print(train_step)

sess = tf.InteractiveSession()
init = tf.global_variables_initializer()
sess.run(init)
writer = tf.summary.FileWriter('logs/', sess.graph)

#train
for step in range(100):
    batch_xs, batch_ys = mnist.train.next_batch()
    train_step.run({x: batch_xs, y: batch_ys})
    print(step)
    variables = tf.all_variables()
    saver = tf.train.Saver(variables)
    print(len(variables))
    print(sess.run(b))
    #print W.get_shape(),b.get_shape()
    saver.save(sess, "data/soft.ckpt")

correct_prediction = tf.equal(tf.argmax(y, 1), tf.argmax(y_, 1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
a = accuracy.eval({x: mnist.test.images, y_: mnist.test.labels})
print('最终的测试正确率：{0}'.format(a))
tf.train.write_graph(sess.graph_def, 'graph', 'soft.ph', False)
