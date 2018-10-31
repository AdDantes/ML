from pymongo import MongoClient
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction import DictVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.ensemble import RandomForestClassifier
import re
import math


"""职业薪资预测"""
client = MongoClient()
db = client['zhaopin']
position = '爬虫工程师'
lagou = db.lagou
lagou_data = lagou.find({'search_name': position})
data = pd.DataFrame(list(lagou_data))

del data['_id']

print(data['salary'])
salary = []
for i in data['salary']:
    salary_list = re.findall('\d+', i)
    if len(salary_list) > 1:
        ave = (int(salary_list[0]) + int(salary_list[1])) / 2

    else:
        ave = int(salary_list[0])

    ave_salary = math.ceil(ave)
    if ave_salary < 5:
        j = '5k以下'
    elif ave_salary in range(5, 10):
        j = '5k-10k'
    elif ave_salary in range(10, 20):
        j = '10k-20k'
    elif ave_salary in range(20, 30):
        j = '20k-30k'
    elif ave_salary in range(30, 40):
        j = '30k-40k'
    else:
        j = '40k以上'
    salary.append(j)

print(data.columns)
x = data[['city','education','search_name','workYear']]
y = salary
# print(x)

x_train,x_test,y_train,y_test = train_test_split(x,y,test_size=0.1)
dv = DictVectorizer()
x_train = x_train.to_dict(orient='records')
# x_test = {'city':'北京', 'education':'本科','search_name':'数据挖掘工程师', 'workYear':'1-3年'}
x_test = x_test.to_dict(orient = 'records')
x_train = dv.fit_transform(x_train)
x_test = dv.transform(x_test)

nb = MultinomialNB()
nb.fit(x_train,y_train)
pre = nb.predict(x_test)
score = nb.score(x_test,y_test)
print(pre)
print(score)

