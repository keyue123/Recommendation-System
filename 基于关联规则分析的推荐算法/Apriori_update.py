#!/usr/bin/env python
# coding: utf-8

# File Name: Apriori_update.py
# Author   : john
# Mail     : keyue654321@126.com
# Created Time: 2019/1/7 11:17
# Describe : 基于关联规则的推荐系统

import math
import collections
import pandas as pd

def load_data(file_path):
    dataSet = dict()
    f = open(file_path, "r", encoding="utf-8")
    for line in f:
        data = line.strip().split(",")
        user = data[0]
        del data[0]
        dataSet[user] = data
	f.close()

    return dataSet

def cut_tree(data_count, data_num, support):
    data = dict([(phone, num) for phone, num in data_count.items() if (num/data_num) >= support])  # 第一次剪枝
    data_cut = dict([(phone, num) for phone, num in data_count.items() if (num/data_num) < support])  # 第一次剪枝
    
    return data, data_cut

def Combinations(data, k):  # 获取列表的K个元素的组合
    n = len(data)
    result = []
    for i in range(n-k+1):
        if k > 1:
            newL = data[i+1: ]
            Comb = Combinations(newL, k - 1)
            for item in Comb:
                item.insert(0, data[i])
                result.append(item)
        else:
            result.append([data[i]])
            
    return result

def move_cut(data, data_cut, K):
    phone = []
    phone_move = []
    for key, value in data.items():
        phone += key.split("、")
        
    phone = list(set(list(phone)))
    data_list = Combinations(phone, K)  # 获取子集
    if len(data_list) == 0:
        return data
    
    for key, value in data_cut.items():
        phone_move.append(key.split("、"))
        
    for i in phone_move:
        for j in data_list:
            if set(list(i)).issubset(list(j)):
                data_list.remove(j)
    
    return data_list

def num_count(dataSet, data):
    data_list = dict()
    for user, phone in dataSet.items():
        phone = list(phone)
        for i in data:
            if set(list(i)).issubset(list(phone)):
                keys = "、".join(list(i))
                data_list.setdefault(keys, 0)
                data_list[keys] += 1
    
    return data_list

def first_num_count(dataSet):
    data_list = dict()
    for user, phone in dataSet.items():
        for keys in phone:
            data_list.setdefault(keys, 0)
            data_list[keys] += 1
    
    return data_list


# 支持度为0.2
if __name__ == '__main__':
    file_path = "./data/data.txt"
    dataSet = load_data(file_path)  # 计数
    print("用户-物品倒排列表: ", dataSet)
    
    data_count = first_num_count(dataSet)
    print("第1次剪枝前拓展项计数: ", data_count)
    
    data_num = len(dataSet)
    data, data_cut = cut_tree(data_count, data_num, 0.5)
    print("第1次剪枝后拓展项计数: ", data)

    K = 2
    while True:
        data = move_cut(data, data_cut, K)
        print("第%d次拓展初始集合: %s" % (K, data))
        
        data_count = num_count(dataSet, data)  # 子集计数
        print("第%d次剪枝前拓展项计数: %s" % (K, data_count))
        
        if len(data_count) == 0:  # 如果无法拓展，表示已经完成，data为最后的拓展项集
            print(">>>>>拓展结束")
            break
        
        data, data_cut = cut_tree(data_count, data_num, 0.5)  # 剪枝
        print("第%d次剪枝后拓展项计数: %s" % (K, data))
        #print("第%d次被剪枝数据: %s" % (K, data_cut))
        
        
        
        K += 1

    phone = []
    for key, value in data.items():
        phone = key.split("、")
        num = value
    
    # 获取列表的非空子集
    print("phone: ", phone)
    data_num = []
    for i in range(1, len(phone)):
        data_num += Combinations(phone, i)
        
    print("非空子集:", data_num)
    
    # 置信度计算
    for i in data_num:
        count = 0
        for u, v in dataSet.items():
            if set(i).issubset(list(v)):
                count += 1
        
        
        print(i, "置信度: ", float(num)/count)