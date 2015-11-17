import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
from datetime import datetime

# Global Varibles
collection = MongoClient('localhost', 27017).iguana.ettoday


hotnewsReq = requests.get("http://www.ettoday.net/news/hot-news.htm")
hotnewsSoup = BeautifulSoup(hotnewsReq.text, "html.parser")


hotnews = []

for titles , time in zip(hotnewsSoup.select('.part_pictxt_2 h3 a'), hotnewsSoup.select('.box_0.clearfix p.summary span')):
    url = "http://www.ettoday.net" + titles.get('href')

    detailReq = requests.get(url)
    detailSoup = BeautifulSoup(detailReq.text)

    url = detailSoup.select('head link[rel="canonical"]')[0].get('href')
    fbReq = requests.get('https://graph.facebook.com/?ids=' + url)
    fbData = fbReq.json()

    shareCount = fbData[url]['shares']
    likeCount = fbData[url]['shares']
    try:
        commentCount = fbData[url]['comments']
    except KeyError:
        commentCount = 0


    time = time.text
    time = time.strip("(")
    time = time.strip(")")
    time = time.replace(" " , "T") + "Z"
    category = detailSoup.select('body')[0].get('id')
    img = detailSoup.select('meta[property="og:image"]')[0].get('content')
    keywords = [keyword.text for keyword in detailSoup.select('.menu_txt_2 a strong')]
    hotnews.append([titles.text , category , url , img , keywords , time , shareCount , likeCount , commentCount])

for lists in hotnews:
    [title, category, keywords, shareCount, likeCount, commentCount, content, url, time, img] = lists
    dataObject = {
        "title": title, # 標題
        "category": category, # 分類
        "keywords" : keywords, #關鍵字
        "shareCount": '', # 分享數
        "likeCount": '', # 按讚數
        "commentCount": '',
        "browserCount": 0, # 瀏覽數
        "content": '', #內文
        "comment" : [], # 評論
        "url" : url, # 網址
        "create_date" : time, # 發布時間
        "image" : img, # 圖片
        "source" : "Ettoday", # 來源
    }
    collection.insert_one(dataObject)




