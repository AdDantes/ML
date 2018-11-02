import requests
import json
from pprint import pprint

data = requests.post('https://www.quandashi.com/brand-order/get-zntype',data={'pid':'0'}).content.decode("gb2312")
data = json.loads(data)
data = data['msg']
item = {}
for i in data:
    # print(i)
    item['ftitle'] = i['ftitle']
    fzid = i['fzid']
    resp = requests.post('https://www.quandashi.com/brand-order/get-zntype',data ={'pid':fzid}).content.decode("gb2312")
    second_class = json.loads(resp)
    msg_list = second_class['msg']
    for msg in msg_list:
        item['stitle'] = msg['ftitle']
        fzid = msg['fzid']
        resp = requests.post('https://www.quandashi.com/brand-order/get-cg-type',data={'pid':fzid}).content.decode()
        third_class = json.loads(resp)
        item['data'] = third_class['msg']
        print(str(item))
        with open('quandashi.json','a',encoding='utf8') as f:
            f.write(str(item)+'\n')
        # m_list = third_class['msg']
        # for msg in m_list:
        #     print(msg)


