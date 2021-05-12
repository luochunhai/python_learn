# coding=utf-8
import requests
from bs4 import BeautifulSoup

resp = requests.get('https://www.baidu.com')
print(resp)
print(resp.content)

bsobj = BeautifulSoup(resp.content, 'html.parser')
a_list = bsobj.find_all('a')

