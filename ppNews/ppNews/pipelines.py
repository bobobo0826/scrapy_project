# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
import os
import re
from ppNews.items import PpnewsItem
class PpnewsPipeline(object):
    def __init__(self):
        clinet = pymongo.MongoClient("localhost", 27017)
        db = clinet["ppNews"]
        self.PpnewsItem = db["ppNews_item"]


    def process_item(self, item, spider):
        """ 判断item的类型，并作相应的处理，再入数据库 """
        if isinstance(item, PpnewsItem):
            try:
                self.PpnewsItem.insert(dict(item))
                if item["type1"] == "时事" or item["type1"] == "财经":
                    file_path = 'D:/ppNews/' + item["datetime"]
                    self.create_ws(file_path, item)
            except Exception:
                pass

        return item
    # def process_item(self, item, spider):
    #     self.db[self.collection_name].update({'url': item['url']}, {'$set': dict(item)}, True)
    #     if item["type1"]=="时事" or item["type1"]=="财经":
    #         file_path = 'D:/ppNews/' + item["datetime"]
    #         self.create_ws(file_path, item)
    #     return item

    def create_ws(self, path, item):
        folder = os.path.exists(path)
        if not folder:  # 判断是否存在文件夹如果不存在则创建为文件夹
            os.makedirs(path)  # makedirs 创建文件时如果路径不存在会创建这个路径
        title = re.sub('[\s+\.\!\/_,$%^*(+\"\')]+|[+——()\|?【】“”！，。？:：、~@#￥%……&*（）>]+', '', item["title"])
        txt_path = path + '/' + item["datetime"] + '-' + title + ".txt"
        file = open(txt_path, 'w', encoding='utf-8')

        file.write(title + "\n")
        file.write(item["datetime"] + "\n")
        if item["source"]:
            file.write("来源：" + item["source"] + "\n")
        else:
            file.write("来源：澎湃新闻" + "\n")
        file.write("板块：" + item["type1"] +'-'+item["type2"]+ "\n")
        file.write("\n")
        if item["editor"]:
            writor = item["editor"]
            file.write("       □记者" + writor + '\n')
        arr = item['content'].split('\r\n')
        if arr and len(arr) > 0:
            for line in arr:
                if line:
                    file.write('       ' + line + '\r\n')
        file.close()


