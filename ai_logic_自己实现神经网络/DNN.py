# 实现神经网络反向传播算法，以此来训练网络。全连接神经网络可以包含多层，但是只有最后一层输出前有激活函数。
# 所谓向量化编程，就是使用矩阵运算。

import random
import math
import numpy as np
import datetime
from ai_logic_自己实现神经网络 import Activators  # 引入激活器模块


# 1. 当为array的时候，默认d*f就是对应元素的乘积，multiply也是对应元素的乘积，dot（d,f）会转化为矩阵的乘积， dot点乘意味着相加，而multiply只是对应元素相乘，不相加
# 2. 当为mat的时候，默认d*f就是矩阵的乘积，multiply转化为对应元素的乘积，dot（d,f）为矩阵的乘积


# 全连接每层的实现类。输入对象x、神经层输出a、输出y均为列向量
class FullConnectedLayer(object):  # (192, 10, Activators.SigmoidActivator(),0.02)
    # 全连接层构造函数。input_size: 本层输入列向量的维度。output_size: 本层输出列向量的维度。activator: 激活函数
    def __init__(self, input_size, output_size, activator, learning_rate):
        self.input_size = input_size
        self.output_size = output_size
        self.activator = activator

        wimin = -math.sqrt(6 / (output_size + input_size))
        wimax = math.sqrt(6 / (output_size + input_size))
        self.W = np.random.uniform(wimin, wimax, (output_size, input_size))
        self.b = np.zeros((output_size, 1))
        # 学习速率
        self.learning_rate = learning_rate
        # 输出向量
        self.output = np.zeros((output_size, 1))  # 初始化为全0列向量
        self.input = None

    # 前向计算，预测输出。input_array: 输入列向量，维度必须等于input_size
    def forward(self, input_array):  # 式2
        self.input = input_array
        self.output = self.activator.forward(np.dot(self.W, input_array) + self.b)

    # 反向计算W和b的梯度。delta_array: 从上一层传递过来的误差项。
    # 列向量
    def backward(self, delta_array):
        # 这里的activator应该是上一层的，所以在这一层无法准备，还不如放在上一层让他自己处理
        # activator.backward 相当于f'(z)
        # self.input是上一层输出
        '''这里本应该用上一层的激活器'''
        # 对应元素相乘
        self.delta = np.multiply(self.activator.backward(self.output), delta_array)

        self.W_grad = np.dot(self.delta, self.input.T)
        self.b_grad = self.delta

    # 使用梯度下降算法更新权重
    def update(self):
        self.W -= self.learning_rate * self.W_grad
        self.b -= self.learning_rate * self.b_grad

    def set_parameters(self, W, b):
        self.W = W
        self.b = b
