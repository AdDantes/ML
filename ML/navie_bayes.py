from sklearn import datasets
from sklearn.model_selection import train_test_split
import pandas as pd
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import classification_report


def load_data():
    #获取sklearn中的小数据量的鸢尾花数据
    iris = datasets.load_iris()
    # 获取数据中的特征数据
    print('特征数据为：',iris.data)
    print('标签数据为：',iris.target)  #目标数据
    print('描述信息为：',iris.DESCR)
    print('特征名称为：',iris.feature_names)
    print('标签名称为：',iris.target_names)

def load_news():
    news = datasets.fetch_20newsgroups(subset='all')  #subset : 'train' or 'test', 'all',切分数据集
    # print(news)
    #参数test_size:指定划分数据集后测试集占比，一般设定test_size， 还可以设置train_size
    #返回值四个参数
    #1.X_train：训练的特征数据，对于特征来说一般是多个多维数据用大写
    #2.X_test：测试的特征数据
    #3.y_train:训练的目标数据
    #4.y_test:测试的目标数据

    #数据切割
    X_train,X_test,y_train,y_test = train_test_split(news.data,news.target,test_size=0.25)
    print(y_train)

def navie_bayes():
#     利用朴素贝叶斯实现二十组新闻数据分类

    # 1.获取数据
    news = datasets.fetch_20newsgroups(subset='all')
    #2.划分数据
    X_train, X_test, y_train, y_test = train_test_split(news.data,news.target,test_size=0.25,random_state=1)
    #3.特征工程（tf-idf处理特征）
    tfidf = TfidfVectorizer(f
    X_train = tfidf.fit_transform(X_train)
    X_test = tfidf.transform(X_test)
    #4.选择估计器
    mn = MultinomialNB(alpha=0.1)
    mn.fit(X_train,y_train)
    #5.预测数据
    y_predict = mn.predict(X_test)
    #6.评测数据
    score = mn.score(X_test,y_test)
    print('预测的结果为：', y_predict)
    print('精准度为：', score)
    ret = classification_report(y_test,y_predict)
    print('分类模型的报告为：',ret)


if __name__ == '__main__':
    # test()
    # load_data()
    # load_news()
    navie_bayes()