# -*- coding: utf-8 -*-
import scrapy
import json
from uuid import uuid4
from copy import deepcopy
import re


class LagouSpider(scrapy.Spider):
    name = 'lagou'
    allowed_domains = ['lagou.com']
    start_urls = ['http://lagou.com/']
    pn = 1
    kd = '爬虫工程师'
    first = 'true'

    def start_requests(self):
        return [scrapy.FormRequest('https://www.lagou.com/jobs/positionAjax.json?',
                                   formdata={'first': self.first, 'pn': str(self.pn), 'kd': self.kd},
                                   cookies={'JSESSIONID': uuid4(), 'user_trace_token': uuid4()},
                                   )]

    def parse(self, response):
        try:
            item = {}
            resp_dict = json.loads(response.text)
            positionResult = resp_dict['content']['positionResult']
            position_list = positionResult['result']
            for position in position_list:
                item['workYear'] = position['workYear']
                item['createTime'] = position['createTime']
                item['salary'] = position['salary']
                item['education'] = position['education']
                item['city'] = position['city']
                item['positionName'] = position['positionName']
                item['search_name'] = self.kd
                item['positionId'] = position['positionId']
                detail_url = 'https://www.lagou.com/jobs/{}.html'.format(item['positionId'])
                yield scrapy.Request(detail_url, callback=self.parse_detail,
                                     cookies={'JSESSIONID': uuid4(), 'user_trace_token': uuid4()},
                                     meta={'item': deepcopy(item)})
        except:
            pass

        finally:
            if self.pn < 30:
                self.pn += 1
                print('正在抓取第{}页'.format(self.pn))
                self.first = 'false'
                yield scrapy.FormRequest('https://www.lagou.com/jobs/positionAjax.json?needAddtionalResult=false',
                                         formdata={'first': self.first, 'pn': str(self.pn), 'kd': self.kd},
                                         cookies={'JSESSIONID': uuid4(), 'user_trace_token': uuid4()})

    def parse_detail(self, response):
        item = response.meta['item']
        desp = response.xpath('//dd[@class="job_bt"]/div/p/text()').extract()
        j = 0
        item['work_duty'] = ''
        global i
        for i in range(len(desp)):

            desp[i] = desp[i].replace('\xa0', ' ')
            if desp[i][0].isdigit():
                if j == 0:
                    desp[i] = desp[i][2:].replace('、', ' ')
                    desp[i] = re.sub('[；;.0-9。]', '', desp[i])
                    item['work_duty'] = item['work_duty'] + desp[i] + '/'
                    j += 1
                elif desp[i][0] == '1' and not desp[i][1].isdigit():
                    break
                else:
                    desp[i] = desp[i][2:].replace('、', ' ')
                    desp[i] = re.sub('[；;.0-9。]', '', desp[i])
                    item['work_duty'] = item['work_duty'] + desp[i] + '/'

        m = i
        j = 0
        item['work_requirement'] = ''
        for i in range(m, len(desp)):
            desp[i] = desp[i].replace('\xa0', ' ')
            if desp[i][0].isdigit():
                if j == 0:
                    desp[i] = desp[i][2:].replace('、', ' ')
                    desp[i] = re.sub('[；;.0-9。]', '', desp[i])
                    item['work_requirement'] = item['work_requirement'] + desp[i] + '/'
                    j += 1
                elif desp[i][0] == '1' and not desp[i][1].isdigit():
                    break
                else:
                    desp[i] = desp[i][2:].replace('、', ' ')
                    desp[i] = re.sub('[；;.0-9。]', '', desp[i])
                    item['work_requirement'] = item['work_requirement'] + desp[i] + '/'
        print(item)
        yield item
        print("-----------------------------")
