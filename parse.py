import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
from datetime import datetime

# Global Varibles
collection = MongoClient('localhost', 27017).iguana.ettoday


hotnewsReq = requests.get("http://www.ettoday.net/news/hot-news.htm")
hotnewsSoup = BeautifulSoup(hotnewsReq.text)

hotnews = []

for titles in hotnewsSoup.select('.part_pictxt_2 h3 a'):
    url = "http://www.ettoday.net" + titles.get('href')

    detailReq = requests.get(url)
    detailSoup = BeautifulSoup(detailReq.text)

    img = detailSoup.select('meta[property="og:image"]')[0].get('content')
    keywords = [keyword.text for keyword in detailSoup.select('.menu_txt_2 a strong')]
    hotnews.append([titles.text , url , img , keywords])

for lists in hotnews:
    [title, url, img, keywords] = lists
    # print title, href ,img, keywords
    dataObject = {
        "source": 'ettoday',
        "newsTitle" : title,
        "url" : url,
        "image" : img,
        "keywords" : keywords,
        "content" : "",
        "tag" : [],
        "title" : "",
        "name" : "",
        "comment" : [],
        "dislike" : [],
        "like" : [],
        "create_date" : ''
    }
    collection.insert_one(dataObject)
