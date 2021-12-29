# 用于测试模型
import numpy as np
from ai_logic_自己实现神经网络.training_model import Network


def get_ai():
    W1 = np.loadtxt('model/W1.txt', dtype=np.float64)
    b1 = np.loadtxt('model/b1.txt', dtype=np.float64)

    W2 = np.loadtxt('model/W2.txt', dtype=np.float64)
    b2 = np.loadtxt('model/b2.txt', dtype=np.float64)

    n = Network()
    n.fl1.set_parameters(W1, b1.reshape(n.fl1.output_size, 1))
    n.fl2.set_parameters(W2, b2.reshape(n.fl2.output_size, 1))
    return n


if __name__ == '__main__':

    n = get_ai()

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

    for i in range(10):
        L = 0
        for x, y in list(zip(X, Y)):
            res = n.forward(x)
            L += np.dot((res - y).T, res-y)
        print(i, L)










