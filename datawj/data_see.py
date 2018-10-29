import pandas as pda
import numpy as np
import matplotlib.pylab as pyl

f = open('C:\\Users\Administrator\Desktop\爬虫\爬虫与数据分析视频课程\源码\源码\第5周\hexun.csv','rb')
data = pda.read_csv(f)
# print(data.values[2])
data2 = data.T #转置
y1 = data2.values[3]
x1 = data2.values[4]
x2 = data2.values[0]
pyl.plot(x2,y1,'*y')
pyl.show()
