import numpy as np
import pandas as pd
import jieba

# http://blog.csdn.net/eastmount/article/details/50323063
# http://blog.csdn.net/eastmount/article/details/50256163
# http://blog.csdn.net/lsldd/article/details/41542107
"""舆情分析"""
####################################
#         第一步 读取数据及分词
#
data = pd.read_excel("D:\\project\\datawj\\pinglun.xlsx", encoding='gbk')
print(data)

# 取表中的第1列的所有值
print("获取第一列内容")
col = data.iloc[:, 0]

# 取表中所有值
arrs = col.values

# 去除停用词
stopwords = {}.fromkeys(['，', '。', '！', '这', '我', '非常'])
# with open('stopwords.txt','r') as f:
#     stopwords = f.read()
print(u"\n中文分词后结果:")
corpus = []
for a in arrs:
    # print a
    seglist = jieba.cut(a, cut_all=False)  # 精确模式
    final = ''
    for seg in seglist:
        # seg = seg.encode('utf-8')
        if seg not in stopwords:  # 不是停用词的保留
            final += seg
    seg_list = jieba.cut(final, cut_all=False)
    output = ' '.join(list(seg_list))  # 空格拼接
    print(output)
    corpus.append(output)
print(corpus)

####################################
#         第二步 计算词频
#
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.linear_model import LogisticRegression

vectorizer = CountVectorizer()  # 将文本中的词语转换为词频矩阵
X = vectorizer.fit_transform(corpus)  # 计算个词语出现的次数
word = vectorizer.get_feature_names()  # 获取词袋中所有文本关键词
for w in word:  # 查看词频结果
    print(w)
print('')
print(X.toarray())

####################################
#         第三步 数据分析
#
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import precision_recall_curve
from sklearn.metrics import classification_report

# 使用前8行数据集进行训练，最后两行数据集用于预测
print(u"\n\n数据分析:")
X = X.toarray()
x_train = X[:8]
x_test = X[8:]
# 1表示好评 0表示差评
y_train = [1, 1, 1, 0, 1, 0, 0, 1]
y_test = [0, 0]
# 调用MultinomialNB分类器
clf = LogisticRegression().fit(x_train, y_train)
pre = clf.predict(x_test)
print(u"预测结果:", pre)
print(u"真实结果:", y_test)

from sklearn.metrics import classification_report

print(classification_report(y_test, pre))
