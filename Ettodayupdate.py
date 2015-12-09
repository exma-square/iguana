# -*- coding: utf-8 -*-
import requests
from pymongo import MongoClient
from datetime import datetime

col_ettoday = MongoClient('192.168.99.100', 27017).iguana.ettoday
col_ettoday_count = MongoClient('192.168.99.100', 27017).iguana.ettoday_count

ettoday = col_ettoday.find()
hotnewsCount = []
for doc in ettoday:
    news_id = doc['_id']
    url = doc['url']
    fbReq = requests.get('https://graph.facebook.com/?ids=' + url)
    fbData = fbReq.json()
    shareCount = fbData[url]['shares'] if fbData[url].has_key('shares') else 0
    likeCount = shareCount
    commentCount = fbData[url]['comments'] if fbData[url].has_key('comments') else 0

    hotnewsCount.append([news_id , shareCount, likeCount , commentCount])

update_time = datetime.now();

for lists in hotnewsCount:
    [news_id, shareCount, likeCount, commentCount] = lists
    #print news_id, shareCount, likeCount, commentCount
    count_dataObject = {
        "news_id" : news_id,
        "shareCount": shareCount, # 分享數
        "likeCount": likeCount, # 按讚數
        "commentCount": commentCount, #評論數
        "update_time" : update_time, #更新時間
        "browserCount": None, # 瀏覽數
    }
    col_ettoday_count.update_one(
        {
            "news_id" : news_id,
            "shareCount": shareCount, # 分享數
            "likeCount": likeCount, # 按讚數
            "commentCount": commentCount, #評論數
            "update_time" : update_time
        },
        {"$set": count_dataObject} ,
        upsert = True
    )