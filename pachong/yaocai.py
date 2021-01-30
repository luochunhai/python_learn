import requests, re
from bs4 import BeautifulSoup

res = requests.get('http://www.pharmnet.com.cn/tcm/knowledge/detail/105486.html')

soup = BeautifulSoup(res.text, 'html.parser')
name = soup.find('h1')
temp = soup.find_all('td', {"class": "maintext"})
pattern = re.compile(r'【生境分布】(.+?)<br')
growing = pattern.findall(str(temp))
print("药材名称: {}, \n 生境分布: {}".format(name, growing))
