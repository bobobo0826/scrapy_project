# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import traceback
import pymongo
import os
import re
from jjckNews.items import JjcknewsItem
class JjcknewsPipeline(object):
    def __init__(self):
        self.client = pymongo.MongoClient("localhost", 27017)
        self.db = self.client["jjck_db"]
        self.newsItem = self.db["jjck_data"]

    def process_item(self, item, spider):
        if isinstance(item, JjcknewsItem):
            self.save_html_to_db(item)
            self.save_content(item)
        return item

    def save_html_to_db(self,item):
        try:
            self.newsItem.insert(dict(item))
        except Exception as e:
            traceback.print_exc()
    def save_content(self,item):
        if "title" not in item or item["title"] is None or item['title'].strip() == "":
            return
        if "content" not in item or item["content"] is None or item['content'].strip() == "":
            return
        file_path = 'D:/jjck/' + item["datetime"]
        self.create_ws(file_path, item)

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

        file.write("       □记者"+item["author"]+'\n')
        arr = item['content'].split('\r\n')
        if arr and len(arr) > 0:
            for line in arr:
                if line:
                    file.write('       '+line+'\r\n')
        file.close()

