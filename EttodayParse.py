# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
from datetime import datetime

#Ettoday parse
EttodayhotnewsReq = requests.get("http://www.ettoday.net/news/hot-news.htm")
EttodayhotnewsSoup = BeautifulSoup(EttodayhotnewsReq.text, "html.parser")


Ettodayhotnews = []

for titles , content, time in zip(EttodayhotnewsSoup.select('.part_pictxt_2 h3 a'), EttodayhotnewsSoup.select('.box_0.clearfix p.summary'), EttodayhotnewsSoup.select('.box_0.clearfix p.summary span')):
    url = "http://www.ettoday.net" + titles.get('href')

    detailReq = requests.get(url)
    detailSoup = BeautifulSoup(detailReq.text, "html.parser")

    title = titles.text

    category = detailSoup.select('body')[0].get('id')

    keywords = [keyword.text for keyword in detailSoup.select('.menu_txt_2 a strong')]

    url = detailSoup.select('head link[rel="canonical"]')[0].get('href')
    fbReq = requests.get('https://graph.facebook.com/?ids=' + url)
    fbData = fbReq.json()
    shareCount = fbData[url]['shares'] if fbData[url].has_key('shares') else 0
    likeCount = shareCount
    commentCount = fbData[url]['comments'] if fbData[url].has_key('comments') else 0
    content = content.text

    time = time.text
    time = time.strip("(")
    time = time.strip(")")
    time = time.replace("-" , "/")
    time = datetime.strptime(time, '%Y/%m/%d %H:%M')

    img = detailSoup.select('meta[property="og:image"]')[0].get('content')

    Ettodayhotnews.append([title, category, keywords, shareCount, likeCount, commentCount, content, url, time, img])


create_at = datetime.now();
col_ettoday = MongoClient('192.168.99.100', 27017).iguana.ettoday
col_ettoday_count = MongoClient('192.168.99.100', 27017).iguana.ettoday_count
for lists in Ettodayhotnews:
    [title, category, keywords, shareCount, likeCount, commentCount, content, url, time, img] = lists
    content_dataObject = {
        "title": title, # 標題
        "category": category, # 分類
        "keywords" : keywords, #關鍵字
        "content": content, #內文
        "url" : url, # 網址
        "create_date" : time, # 發布時間
        "create_at" : create_at, #寫入時間
        "image" : img, # 圖片
        "source" : "Ettoday", # 來源
    }
    col_ettoday.update_one(
        {
           "title": title
        },
        {"$set": content_dataObject},
        upsert = True
    )
    news_id = col_ettoday.find_one({'title': title})['_id']
    count_dataObject = {
        "news_id" : news_id,
        "shareCount": shareCount, # 分享數
        "likeCount": likeCount, # 按讚數
        "commentCount": commentCount, #評論數
        "update_time" : create_at,
        "browserCount": None, # 瀏覽數
    }
    col_ettoday_count.update_one(
        {
            "news_id" : news_id,
            "shareCount": shareCount, # 分享數
            "likeCount": likeCount, # 按讚數
            "commentCount": commentCount, #評論數
            "update_time" : create_at
        },
        {"$set": count_dataObject} ,
        upsert = True
    )
