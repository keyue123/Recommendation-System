#!/usr/bin/env python
# coding: utf-8

# File Name: 推荐算法-时间上下文的ItemCF算法.py
# Author   : john
# Mail     : keyue654321@126.com
# Created Time: 2019/1/7 11:17
# Describe : 时间上下文的ItemCF算法

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

def ItemSimilarity(dataSet, alpha):
    C = dict()
    N = dict()
    for u, items in dataSet.items():
        for i, tui in items.items():
            N.setdefault(i, 0)
            N[i] += 1   # 统计歌曲数量
            for j, tuj in items.items():
                if i == j:
                    continue
                C.setdefault(i, {})
                C[i].setdefault(j, 0)
                C[i][j] += 1 / (1 + alpha * abs(tui - tuj))   # 时间衰减函数

    #print("歌曲间兴趣衰减: ", C)
    #print("----------------------------------------------------------------------------------------------------------")
    
    W = dict()
    for i, related_items in C.items():
        for j, cij in related_items.items():
            W.setdefault(i, {})
            W[i].setdefault(j, 0)
            W[i][j] = cij / math.sqrt(N[i] * N[j])  # 歌曲相似度
    
    #print("歌曲相似度: ", W)
    return W

def Recommend(dataSet, user, W, K, t0):
    rank = dict()
    ru = dataSet[user]
    print("用户"+user+"喜欢歌曲集合: ", ru)

    for i, pi in ru.items():  # 歌曲   时间戳
        print("《" + i + "》与其他歌曲相似度排名:", sorted(W[i].items(), key=itemgetter(1), reverse=True))
        for j, wj in sorted(W[i].items(), key=itemgetter(1), reverse=True)[0:K]:  # 相似度排名，wj相似度, 每首歌曲找K个相似的歌曲
            if j in ru.items():   # j歌曲名，pi时间戳
                continue
            rank.setdefault(j, 0)
            rank[j] += pi * wj / (1 + 0.85 * (t0 - pi))

    for i in list(ru.keys()):  # 删除用户本已经感兴趣的歌曲
        for j in list(rank.keys()):
            if i == j:
                del rank[j]
    
    return rank

if __name__ == '__main__':
    file_path = u"./data/基于时间的推荐数据.txt"
    
    dataSet = load_data(file_path)
    #print("数据集: ", dataSet)
    #print("----------------------------------------------------------------------------------------------------------")
    
    W = ItemSimilarity(dataSet, 0.85)  # 计算物品相似度
    #print("歌曲相似度: ", W)
    #print("----------------------------------------------------------------------------------------------------------")
    
    t = "2019-02-14 09:08:42"
    timeArray = time.strptime(t, "%Y-%m-%d %H:%M:%S")
    t0 = int(time.mktime(timeArray))  # 将日期转为时间戳
    
    lastRank = Recommend(dataSet, "18576636296", W, 2, t0)
    print("为用户推荐音乐列表: ", list(lastRank.keys()))
    print("----------------------------------------------------------------------------------------------------------")