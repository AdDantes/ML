import sys
import math


input_file = 'D:\GIT\\recommend\data_for_cb.data'
output1 = 'output1.txt'
output2 = 'output2.txt'

def ti_map():
    with open(input_file,'r') as f:
        for line in f:
                ss = line.strip().split(',')
                if len(ss)!=3:
                    continue
                token,item,score = ss
                print('%s\t%s\t%s'%(item,token,score))
                with open(output1,'a') as f:
                    f.write('%s\t%s\t%s'%(item,token,score))
                    f.write('\n')

def ui_reduce():
    """
    score归一化
    :return:
    """
    cur_item = None
    token_score_list = []

    with open(output1,'r') as f:
        for line in f:
            item, token, score = line.strip().split('\t')
            if not cur_item:
                cur_item = item
            if item != cur_item:
                sum = 0
                for tuple in token_score_list:
                    (t,s) = tuple
                    sum+=pow(float(s),2)#求同一item不同token：score平方和
                sum = math.sqrt(sum)#再开方
                for tuple in token_score_list:
                    (t,s) = tuple
                    print('%s\t%s\t%s'%(t,cur_item,float(s)/sum))
                    with open(output2, 'a') as f:
                        f.write('%s\t%s\t%s'%(t,cur_item,float(s)/sum))
                        f.write('\n')
                token_score_list = []
                cur_item = item
            token_score_list.append((token, score))
        sum = 0
        for tuple in token_score_list:
            (t, s) = tuple
            sum += pow(float(s), 2) #求所有平方和
        sum = math.sqrt(sum) #开方
        for tuple in token_score_list:
            (t, s) = tuple
            print('%s\t%s\t%s' % (t, cur_item, float(s) / sum))
            with open(output2, 'a') as f:
                f.write('%s\t%s\t%s' % (t, cur_item, float(s) / sum))
                f.write('\n')


def ii_pair_map():
   with open(output2,'r') as f:
       for line in f:
           token,item,score = line.strip().split('\t')
           print('%s\t%s\t%s' % (token,item,score))


def ii_pair_reduce():
    cur_token = None
    item_score_list = []
    with open(output2,'r') as f:
        for line in f:
            token,item,score = line.strip().split('\t')
            if not cur_token:
                cur_token = token
            if token!=cur_token:
                for i in range(0,len(item_score_list)-1):
                    for j in range(i+1,len(item_score_list)):
                        item_a,score_a = item_score_list[i]
                        item_b,score_b = item_score_list[j]
                        print("%s\t%s\t%s"%(item_a,item_b,score_a*score_b))
                        print("%s\t%s\t%s" % (item_b ,item_a, score_a * score_b))
                item_score_list = []
                cur_token = token
            item_score_list.append((item,score))
        for i in range(0, len(item_score_list) - 1):
            for j in range(i + 1, len(item_score_list)):
                item_a, score_a = item_score_list[i]
                item_b, score_b = item_score_list[j]
                print("%s\t%s\t%s" % (item_a, item_b, score_a * score_b))
                print("%s\t%s\t%s" % (item_b, item_a, score_a * score_b))

def sum_map():
    for line in sys.stdin:
        i_a,i_b,s = line.strip().split('\t')
        print("%s\t%s" % (i_a + "" + i_b, s))

def sum_reduce():
    pass
if __name__ == '__main__':
    ii_pair_map()