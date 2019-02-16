#!/usr/bin/env python
# coding: utf-8

# File Name: 推荐系统-基于图的标签推荐算法.py
# Author   : john
# Mail     : keyue654321@126.com
# Created Time: 2019/1/7 11:17
# Describe : 基于图的标签推荐算法


from math import log
from operator import itemgetter
from collections import defaultdict


def load_data(file_path):
    records = []
    f = open(file_path, "r", encoding="utf-8")
    for line in f:
        info = line.strip().split("\t")
        records.append(info)
	f.close()
    
    return records

def user_vertex_cal(records):  # 建立物品-用户的倒排列表
    user_tag = dict()
    tag_user = dict()
    
    tag_music = dict()
    music_tag = dict()
    
    for user, music, tag in records:
        user_tag.setdefault(user, dict())
        user_tag[user].setdefault(tag, 0)
        user_tag[user][tag] = 1 # 用户顶点
        
        tag_user.setdefault(tag, dict())
        tag_user[tag].setdefault(user, 0)
        tag_user[tag][user] = 1  # 标签顶点
        
        tag_music.setdefault(tag, dict())
        tag_music[tag].setdefault(music, 0)
        tag_music[tag][music] = 1  # 标签顶点
        
        music_tag.setdefault(music, dict())
        music_tag[music].setdefault(tag, 0)
        music_tag[music][tag] = 1  # 音乐顶点
        
    return user_tag, tag_user, tag_music, music_tag

def initGraph(user_tag, tag_user, tag_music, music_tag):
    tag_G = dict()
    music_G = dict()
    
    tag_G = dict(user_tag, **tag_user)
    music_G = dict(tag_music, **music_tag)

    return tag_G, music_G

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
    file_path = u"./data/基于图标签的推荐数据.txt"
    records = load_data(file_path)
    #print(records)
    user_tag, tag_user, tag_music, music_tag = user_vertex_cal(records)
    print("用户-标签顶点: ", user_tag)
    print("标签-用户顶点: ", tag_user)
    print("标签-音乐顶点: ", tag_music)
    print("音乐-标签顶点: ", music_tag)
    tag_G, music_G = initGraph(user_tag, tag_user, tag_music, music_tag)
    print("tag_G: ", tag_G)
    print("music_G: ", music_G)
    rank = PersonalRank(tag_G, 0.85, "A", 100)
    print(rank)
    rec = Recommend("A", rank, user_tag)
    print("推荐风格: ", rec)