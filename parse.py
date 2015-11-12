import requests
from bs4 import BeautifulSoup
res = requests.get("http://www.ettoday.net")
print res.text