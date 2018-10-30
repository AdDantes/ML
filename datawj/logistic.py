from sklearn.linear_model import LogisticRegression,RandomizedLogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import StandardScaler
import pandas as pd

#是否录取
luqu = open('D:\GIT\datawj\data\luqu.csv')
data = pd.read_csv(luqu)
# print(data)
y = data.iloc[:,0]
x = data.iloc[:,1:]

#特征筛选
rlr = RandomizedLogisticRegression()
rlr.fit(x,y)
print(rlr.get_support())
print(rlr.scores_)
print(data.columns[rlr.get_support(True)])
t = data[data.columns[rlr.get_support(True)]]

#数据划分
y = t.iloc[:,0]
x = t.iloc[:,1:2]
X_train = x[:380]
X_test = x[380:]
Y_train = y[:380]
Y_test = y[380:]

#使用逻辑回归训练模型
lr = LogisticRegression()
lr.fit(X_train,Y_train)

#评估模型
pre = lr.predict(X_test)
score = lr.score(X_test,Y_test)
print(pre)
print(score)

