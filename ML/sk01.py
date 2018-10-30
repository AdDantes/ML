from sklearn.feature_extraction import DictVectorizer
from sklearn.feature_extraction.text import CountVectorizer,TfidfVectorizer
from sklearn.preprocessing import MinMaxScaler,StandardScaler,Imputer
from sklearn.feature_selection import VarianceThreshold
from sklearn.decomposition import PCA
import jieba
import numpy as np

def dict_vec():
    # 字典特征抽取
    data = [{'name':'北京','temp':100},
            {'name': '上海', 'temp': 60},
            {'name': '厦门', 'temp': 30},
            {'name': '深圳', 'temp': 80},]
    # 利用DictVectorizer进行字典特征抽取
    # 1.创建字典特征抽取对象
    dict = DictVectorizer(sparse=False)
    # 2.进行特征抽取，创建标准转换数据
    data = dict.fit_transform(data)
    print(data)
    # 获取特征名称
    names = dict.get_feature_names()
    print(names)

def count_vec():
#     进行文本特征值化
    data = ['life is short,i love python','life is too long, i dislike python']
    cv = CountVectorizer()  #通过空格进行区分
    data = cv.fit_transform(data)
    print(cv.get_feature_names())
    # 如果返回结果是一个稀疏矩阵，但Vectorizer中没有设置不显示稀疏矩阵的参数，调用toarray方法即可
    print(data.toarray())

def cut():
    con1 = jieba.cut('人人车')
    con2 = jieba.cut('土地是以它的肥沃和收获而被估价的；才能也是土地，不过它生产的不是粮食，而是真理。如果只能滋生瞑想和幻想的话，即使再大的才能也只是砂地或盐池，那上面连小草也长不出来的。')
    con3 = jieba.cut('我需要三件东西：爱情友谊和图书。然而这三者之间何其相通！炽热的爱情可以充实图书的内容，图书又是人们最忠实的朋友。')
    content1 = changeTostr(con1)
    content2 = changeTostr(con2)
    content3 = changeTostr(con3)
    return content1,content2,content3

def changeTostr(con):
    content = ''
    for i in con:
        content+=i+' ' #将分后的词加空格组成句子
    return content

def Chinese_count_vec():
    content1,content2,content3 = cut()
    # stop_words：进行文本特征处理过程中不要的词
    cv = CountVectorizer(stop_words=['三件'])
    # 注意，传入的一定是列表数据
    data = cv.fit_transform([content1,content2,content3])
    print(cv.get_feature_names())
    print(data.toarray())

def tf_idf_vec():
    """TF_IDF主要思想：如果某个词或短语在一篇文章中出现的频率高，并且在其他文章中很少出现,
    则认为此词或短语具备很好的类别区分能力，适合用来分类。
    TF_IDF作用：用以评估一个词对于一个文件集或语料库中的其中一个文件的重要程度"""
    tf_idf = TfidfVectorizer()
    content1, content2, content3 = cut()
    data = tf_idf.fit_transform([content1,content2,content3])
    print(tf_idf.get_feature_names())
    print(data.toarray())

def min_max():
    #利用归一化处理数据
    data = [[90,20,60,40],
            [25,70,34,25],
            [45,33,21,67],
            [45,12,65,15]]
    mm = MinMaxScaler()
    data = mm.fit_transform(data)
    print(data)
    data = mm.inverse_transform(data)
    print(data)

def stantard_scaler():
#     利用标准化处理数据
    data = [[1.,-1.,3.],
            [2.,4.,2.],
            [4.,6.,-1.]]

    ss = StandardScaler()
    data = ss.fit_transform(data)
    print(data)
    data = ss.inverse_transform(data)
    print(data)

def nan():
    #缺失值的处理，默认填充列的平均值
    data = [[1,2],
            [np.nan,3],
            [7,6]]
    i = Imputer(missing_values='NaN')
    data = i.fit_transform(data)
    print(data)

def var():
    #特征选择，去掉方差值小的特征,去掉特征方差值小于threshold的那些特征
    data = [[0,2,0,3],
            [0,1,4,3],
            [0,1,1,3]]

    va = VarianceThreshold(threshold=0.5)
    data = va.fit_transform(data)
    print(data)
    data = va.inverse_transform(data)
    print(data)

def pca():
    #利用pca技术进行数据降维处理
    data = [[2,8,4,5],
            [6,3,0,8],
            [5,4,9,1]]
    p = PCA()
    data = p.fit_transform(data)
    print(data)



if __name__ == '__main__':
    dict_vec()
    count_vec()
    # cut()
    # Chinese_count_vec()
    # tf_idf_vec()
    # min_max()
    # stantard_scaler()
    # nan()
    # var()
    pca()