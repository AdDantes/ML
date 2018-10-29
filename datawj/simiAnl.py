from gensim import corpora,models,similarities
import jieba
from time import time


#二.分词
#获取第一个新闻文本并分词

def sim():
    doc1 = open('ljm.txt','r+',encoding='utf8').read()
    w1_list = jieba.cut(doc1)
    text1 = ''
    for word1 in w1_list:
        text1+=word1+' '
    #获取第二个新闻文本并分词
    doc2 = open('dm.txt','r+',encoding='utf8').read()
    w2_list = jieba.cut(doc2)
    text2 = ''
    for word2 in w2_list:
        text2+=word2+' '#词间加空格隔开

    doc3 = open('doc3.txt',encoding='utf8').read()
    w3_list = jieba.cut(doc3)
    text3 = ''
    for i in w3_list:
        text3+=i+' '


    docs = [text1,text2,text3]#分词后的新闻文本字符串
    words_list= [[word for word in doc.split()] for doc in docs]#将各文本中的词转成列表形式


    #三.统计词频
    from collections import defaultdict
    freq = defaultdict(int)
    for text in words_list:
        for word in text:
            freq[word]+=1

    #四.去除低频词（可选）
    words_list = [[word for word in text if freq[word]>25] for text in words_list]

    #五.通过语料库构建词典
    dict = corpora.Dictionary(words_list)


    #六. 加载要对比的文档
    # doc4 = open('C:\\Users\Administrator\Desktop\ML\数据挖掘\gcd.txt',encoding='utf8').read()
    doc4 = '美国总统的女儿是伊万卡'
    text4 = jieba.cut(doc4)
    doc3 = ''
    for i in text4:
        doc3+=i+' '

    #七.将要对比的文档通过doc2bow转化为稀疏向量
    new_vec = dict.doc2bow(doc3.split())
    #八.构建新的语料库
    corpus=[dict.doc2bow(text) for text in words_list]
    # corpora.MmCorpus.serialize('6562.txt',corpus)
    #九.将新语料库通过tfidfmodel进行处理，得到tfidf
    tfidf=models.TfidfModel(corpus)
    #十.通过token2id得到特征数
    featureNum=len(dict.token2id.keys())
    #十一.稀疏矩阵相似度，从而建立索引
    index = similarities.SparseMatrixSimilarity(tfidf[corpus], num_features=featureNum)
    sims=index[tfidf[new_vec]]
    return sims

if __name__ == '__main__':
    start_time = time()
    sim()
    end_time = time()
    print('共用时:{}'.format(end_time-start_time))
