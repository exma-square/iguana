
# coding: utf-8

# In[23]:

import requests
from bs4 import BeautifulSoup
hotnewsReq = requests.get("http://www.ettoday.net/news/hot-news.htm")


# In[22]:

hotnewsSoup = BeautifulSoup(hotnewsReq.text)


# In[43]:

hotnewsTitle = []
for titles in hotnewsSoup.select('h3 a'):
    hotnewsTitle.append([titles.text , titles.get('href')])


# In[53]:

for lists in hotnewsTitle:
    [title,href] = lists
    print title , href


# In[ ]:



