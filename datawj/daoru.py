import pandas as pda


#导入csv数据
f = open('C:\\Users\Administrator\Desktop\爬虫\爬虫与数据分析视频课程\源码\源码\第5周\hexun.csv','rb')
web = pda.read_csv(f)
print(web.describe())
print(web.mean())
# print(web.sort_values(by='21'))
# print(web.sort_values(by='0'))

#导入excel数据
f = open('C:\\Users\Administrator\Desktop\爬虫\爬虫与数据分析视频课程\源码\源码\第5周\\abc.xls','rb')
abc = pda.read_excel(f)
# print(abc)

#导入html数据
f = open('C:\\Users\Administrator\Desktop\爬虫\爬虫与数据分析视频课程\源码\源码\第5周\\abc.html','rb')
# print(pda.read_html('https://book.douban.com'))

#导入文本数据
i = open('C:\\Users\Administrator\Desktop\爬虫\爬虫与数据分析视频课程\源码\源码\第5周\\abc.txt','rb')
# print(pda.read_table(i))
#