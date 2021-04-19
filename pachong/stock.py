import requests
from bs4 import BeautifulSoup

res = requests.get('http://stockpage.10jqka.com.cn/600109/')
res.encoding = 'utf-8'
html = res.text

soup = BeautifulSoup(res.text, 'html.parser')

temp = soup.find(class_="company_details")
result = temp.contents[9].attrs
print(result)
