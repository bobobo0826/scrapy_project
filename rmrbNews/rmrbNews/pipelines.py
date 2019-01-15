# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import traceback
import pymongo
import os
import re
from rmrbNews.items import RmrbnewsItem
class RmrbnewsPipeline(object):
    def __init__(self):
        self.client = pymongo.MongoClient("localhost", 27017)
        self.db = self.client["rmrb_db"]
        self.newsItem = self.db["rmrb_data"]

    def process_item(self, item, spider):
        if isinstance(item, RmrbnewsItem):
            self.save_html_to_db(item)
            self.save_content(item)
        return item

    def save_html_to_db(self,item):
        try:
            self.newsItem.insert(dict(item))
        except Exception as e:
            traceback.print_exc()

    def save_content(self,item):
        if item['title']:
            if item["content"]:
                if item["datetime"]:
                    file_path = 'D:/rmrb/' + item["datetime"]
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
            file.write("来源：人民日报"+"\n")
        if item["type"]:
            type=item["type"].split(":")[1]
            file.write("板块："+type+"\n")
        if item["author"]:
            file.write("       □记者"+item["author"].replace(" ","")+'\n')
        arr = item['content'].split('\r\n')
        if arr and len(arr) > 0:
            for line in arr:
                if line:
                    file.write(line+'\r\n')
        file.close()


