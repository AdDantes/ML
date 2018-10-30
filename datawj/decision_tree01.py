from sklearn.tree import DecisionTreeClassifier
from sklearn.feature_extraction import DictVectorizer
import pandas as pd


"""使用决策树预测销量"""
data = pd.read_csv('D:\project\datawj\lesson.csv', encoding='gbk')
print(data)
x = data.iloc[:, 1:5]
y = data['销量']
#数据划分
x_train = x[:26]
x_test = x[26:]
y_train = y[:26]
y_test = y[26:]
#特征工程：字典特征抽取
dict = DictVectorizer()
X_train = x_train.to_dict(orient='records')  # records : list like :[{column -> value}, ... , {column -> value}]
X_test = x_test.to_dict(orient='records')
X_train = dict.fit_transform(X_train)
X_test = dict.transform(X_test)
#使用决策树训练模型
tree = DecisionTreeClassifier()
# tree = KNeighborsClassifier(n_neighbors=25)
tree.fit(X_train, y_train)
# 模型评估
y_predict = tree.predict(X_test)
score = tree.score(X_test, y_test)
print(y_predict)
print(score)
