import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
from datetime import datetime

# Global Varibles
collection = MongoClient('localhost', 27017).xgag.posts


hotnewsReq = requests.get("http://www.ettoday.net/news/hot-news.htm")
hotnewsSoup = BeautifulSoup(hotnewsReq.text , "html.parser")

hotnews = []

for titles , time in zip(hotnewsSoup.select('.part_pictxt_2 h3 a'), hotnewsSoup.select('.box_0.clearfix p.summary span')):
    url = "http://www.ettoday.net" + titles.get('href')

    detailReq = requests.get(url)
    detailSoup = BeautifulSoup(detailReq.text)

    time = time.text
    time = time.strip("(")
    time = time.strip(")")
    time = time.replace(" " , "T") + "Z"
    tag = detailSoup.select('body')[0].get('id')
    img = detailSoup.select('meta[property="og:image"]')[0].get('content')
    keywords = [keyword.text for keyword in detailSoup.select('.menu_txt_2 a strong')]
    hotnews.append([titles.text , tag , url , img , keywords , time])

for lists in hotnews:
    [title, tag, url, img, keywords , time] = lists
    dataObject = {
        "url" : url,
        "content" : "",
        "keywords" : keywords,
        "create_date" : time,
        "image" : img,
        "newsTitle" : title,
        "tag" : tag,
        "title" : title,
        "name" : "Ettoday",
        "comment" : [],
        "dislike" : [],
        "like" : [],
        "__v" : 0
    }
    collection.insert_one(dataObject)
