import pandas as pd
from sklearn.preprocessing import Imputer
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction import DictVectorizer
from sklearn.tree import DecisionTreeClassifier,export_graphviz
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from sklearn.model_selection import GridSearchCV

def decision_tree():
    """利用决策树，实现泰坦尼克号案例"""
# 1.获取数据
    data = pd.read_csv('http://biostat.mc.vanderbilt.edu/wiki/pub/Main/DataSets/titanic.txt')
    # print(data)
# 2.处理数据
    # 分割数据,从data中获取X，y
    y = data['survived']
    X = data[['pclass','age','sex']]
    # print(X,y)
    #缺失值处理·
    X['age'].fillna(X['age'].mean(),axis=0,inplace=True) #inplace改掉原来X的值
    # i = Imputer(missing_values='NaN',strategy='mean',axis=0)
    # age = i.fit_transform(X['age'],inplace = True)
    # print(age)
    #数据划分
    X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.25,random_state=1)
    # print(X_train)

# 3.特征工程
    #特征中有字符串也有数值，用字典特征抽取
    dict = DictVectorizer()
    #由于多个字典，fit_transform括号内[{}],将训练特征转换成列表套字典的形式
    X_train = X_train.to_dict(orient='records') # records : list like :[{column -> value}, ... , {column -> value}]
    X_test = X_test.to_dict(orient='records')
    X_train = dict.fit_transform(X_train)
    X_test = dict.transform(X_test)

# 4.选择估计器，训练模型
    tree = DecisionTreeClassifier()
    tree.fit(X_train,y_train)
    # print(X_train.toarray())
# 5.预测数据
    y_predict = tree.predict(X_test)
# 6.得出准确率，评测数据
    score = tree.score(X_test,y_test)
    # print('预测的结果为：',y_predict)
    print('使用决策树的精准度为：',score)
    # 导出决策树结构
    # export_graphviz(tree,out_file='tree.dot',feature_names=['age','1st','2nd','3rd','female','male'])

def random_forest():
    """随机森林"""

    # 1.获取数据
    data = pd.read_csv('http://biostat.mc.vanderbilt.edu/wiki/pub/Main/DataSets/titanic.txt')
    # print(data)
    # 2.处理数据
    # 分割数据,从data中获取X，y
    y = data['survived']
    X = data[['pclass', 'age', 'sex']]
    # print(X,y)
    # 缺失值处理·
    X['age'].fillna(X['age'].mean(), axis=0, inplace=True)  # inplace改掉原来X的值
    # i = Imputer(missing_values='NaN',strategy='mean',axis=0)
    # age = i.fit_transform(X['age'],inplace = True)
    # print(age)
    # 数据划分
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25,random_state=1)
    # print(X_train)

    # 3.特征工程
    # 特征中有字符串也有数值，用字典特征抽取
    dict = DictVectorizer()
    # 由于多个字典，fit_transform括号内[{}],将训练特征转换成列表套字典的形式
    X_train = X_train.to_dict(orient='records')  # records : list like :[{column -> value}, ... , {column -> value}]
    X_test = X_test.to_dict(orient='records')
    X_train = dict.fit_transform(X_train)
    X_test = dict.transform(X_test)

    # 4.选择估计器，训练模型 --随机森林
    rfc = RandomForestClassifier(n_estimators=15) #n_estimators：森林里树木的数量
    rfc.fit(X_train,y_train)
    y_predict = rfc.predict(X_test)
    score = rfc.score(X_test,y_test)
    # print('预测的结果为：', y_predict)
    print('使用随机森林的精准度为：', score)
    # #使用网格搜索优化参数
    gs = GridSearchCV(rfc,param_grid={'n_estimators':[5,10,15,20,25,30]},cv=4)
    gs.fit(X_train,y_train)
    y_predict = gs.predict(X_test)
    print('使用随机森林并网格搜索优化参数后的精准度为：', gs.score(X_test, y_test))
    print('在交叉验证中得到的最好结果：', gs.best_score_)
    # print('每次交叉验证的结果：', gs.cv_results_)
    print('最好的参数模型', gs.best_estimator_)
    #
    # ret = classification_report(y_test,y_predict)
    # print('分类模型的报告为：', ret)

if __name__ == '__main__':
    decision_tree()
    random_forest()