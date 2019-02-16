#!/usr/bin/env python
# coding: utf-8

# File Name: 推荐系统-基于图的推荐算法.py
# Author   : john
# Mail     : keyue654321@126.com
# Created Time: 2019/1/7 11:17
# Describe : 基于图的推荐算法

def load_data(file_path):
    records = []
    f = open(file_path, "r", encoding="utf-8")
    for line in f:
        info = line.strip().split("\t")
        records.append(info)
	f.close()
    
    return records

def calc_user_item(records):
    user_item = dict()
    item_user = dict()
    
    for user, item in records:
        user_item.setdefault(user, dict())
        user_item[user].setdefault(item, 0)
        user_item[user][item] = 1   # 用户顶点
        
        item_user.setdefault(item, dict())
        item_user[item].setdefault(user, 0)
        item_user[item][user] = 1   # 物品顶点  
    
    #print("物品-用户倒排列表: ", user_item)
    return user_item, item_user

def initGraph(user_item, item_user):
    user_item_tag = dict()
    
    user_item_tag = dict(user_item, **item_user)

    return user_item_tag

# G: 二分图     alpha：随机游走概率     root: 初始节点     max_step: 最大游走步数
def PersonalRank(G, alpha, root, max_step):
    rank = dict()
    rank = {x:0 for x in G.keys()}
    rank[root] = 1
    
    for k in range(max_step):
        tmp = {x:0 for x in G.keys()}
        for i, ri in G.items():
            for j, wij in ri.items():
                if j not in tmp:
                    tmp[j] = 0
                
                tmp[j] += 0.6 * rank[i] / (1.0 * len(ri))
                if j == root:
                    tmp[j] += 1 - alpha

        #tmp[root] += 1 - alpha
        rank = tmp
        
    rec = sorted(rank.items(),key = lambda x:x[1],reverse = True)   # 将推荐歌曲按兴趣度排名
    
    return rec

def Recommend(user, rank, user_item):
    rec = []
    for music in rank:
        data = music[0]
        rec.append(data)
        
    for u, v in user_item.items():
        for i in rec:
            if i == u:
                rec.remove(i)

    for u, v in user_item[user].items():
        for i in rec:
            if i == u:
                rec.remove(i)
                    
    return rec            

if __name__ == '__main__':
    user = "A"
    file_path = u"./data/基于图的推荐数据.txt"
    records = load_data(file_path)
    print("数据集: ", records)
    user_item, item_user = calc_user_item(records)
    print("用户顶点: ", user_item)
    print("物品顶点: ", item_user)
    G = initGraph(user_item, item_user)
    print("G: ", G)
    rank = PersonalRank(G, 0.85, user, 100)
    print(rank)
    rec = Recommend(user, rank, user_item)
    print("推荐物品: ", rec)