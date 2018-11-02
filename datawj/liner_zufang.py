import pandas as pd
from pymongo import MongoClient
from sklearn.linear_model import LinearRegression,SGDRegressor,Ridge
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
print(data1.describe())
print(data1.shape)
print(data1.columns)
data2 = data1.T
# print(data2)
rent = data2.values[12]
area = data2.values[6]
plt.plot(area,rent,'o')
plt.xlabel('area')
plt.ylabel('rent')
plt.show()
line = len(data1.values)
col = len(data1.values[0])
da = data1.values
print(da)
for i in range(0,line):
    for j in range(0,col):
        if (da[i][6]>300):
            # print(da[i][4])
            # print(da[i][6])
            da[i][6] = 57.0
            # print(da[i][6])
            # print('*******************')
        if (da[i][12]>30000):
            # print(da[i][4])
            # print(da[i][12])
            da[i][12] = 3600
            # print(da[i][12])
            # print('*******************')
da1 = pd.DataFrame(da)
da2 = da1.T
rent = da2.values[12]
area = da2.values[6]
plt.plot(area,rent,'o')
plt.xlabel('area')
plt.ylabel('rent')
plt.show()


# x['area'].fillna(x['area'].mean(),axis=0,inplace=True)
# x['metro_distance'].fillna(x['metro_distance'].mean(),axis=0,inplace=True)

# print(y)
# X_train,X_test,Y_train,Y_test = train_test_split(x,y,test_size=0.1)

# ss = StandardScaler()
# ss.fit_transform(X_train)
# ss.transform(X_test)
# plt.plot(X_train,Y_train)
# plt.title('show')
# plt.xlabel('area mt')
# plt.ylabel('rent')
# plt.ylim(0,50000)
# plt.show()
# dict = DictVectorizer()
# X_train = X_train.to_dict(orient='records')
# X_test = X_test.to_dict(orient='records')
# X_train = dict.fit_transform(X_train)
# X_test = dict.transform(X_test)
# print('真实结果为：',Y_test.values)
# lr = LinearRegression()
# lr.fit(X_train,Y_train)
# y_predict = lr.predict(X_test)
#
#
# print('正规方程预测的结果为：', [round(i,2) for i in y_predict])
# #7.评测数据
# weights = lr.coef_
# print('正规方程得到的权重值：',weights)
# mse = mean_squared_error(Y_test,y_predict)
# print('正规方程均方误差为：',mse)
