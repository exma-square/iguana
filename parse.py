# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
from datetime import datetime


hotnewsReq = requests.get("http://www.ettoday.net/news/hot-news.htm")
hotnewsSoup = BeautifulSoup(hotnewsReq.text, "html.parser")


hotnews = []

for titles , content, time in zip(hotnewsSoup.select('.part_pictxt_2 h3 a'), hotnewsSoup.select('.box_0.clearfix p.summary'), hotnewsSoup.select('.box_0.clearfix p.summary span')):
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
    time = time.replace(" " , "T") + "Z"

    img = detailSoup.select('meta[property="og:image"]')[0].get('content')

    hotnews.append([title, category, keywords, shareCount, likeCount, commentCount, content, url, time, img])

col_ettoday = MongoClient('localhost', 27017).iguana.ettoday
col_ettoday_count = MongoClient('localhost', 27017).iguana.ettoday_count
for lists in hotnews:
    [title, category, keywords, shareCount, likeCount, commentCount, content, url, time, img] = lists
    content_dataObject = {
        "title": title, # 標題
        "category": category, # 分類
        "keywords" : keywords, #關鍵字
        "content": content, #內文
        "comment" : [], # 評論
        "url" : url, # 網址
        "create_date" : time, # 發布時間
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
        "browserCount": None, # 瀏覽數
    }
    col_ettoday_count.update_one(
        {
        "shareCount": shareCount, # 分享數
        "likeCount": likeCount, # 按讚數
        "commentCount": commentCount #評論數
        },
        {"$set": count_dataObject} ,
        upsert = True
    )




