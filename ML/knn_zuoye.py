from sklearn import datasets
from sklearn.model_selection import train_test_split,GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier

#获取数据
iris = datasets.load_iris()
# print(iris)
#取出数据中的目标和特征
y = iris.target
X = iris.data
#数据划分：
#1.X_train：训练的特征数据，对于特征来说一般是多个多维数据用大写
#2.X_test：测试的特征数据
#3.y_train:训练的目标数据
#4.y_test:测试的目标数据
X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.25,random_state=1)
#特征工程（数据的标准化处理）
ss = StandardScaler()
X_train = ss.fit_transform(X_train)
X_test = ss.transform(X_test)
#选择估计器（算法），训练模型
knn = KNeighborsClassifier(n_neighbors=32)
knn.fit(X_train,y_train)
y_predict = knn.predict(X_test)
# print(X_test,y_predict)
score = knn.score(X_test,y_test)
# print('预测的结果为：',y_predict)
# print('精准度为：',score)

gs = GridSearchCV(knn,param_grid={'n_neighbors':[1,3,5,7]},cv=4)
gs.fit(X_train,y_train)
print('精准度为：',gs.score(X_test,y_test))
print('在交叉验证中得到的最好结果：',gs.best_score_)
print('每次交叉验证的结果：',gs.cv_results_)
print('最好的参数模型',gs.best_estimator_)

