from sklearn.linear_model import LinearRegression,SGDRegressor,Ridge,LogisticRegression
from sklearn.datasets import load_boston
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import StandardScaler
from sklearn.externals import joblib
from sklearn.metrics import classification_report
import pandas as pd
import numpy as np


def zhenggui():
    """
    利用最小二乘法的正规方程来进行波士顿房价的预测
    :return: 
    """
    #1.加载数据
    boston = load_boston()
    #2.分割数据
    X_train, X_test, y_train, y_test = train_test_split(boston.data,boston.target,test_size=0.25)
    #3.标准化处理
    ss = StandardScaler()
    X_train = ss.fit_transform(X_train)
    X_test = ss.transform(X_test)
    #4.创建正规方程的实例
    lr = LinearRegression()
    #5.训练模型
    lr.fit(X_train,y_train)
    #6.预测数据
    y_predict = lr.predict(X_test)
    print('正规方程预测的结果为：', y_predict)
    #7.评测数据
    weights = lr.coef_
    print('正规方程得到的权重值：',weights)
    mse = mean_squared_error(y_test,y_predict)
    print('正规方程均方误差为：',mse)
def tidu():
    """
        利用最小二乘法的梯度下降来进行波士顿房价的预测
        :return: 
        """
    # 1.加载数据
    boston = load_boston()
    # 2.分割数据
    X_train, X_test, y_train, y_test = train_test_split(boston.data, boston.target, test_size=0.25)
    # 3.标准化处理
    ss = StandardScaler()
    X_train = ss.fit_transform(X_train)
    X_test = ss.transform(X_test)
    # 4.创建梯度下降的实例
    sgd = SGDRegressor()
    # 5.训练模型
    sgd.fit(X_train, y_train)
    # 6.预测数据
    y_predict = sgd.predict(X_test)
    print('梯度下降预测的结果为：', y_predict)
    # 7.评测数据
    weights = sgd.coef_
    print('梯度下降得到的权重值：', weights)
    mse = mean_squared_error(y_test, y_predict)
    print('梯度下降均方误差为：', mse) #预测值减去真实值

def ridge():
    """
        利用岭回归来进行波士顿房价的预测
        :return: 
        """
    # 1.加载数据
    boston = load_boston()
    # 2.分割数据
    X_train, X_test, y_train, y_test = train_test_split(boston.data, boston.target, test_size=0.25,random_state=2)
    # 3.标准化处理
    ss = StandardScaler()
    X_train = ss.fit_transform(X_train)
    X_test = ss.transform(X_test)
    # ridge = Ridge()
    # ridge.fit(X_train,y_train)
    # #fit后模型就产生了，可以存储。
    # joblib.dump(ridge,'model01.pkl')

    #如果保存了模型，可以从本地将模型读取，进行预测
    ridge = joblib.load('model01.pkl')

    y_predict = ridge.predict(X_test)
    weights = ridge.coef_
    print('岭回归预测的结果为：', y_predict)
    print('岭回归得到的权重值：', weights)
    mse = mean_squared_error(y_test, y_predict)
    print('岭回归均方误差为：', mse)  # 预测值减去真实值

def logistic():
    """
    利用逻辑回归进行肿瘤预测
    :return: 
    """

    #1.数据获取，数据处理
    column_names = ['Sample code number', 'Clump Thickness', 'Uniformity of Cell Size', 'Uniformity of Cell Shape',
                    'Marginal Adhesion', 'Single Epithelial Cell Size', 'Bare Nuclei', 'Bland Chromatin',
                    'Normal Nucleoli', 'Mitoses', 'Class']
    data = pd.read_csv('https://archive.ics.uci.edu/ml/machine-learning-databases/breast-cancer-wisconsin/breast-cancer-wisconsin.data',names=column_names)
    # print(data.shape)
    # 替换数据中的“？”为np.nan，才能对空值做处理
    data.replace(to_replace='?',value=np.nan,inplace=True)
    data.dropna(inplace=True)
    # print(data.shape) #查看数据行数，列数情况
    y = data.iloc[:,-1]  #先行，后列
    X = data.iloc[:,1:-1]
    #2.数据划分
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25)
    #3.选择估计器
    lr = LogisticRegression()
    #4.训练模型
    lr.fit(X_train, y_train)
    #5.预测，评价模型
    y_predict = lr.predict(X_test)
    score = lr.score(X_test,y_test)
    weights = lr.coef_
    print('精准度为：',score)
    print("逻辑回归中的权重为：", weights)
    ret = classification_report(y_test, y_predict, labels=[2, 4], target_names=["良性", "恶性"])
    print(ret)


if __name__ == '__main__':
    # zhenggui()
    # tidu()
    # ridge()
    logistic()
