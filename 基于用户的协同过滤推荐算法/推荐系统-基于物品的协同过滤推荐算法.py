#!/usr/bin/env python
# coding: utf-8

# File Name: 推荐系统-基于物品的协同过滤推荐算法.py
# Author   : john
# Mail     : keyue654321@126.com 
# Created Time: 2019/1/7 11:17
# Describe : 基于物品的协同过滤音乐推荐系统


import math
from collections import defaultdict
from operator import itemgetter


def load_data(filePath):
    f = open(filePath, "r", encoding="utf-8")
    trainSet = {}
    len = 0
    for line in f:
        userId, songName, rating = line.strip().split(",")
        trainSet.setdefault(userId, {})
        trainSet[userId][songName] = rating
        len = len + 1
        if len > 10000:  # 取10000条数据
            break
	f.close()

    return trainSet

def calc_item_sim(dataSet):
    item_users = dict()
    for user, items in dataSet.items():
        for song in items:
            if song not in item_users:
                item_users[song] = set()
            item_users[song].add(user)
      
    #print("物品-用户倒排列表: ", item_users)
    return item_users

def item_similarity(userSet):
    C = dict()
    N = dict()
    for u, items in userSet.items():
        for i in items:
            N.setdefault(i, 0)
            N[i] += 1
            for j in items:
                if i == j:
                    continue
                C.setdefault(i, {})
                C[i].setdefault(j, 0)
                C[i][j] += 1

    #print("稀疏矩阵: ", C)
    W = dict()
    for i,related_items in C.items():
        for j, cij in related_items.items():
            W.setdefault(i, {})
            W[i].setdefault(j, 0)
            W[i][j] = cij / math.sqrt(N[i] * N[j])
    
    #print("物品相似度: ", W)
    return W

def recommend(user, train, W, K):
    pi = 1
    rank = dict()
    interacted_items = train[user]
    
    for item in interacted_items:
        #print(">>>>>>>>", item)
        related_item = []
        for user, score in W[item].items():
            related_item.append((user, score))
                    
        for j, v in sorted(related_item, key=itemgetter(1), reverse=True)[0:K]:
            if j in interacted_items:
                continue
            if j not in rank.keys():
                rank[j]=0
            rank[j] += pi * v
           
    return rank

if __name__ == '__main__':
    file_path = u"./data/协同过滤的推荐数据.csv"
    dataSet = load_data(file_path)
    #print(dataSet)
    userSet = calc_item_sim(dataSet)  # 对每部电影产生行为的用户列表
    itemSimi = item_similarity(dataSet)  # 计算物品相似度
    lastRank = recommend("0", dataSet, itemSimi, 3)
    print("为用户推荐音乐: ", lastRank)
