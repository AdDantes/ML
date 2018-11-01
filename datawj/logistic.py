from sklearn.linear_model import LogisticRegression,RandomizedLogisticRegression
from sklearn.model_selection import train_test_split
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
X_train,X_test,Y_train,Y_test = train_test_split(x,y,test_size=.2)
#使用逻辑回归训练模型
lr = LogisticRegression()
lr.fit(X_train,Y_train)

#评估模型
pre = lr.predict(X_test)
score = lr.score(X_test,Y_test)
print(pre)
print(score)

