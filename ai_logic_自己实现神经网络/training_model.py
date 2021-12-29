# 用于训练模型
import numpy as np
import ai_logic_自己实现神经网络.Activators as Activators
import ai_logic_自己实现神经网络.DNN as DNN


# 网络模型类
class Network:
    # 定义网络结构
    def __init__(self):
        # 全连接层构造函数。input_size: 本层输入向量的维度. output_size: 本层输出向量的维度. activator: 激活函数. learning_rate: 学习率
        self.fl1 = DNN.FullConnectedLayer(7, 30, Activators.TanhActivator(), 0.05)
        self.fl2 = DNN.FullConnectedLayer(30, 2, Activators.TanhActivator(), 0.05)

    # 向前传播
    def forward(self, input):
        self.fl1.forward(input)
        self.fl2.forward(self.fl1.output)
        return self.fl2.output

    # 反向传播
    def backward(self, labels):
        # 计算误差
        delta = self.fl2.output - labels
        # 反向传播
        self.fl2.backward(delta)
        self.fl2.update()
        self.fl1.backward(np.dot(self.fl2.W.T, self.fl2.delta))
        self.fl1.update()


if __name__ == '__main__':

    data_source = np.loadtxt('data/data.txt', dtype='float')
    res_source = np.loadtxt('data/res.txt', dtype='float')

    data = np.array(data_source)
    res = np.array(res_source)
    # (516, 7) (516, 2)

    # 归一化
    col_max = []
    temp = np.zeros_like(data)
    for i in range(7):
        t = max(data[:, i])
        col_max.append(t)
        temp[:, i] = data[:, i] / t

    X = np.array([np.reshape(x, (7, 1)) for x in temp])
    Y = np.array([np.reshape(y, (2, 1)) for y in res])

    # print(X.shape, Y.shape)

    n = Network()

    epochs = 500
    for i in range(epochs):
        L = 0
        for x, y in list(zip(X, Y)):
            res = n.forward(x)
            n.backward(y)
        for x, y in list(zip(X, Y)):
            res = n.forward(x)
            L += np.dot((res - y).T, res-y)
        if i % 10 == 0:
            print(i, L)


    np.savetxt('model/W1.txt', n.fl1.W, fmt='%.16f')
    np.savetxt('model/b1.txt', n.fl1.b, fmt='%.16f')

    np.savetxt('model/W2.txt', n.fl2.W, fmt='%.16f')
    np.savetxt('model/b2.txt', n.fl2.b, fmt='%.16f')

    np.savetxt('model/col_max.txt', np.array(col_max), fmt='%.16f')








