import requests, json

'''
params = {"query":"ATM","tag":"yinghagn"}
res= requests.get("http://api.map.baidu.com/place/v2/search", params=params}
'''

url = "http://api.map.baidu.com/place/v2/search?query=ATM机&tag=银行&region=北京&output=json&ak="
api_url = url + "CB93fSBovNTebnj33PspmlisKyX3uMDp"

res = requests.get(api_url)

api_rdata = json.loads(res.text)

with open("baidu_api_data.csv", "w") as apiFile:
    # 提取output中 result 字段部分写入
    for i in range(len(api_rdata["results"])):
        apiFile.write(api_rdata["results"][i]["name"] + "\t")
        apiFile.write(api_rdata["results"][i]["city"] + "\t")
        apiFile.write(api_rdata["results"][i]["area"] + "\n")
