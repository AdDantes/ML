import requests
import pandas as pd


# iris = requests.get('https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data')
# with open('iris.csv','w') as f:
#     f.write(iris.text)
df = pd.read_csv('iris.csv',names=['sepal length','sepal width', 'petal length','petal width','class'])
# print(df['sepal length'])
#前三行，包含‘width’的所有列
# print(df.ix[:3,[x for x in df.columns if 'width' in x]])
#切片所有行，指定字段
print(df.ix[:,['sepal length', 'sepal width', 'petal length', 'petal width']])
print(df.iloc[:,4])
#列出单个字段
print(df['class'])
#列出所有字段名
print(df.columns) #返回值：Index(['sepal length', 'sepal width', 'petal length', 'petal width', 'class'], dtype='object')
#列出所有唯一类名
print(df['class'].unique())
#条件查询
print(df[df['class']=='Iris-setosa'])
#统计总样本数
print(df.count())
#统计过滤后单类样本数
print(df[df['class']=='Iris-setosa'].count())
#重置索引
virginica = df[df['class']=='Iris-virginica'].reset_index(drop=True)
# print(virginica)

#'Iris-setosa'类中'sepal width'>3.5的所有样本
print(df[(df['class']=='Iris-setosa')&(df['sepal width']>3.5)])
#描述性统计信息
print(df[df['class']=='Iris-setosa'].describe())
print(df['sepal length'].std())
#检查这些特征之间是否有任何相关性
print(df.corr())
# 系统按照类别对数据进行了划分，并且提供了每个特征的均值
print(df.groupby('class').mean())
# 每个类别完全的描述性统计信息
print(df.groupby('class').describe())
