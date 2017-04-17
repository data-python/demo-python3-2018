import requests
import json
import pymongo

ip = "127.0.0.1"
port = 27017 # 默认端口
db_name = 'mean'
collection_name = 'article'

url_1 = 'http://ditu.amap.com/service/poiInfo?id=BOFFG62VDM&query_type=IDQ' # 高德 - 哈尔滨江北技术馆
url_2 = 'http://ditu.amap.com/service/poiInfo?id=B01C30003A&query_type=IDQ' # 太阳岛风景区
urls = [url_1, url_2] # 列表

mongo_conn = pymongo.MongoClient(ip, port)
db = mongo_conn[db_name]
collection = db[collection_name]

for url in urls:
    try:
        print(url)
        resp = requests.get(url)
        json_dict = json.loads(resp.text)
        collection.save(json_dict)
    except Exception as e:
        print(e)
