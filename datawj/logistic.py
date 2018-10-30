from sklearn.linear_model import LogisticRegression,RandomizedLogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import StandardScaler
import pandas as pd
import numpy as np

luqu = open('D:\GIT\datawj\data\luqu.csv')
data = pd.read_csv(luqu)
# print(data)
y = data.iloc[:,0].as_matrix()
x = data.iloc[:,1:].as_matrix()
print(x)
X_train = x[:390]
X_test = x[390:]
Y_train = y[:390]
Y_test = y[390:]
#
ss = StandardScaler()
X_train = ss.fit_transform(X_train)
X_test = ss.transform(X_test)

rlr = RandomizedLogisticRegression()
rlr.fit(X_train,Y_train)
print(rlr.get_support())
print(rlr.scores_)
print(data.columns[rlr.get_support()])
# print(u'有效特征为：%s'%','.join(data.iloc[0,:].columns)[lr.get_support()])
# lr = LogisticRegression()
# lr.fit(X_train,Y_train)
# pre = lr.predict(X_test)
# score = lr.score(X_test,Y_test)
# print(pre)
# print(score)

