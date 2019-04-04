# _*_ coding:utf-8 _*_
import jieba
import jieba.posseg
import jieba.analyse

idf_file = './idf.txt'
input_file = './merge_data.data'
out_file = './data_for_cb.data'
ofile = open(out_file, 'w')

idf_token = {}
with open(idf_file, 'r',encoding='utf-8') as f:
    for line in f:
        token, score = line.strip().split(' ')

        idf_token[token] = score

# 权重占比
Ratio_name = 0.7
Ratio_desc = 0.4
Ratio_tag = 0.01
with open(input_file, 'r',encoding='utf-8') as f:
    item_set = set()
    for line in f:
        ss = line.strip().split('	')
        if len(ss)!=13:
        	continue
        # 用户行为
        userid = ss[0]
        itemid = ss[1]
        watch_len = ss[2]
        hour = ss[3]
        # 用户画像
        gender = ss[4]
        age = ss[5]
        salary = ss[6]
        user_location = ss[7]
        # 物品元数据
        name = ss[8].strip()
        desc = ss[9].strip()
        total_timelen = ss[10]
        item_location = ss[11]
        tags = ss[12].strip()

        # item去重
        if itemid not in item_set:
            item_set.add(itemid)
        else:
            continue

        token_dict = {}
        # 对name分词-->token:score
        for a in jieba.analyse.extract_tags(name, withWeight=True):
            token = a[0]
            score = float(a[1])
            print(token, score)
            if token in token_dict:
                token_dict[token] += score * Ratio_name
            else:
                token_dict[token] = score * Ratio_name

        # 对desc分词-->token:score
        for a in jieba.analyse.extract_tags(desc, withWeight=True):
            token = a[0]
            score = float(a[1])
            if token in token_dict:
                token_dict[token] += score * Ratio_desc
            else:
                token_dict[token] = score * Ratio_desc

        # tags-->token:score
        tag_list = tags.strip().split(',')
        for tag in tag_list:
            if tag not in idf_token:
                continue
            else:
                if tag in token_dict:
                    token_dict[tag] += float(idf_token[tag]) * Ratio_tag
                else:
                    token_dict[tag] = float(idf_token[tag]) * Ratio_tag

        for k, v in token_dict.items():
            token = k.strip()
            score = str(v)
            ofile.write(','.join([token, itemid, score]))
            ofile.write('\n')
