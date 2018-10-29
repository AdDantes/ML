from gensim import corpora,models,similarities
import jieba
from time import time
from collections import defaultdict


class simAnl():

    def __init__(self):
        self.filename = 'D:\project\datawj\\' #文本绝对路径
        self.path1 = 'ljm.txt'
        self.path2 = 'dm.txt'
        self.path3='doc3.txt'
        self.new_path ='gcd.txt'

    def cut_word(self,path):
        """
        将文本分词
        :param path: 文本相对路径
        :return: 分词后的文本(str)
        """
        doc = open(self.filename+path,'r+',encoding='utf8').read()
        w_list = jieba.cut(doc)
        text = ''
        for word in w_list:
            text+=word+' '
        return text


    def to_list(self,text1,text2,text3):
        """
        将待对比文本转化文list并添加至同一列表中
        :param text1: 文本1
        :param text2: 文本2
        :param text3: 文本3
        :return: 包含所有文本的list
        """
        docs = [text1,text2,text3]#分词后的新闻文本字符串
        words_list= [[word for word in doc.split()] for doc in docs]#将各文本中的词转成列表形式
        return words_list


    def tf(self,words_list):
        """
        统计词频,去除低频词
        :param words_list: 包含所有文本的list
        :return: 去除低频词后的list
        """
        freq = defaultdict(int)
        for text in words_list:
            for word in text:
                freq[word]+=1
        drop_low = [[word for word in text if freq[word]>25] for text in words_list]
        dict = corpora.Dictionary(drop_low) #通过语料库构建词典
        return drop_low,dict


    def load_new_doc(self,new_path,dict,drop_low):
        """
 
        :param new_path: 新文本路径
        :param dict: 语料库词典
        :param drop_low: 词汇列表
        :return: 对比结果(list)
        """
        new_text = self.cut_word(self.new_path)
        #加载要对比的文档,将要对比的文档通过doc2bow转化为稀疏向量
        new_vec = dict.doc2bow(new_text.split())
        corpus=[dict.doc2bow(text) for text in drop_low] #构建新的语料库
        # # corpora.MmCorpus.serialize('6562.txt',corpus)
        tfidf=models.TfidfModel(corpus)# 将新语料库通过tfidfmodel进行处理，得到tfidf
        featureNum=len(dict.token2id.keys())#通过token2id得到特征数
        index = similarities.SparseMatrixSimilarity(tfidf[corpus], num_features=featureNum)#稀疏矩阵相似度，从而建立索引
        sims=index[tfidf[new_vec]]
        return sims

    def run(self):
        text1 = self.cut_word(self.path1)
        text2 = self.cut_word(self.path2)
        text3 = self.cut_word(self.path3)
        words_list = self.to_list(text1,text2,text3)
        drop_low,dict = self.tf(words_list)
        sims = self.load_new_doc(self.new_path,dict,drop_low)
        return sims

if __name__ == '__main__':
    simAnl = simAnl()
    start = time()
    sims = simAnl.run()
    end = time()
    print(sims)
    print('Use{}sec'.format(end-start))


