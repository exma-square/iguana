import requests
from bs4 import BeautifulSoup
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
    [title,href,img , keywords] = lists
    print title , href , img
    for keyword in keywords:
        print keyword



