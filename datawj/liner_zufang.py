import pandas as pd
from pymongo import MongoClient
from sklearn.linear_model import LinearRegression,SGDRegressor,Ridge
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.feature_extraction import DictVectorizer
from sklearn.metrics import mean_squared_error
import matplotlib.pylab as plt


client = MongoClient(host='192.168.1.116')
db = client.zufang
tongcheng = db.tongcheng
data = tongcheng.find()
data1 = pd.DataFrame(list(data))
# print(data1.describe())
# print(data1.shape)
print(data1.columns)
data2 = data1.T
# print(data2)
# rent = data2.values[12]
# area = data2.values[6]
# plt.plot(area,rent,'o')
# plt.xlabel('area')
# plt.ylabel('rent')
# plt.show()
line = len(data1.values)
col = len(data1.values[0])
da = data1.values
for i in range(0,line):
    for j in range(0,col):
        if (da[i][6]>100):
            # print(da[i][4])
            # print(da[i][6])
            da[i][6] = 57.0
            # print(da[i][6])
            # print('*******************')
        if (da[i][12]>10000):
            # print(da[i][4])
            # print(da[i][12])
            da[i][12] = 3600
            # print(da[i][12])
            # print('*******************')

da1 = pd.DataFrame(da,columns = ['Big_quYu', 'Decoration', 'Orientation', 'Payment_method', 'Title',
       '_id', 'area', 'detail_quYu', 'floor', 'house_disposal', 'house_type',
       'metro_distance', 'rent', 'ret_method', 'xiao_qu'])
x = da1[['Big_quYu',  'Orientation',
       'area',
       'metro_distance', 'xiao_qu']]
y = da1['rent']
X_train,X_test,Y_train,Y_test = train_test_split(x,y,test_size=0.02)
# print(X_train)
# X_train = pd.DataFrame(list(X_train))
# Y_train = pd.DataFrame(list(Y_train))
# X_test = pd.DataFrame(list(X_test))
# ss = StandardScaler()
# ss.fit_transform(X_train)
# ss.transform(X_test)
#
dict = DictVectorizer()
X_train = X_train.to_dict(orient='records')
X_test = X_test.to_dict(orient='records')
X_train = dict.fit_transform(X_train)
X_test = dict.transform(X_test)
print('真实结果为：',Y_test.values)
lr = Ridge()
lr.fit(X_train,Y_train)
y_predict = lr.predict(X_test)

#
print('正规方程预测的结果为：', y_predict)
#7.评测数据
weights = lr.coef_
print('正规方程得到的权重值：',weights)
mse = mean_squared_error(Y_test,y_predict)
print('正规方程均方误差为：',mse)

