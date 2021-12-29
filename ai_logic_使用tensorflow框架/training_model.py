# 通过数据训练并保存模型

import numpy as np
import tensorflow as tf

data_source = np.loadtxt('data/data.txt', dtype='float')
res_source = np.loadtxt('data/res.txt', dtype='float')

data = np.array(data_source)
res = np.array(res_source)

print(data.shape)


def add_layer(inputs, in_size, out_size, activation_function=None):
    """
    :param input: 数据输入
    :param in_size: 输入大小
    :param out_size: 输出大小
    :param activation_function: 激活函数（默认没有）
    :return:output：数据输出
    """
    Weights = tf.Variable(tf.random_normal([in_size, out_size]))
    biases = tf.Variable(tf.zeros([1, out_size]) + 0.1)
    Wx_plus_b = tf.matmul(inputs, Weights) + biases
    if activation_function is None:
        outputs = Wx_plus_b
    else:
        outputs = activation_function(Wx_plus_b)
    return outputs


xs = tf.placeholder(tf.float32, [None, 7])
ys = tf.placeholder(tf.float32, [None, 2])

# 定义神经网络结构
hidden_layer1 = add_layer(xs, 7, 30, activation_function=tf.nn.sigmoid)
prediction = add_layer(hidden_layer1, 30, 2, activation_function=tf.nn.sigmoid)

loss = tf.reduce_mean(tf.reduce_sum(tf.square(ys - prediction), reduction_indices=[1]))
train_step = tf.train.GradientDescentOptimizer(0.1).minimize(loss)

saver = tf.train.Saver()

init = tf.global_variables_initializer()
sess = tf.Session()
sess.run(init)

# 3.进行训练

for i in range(10000):
    sess.run(train_step, feed_dict={xs: data, ys: res})
    if i % 100 == 0:
        print(sess.run(loss, feed_dict={xs: data, ys: res}))
saver.save(sess, "model/nn_car")

# 关闭sess
sess.close()
