# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
import os
import re
class ZgNewsPipeline(object):
    collection_name = 'news20181203'
    #news-20180101-20180517
    #curNews-20181121-20180813
    #news1--20180518-20180812
    #news2016-20160926-20161231
    #news2016-20160926-20161231


    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db


    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.db[self.collection_name].update({'url': item['url']}, {'$set': dict(item)}, True)
        if item["datetime"]:
            file_path = 'D:/zgxw/' + item["datetime"]
            self.create_ws(file_path, item)
        return item

    def create_ws(self,path,item):
        folder = os.path.exists(path)
        if not folder:  # 判断是否存在文件夹如果不存在则创建为文件夹
            os.makedirs(path)  # makedirs 创建文件时如果路径不存在会创建这个路径
        title =re.sub('[\s+\.\!\/_,$%^*(+\"\')]+|[+——()\|?【】“”！，。？:：、~@#￥%……&*（）>]+', '', item["title"])
        txt_path = path + '/'+item["datetime"] + '-' + title+".txt"
        file = open(txt_path, 'w',encoding='utf-8')

        file.write(item["title"]+"\n")
        file.write(item["datetime"]+"\n")
        if item["source"]:
            file.write("来源："+item["source"]+"\n")
        else:
            file.write("来源：中国新闻网"+"\n")
        file.write("板块："+item["type"]+"\n")
        file.write("\n")
        if item["editor"]:
            writor=item["editor"].split("编辑:")[1].split("】")[0]
            file.write("       □记者"+writor+'\n')
        arr = item['content'].split('\u3000')
        if arr and len(arr) > 0:
            for line in arr:
                if line:
                    file.write('       '+line+'\r\n')
        file.close()


