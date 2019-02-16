#!/usr/bin/env python
# coding: utf-8

# File Name: 推荐算法-基于时间上下文的UserCF算法.py
# Author   : john
# Mail     : keyue654321@126.com
# Created Time: 2019/1/7 11:17
# Describe : 基于时间上下文的UserCF算法

import math
import time, datetime
from collections import defaultdict
from operator import itemgetter


def load_data(filePath):
    f = open(filePath, "r", encoding="utf-8")
    dataSet = {}

    for line in f:
        userId, songName, timestamp = line.strip().split(",")
        dataSet.setdefault(userId, {})
        timeArray = time.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
        timeStamp = int(time.mktime(timeArray))  # 将日期转为时间戳
        
        dataSet[userId][songName] = timeStamp
	f.close()

    return dataSet

def UserSimilarity(train):
    # build inverse table for item_users
    item_users = dict()
    for u, items in train.items(): # 用户
        for i, tui in items.items(): # 歌曲，时间
            item_users.setdefault(i, {})
            item_users[i][u] = tui
        
    C = dict()
    N = dict()
    for i, users in item_users.items(): # 歌曲
        for u, tui in users.items(): # 用户，时间
            N.setdefault(u, 0)
            N[u] += 1   # 统计喜欢某首歌曲的用户数量
            for v, tvi in users.items():
                if u == v:
                    continue
                C.setdefault(u, {})           
                C[u].setdefault(v, 0)
                C[u][v] += 1 / (1 + 0.85 * abs(tui - tvi))
      
    #print("用户喜欢音乐衰减: ", C)
    #print("--------------------------------------------------------------------------------")

    W = dict()
    for u, related_users in C.items():
        for v, cuv in related_users.items():
            W.setdefault(u, {})           
            W[u].setdefault(v, 0)       
            W[u][v] = cuv / math.sqrt(N[u] * N[v])
    
    #print("用户相似度: ", W)
    #print("--------------------------------------------------------------------------------")
    
    return W

def Recommend(train, user, W, K, T):
    rank = dict()
    interacted_items = train[user]
    
    for v, wuv in sorted(W[user].items(), key=itemgetter(1), reverse=True)[0:K]:  # 寻找前K个相似用户
        for i, tvi in train[v].items():
            if i in interacted_items:
                continue
            rank.setdefault(i, 0)  
            rank[i] += wuv / (1 + 0.85 * (T - tvi))
      
    for i in list(rank.keys()):  # 删除用户已经听过的歌曲
        for j in list(interacted_items.keys()):
            if i == j:
                del rank[i]
                
    return rank

if __name__ == '__main__':
    file_path = "./data/基于时间的推荐数据.txt"
    
    dataSet = load_data(file_path)
    #print("数据集: ", dataSet)
    #print("----------------------------------------------------------------------------------------------------------")
    
    W = UserSimilarity(dataSet)  # 计算物品相似度
    #print("用户相似度: ", W)
    #print("----------------------------------------------------------------------------------------------------------")
    
    t = "2019-02-14 09:08:42"
    timeArray = time.strptime(t, "%Y-%m-%d %H:%M:%S")
    t0 = int(time.mktime(timeArray))  # 将日期转为时间戳
    
    lastRank = Recommend(dataSet, "18576636296", W, 2, t0)
    print("为用户推荐音乐列表: ", list(lastRank.keys()))




