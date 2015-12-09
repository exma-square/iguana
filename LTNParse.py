# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
from datetime import datetime

#LTN parse
LTNbreakingnewsReq = requests.get("http://news.ltn.com.tw/list/BreakingNews")
LTNbreakingnewsSoup = BeautifulSoup(LTNbreakingnewsReq.text, "html.parser")

LTNbreakingnews = []
categoryDict = {"tab1":"焦點", "tab2":"政治","tab3":"社會","tab4":"生活","tab5":"國際","tab6":"言論","tab7":"財經","tab8":"體育","tab9":"地方","tab10":"娛樂","tab11":"消費","tab12":"副刊","tab13":"3C","tab14":"汽車","tab15":"iStyle"}
for titles, time, category in zip(LTNbreakingnewsSoup.select('.lipic .picword') , LTNbreakingnewsSoup.select('.lipic span') , LTNbreakingnewsSoup.select('.lipic span a')):
    url = titles.get('href')

    title = titles.text

    time = time.text
    time = time.replace("-" , "/")
    time = datetime.strptime(time, '%Y/%m/%d %H:%M')

    category = category.get('class')
    category = categoryDict[category[0]]

    #print url, title, time, category

    fbReq = requests.get('https://graph.facebook.com/?ids=' + url)
    fbData = fbReq.json()
    shareCount = fbData[url]['shares'] if fbData[url].has_key('shares') else 0
    likeCount = shareCount
    commentCount = fbData[url]['comments'] if fbData[url].has_key('comments') else 0

    detailReq = requests.get(url)
    detailSoup = BeautifulSoup(detailReq.text, "html.parser")

    content = []
    keywords = []

    contents = detailSoup.select('meta[property="og:description"]')
    for cont in contents:
        content.append(cont.get('content'))
    keyword = detailSoup.select('.con_keyword a')
    for key in keyword:
        keywords.append(key.text)
    img = detailSoup.select('meta[property="og:image"]')[0].get('content')

    LTNbreakingnews.append([title, category, keywords, shareCount, likeCount, commentCount, content, url, time, img])


create_at = datetime.now();
col_LTN = MongoClient('192.168.99.100', 27017).iguana.LTN
col_LTN_count = MongoClient('192.168.99.100', 27017).iguana.LTN_count
for lists in LTNbreakingnews:
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
        "source" : "LTN", # 來源
    }
    col_LTN.update_one(
        {
           "title": title
        },
        {"$set": content_dataObject},
        upsert = True
    )
    news_id = col_LTN.find_one({'title': title})['_id']
    count_dataObject = {
        "news_id" : news_id,
        "shareCount": shareCount, # 分享數
        "likeCount": likeCount, # 按讚數
        "commentCount": commentCount, #評論數
        "update_time" : create_at,
        "browserCount": None, # 瀏覽數
    }
    col_LTN_count.update_one(
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

