#!/usr/bin/env python
# coding: utf-8

# File Name: TagBasedTFIDF.py
# Author   : john
# Mail     : keyue654321@126.com
# Created Time: 2019/1/25 11:17
# Describe : 基于标签的音乐推荐系统

from math import log
from collections import defaultdict


def load_data(file_path):
    records = []
    f = open(file_path, "r", encoding="utf-8")
    for line in f:
        info = line.strip().split("\t")
        records.append(info)
	f.close()

    return records


def InitStat(records):
    user_tags = dict()  # 用户打过标签的次数
    tag_items = dict()  # 音乐被打过标签的次数，代表歌曲流行度

    for user, item, tag in records:
        user_tags.setdefault(user, dict())
        user_tags[user].setdefault(tag, 0)
        user_tags[user][tag] += 1

        tag_items.setdefault(tag, dict())
        tag_items[tag].setdefault(item, 0)
        tag_items[tag][item] += 1

    return user_tags, tag_items


def InitStat_update(records):
    user_tags = dict()  # 用户打过标签的次数
    tag_items = dict()  # 音乐被打过标签的次数，代表歌曲流行度
    tag_user = dict()  # 标签被用户标记次数

    for user, item, tag in records:
        user_tags.setdefault(user, dict())
        user_tags[user].setdefault(tag, 0)
        user_tags[user][tag] += 1

        tag_items.setdefault(tag, dict())
        tag_items[tag].setdefault(item, 0)
        tag_items[tag][item] += 1

        tag_user.setdefault(tag, dict())
        tag_user[tag].setdefault(user, 0)
        tag_user[tag][user] += 1

    return user_tags, tag_items, tag_user


def InitStat_update_2(records):
    user_tags = dict()  # 用户打过标签的次数
    tag_items = dict()  # 音乐被打过标签的次数，代表歌曲流行度
    tag_user = dict()  # 标签被用户标记次数
    item_user = dict()  # 音乐被不同用户标记次数

    for user, item, tag in records:
        user_tags.setdefault(user, dict())
        user_tags[user].setdefault(tag, 0)
        user_tags[user][tag] += 1

        tag_items.setdefault(tag, dict())
        tag_items[tag].setdefault(item, 0)
        tag_items[tag][item] += 1

        tag_user.setdefault(tag, dict())
        tag_user[tag].setdefault(user, 0)
        tag_user[tag][user] += 1

        item_user.setdefault(item, dict())
        item_user[item].setdefault(user, 0)
        item_user[item][user] += 1

    return user_tags, tag_items, tag_user, item_user


def Recommend(user, K):
    recommend_items = dict()
    for tag, wut in user_tags[user].items():
        for item, wti in tag_items[tag].items():
            if item not in recommend_items:
                recommend_items[item] = wut * wti  # 计算用户对物品兴趣度
            else:
                recommend_items[item] += wut * wti

    rec = sorted(recommend_items.items(), key=lambda x: x[1], reverse=True)  # 将推荐歌曲按兴趣度排名
    print(">>>>>>", rec)
    music = []
    for i in range(K):
        music.append(rec[i][0])

    music = "/".join(music)

    return music


def Recommend_update(user, K):
    recommend_items = dict()
    for tag, wut in user_tags[user].items():
        for item, wti in tag_items[tag].items():
            if item not in recommend_items:
                recommend_items[item] = wut * wti / log(1 + len(tag_user[tag]))  # 计算用户对物品兴趣度
            else:
                recommend_items[item] += wut * wti / log(1 + len(tag_user[tag]))

    rec = sorted(recommend_items.items(), key=lambda x: x[1], reverse=True)  # 将推荐歌曲按兴趣度排名
    print(">>>>>>", rec)
    music = []
    for i in range(K):
        music.append(rec[i][0])

    music = "/".join(music)

    return music


def Recommend_update_2(user, K):
    recommend_items = dict()
    for tag, wut in user_tags[user].items():
        for item, wti in tag_items[tag].items():
            if item not in recommend_items:
                recommend_items[item] = (wut / log(1 + len(tag_user[tag]))) * (
                            wti / log(1 + len(item_user[item])))  # 计算用户对物品兴趣度
            else:
                recommend_items[item] += (wut / log(1 + len(tag_user[tag]))) * (wti / log(1 + len(item_user[item])))

    rec = sorted(recommend_items.items(), key=lambda x: x[1], reverse=True)  # 将推荐歌曲按兴趣度排名
    print(">>>>>>", rec)
    music = []
    for i in range(K):
        music.append(rec[i][0])

    music = "/".join(music)

    return music


if __name__ == '__main__':
    file_path = u"./data/标签的推荐数据.txt"
    records = load_data(file_path)
    # print(records)
    # user_tags, tag_items = InitStat(records)
    # user_tags, tag_items, tag_user = InitStat_update(records)
    user_tags, tag_items, tag_user, item_user = InitStat_update_2(records)
    print("用户打过标签的次数: ", user_tags)
    print("音乐打过标签的次数: ", tag_items)
    print("标签被用户使用次数: ", tag_user)
    print("音乐被用户标记次数: ", item_user)
    # rec = Recommend("A", 2)
	# rec = Recommend_update("A", 2)
    rec = Recommend_update_2("A", 2)
    print("推荐歌曲: ", rec)
