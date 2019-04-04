import sys

cur_item=None
token_score_list = []
for line in sys.stdin:
    ss = line.strip().split('\t')
    item = ss[0]
    token = ss[1]
    score = ss[2]
    if not cur_item:
        cur_item = item
    if item != cur_item:
        for tuple in token_score_list:
            pass
    token_score_list.append((token,score))
