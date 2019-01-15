# -*- coding: utf-8 -*-

import os
import re
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import traceback

import pymongo

from xhdxNews.items import XhdxnewsItem
from xhdxNews.statistics import Statistics


class XhdxnewsPipeline(object):
    def __init__(self):
        self.client=pymongo.MongoClient("localhost",27017)
        self.db=self.client["xhdx_db"]
        self.data=self.db["xhdx_data"]
        self.log=self.db["data_raw"]


    #爬虫被打开的时候
    def open_spider(self,spider):
        print("-------------open_spider----------------")
        spider.stat=Statistics(spider.name)
        #初始化已经爬过的数据
        items=self.db["data_raw"].find({'source':spider.name})
        spider.titles=set()
        for item in items:
            spider.titles.add(item['title'])
        spider.stat.crawled_display(spider.name,len(spider.titles))#从数据库中提取已爬取的条数，并打印反馈。


    def process_item(self, item, spider):

        if isinstance(item,XhdxnewsItem):
            print("================save===================")
            self.save_html_to_db(item)
            self.save_content_to_file(item)
        return item

    def save_html_to_db(self,item):
        try:
            self.data.insert(dict(item))
        except Exception as e:
            traceback.print_exc()

    def save_content_to_file(self,item):
        if item['title']:
            if item["content"].strip() != '':
                if item["datetime"]:
                    file_path = 'D:/xhdx/' + item["datetime"]
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
            file.write("来源：新华每日电讯"+"\n")
        if item["type"]:
            type=item["type"]
            file.write("板块："+type+"\n")
        file.write("\n")
        if item["editor"]:
            editor=item["editor"].split("：")[1]
            file.write("       □记者"+editor+'\n')
        arr = item['content'].split('\r\n')
        if arr and len(arr) > 0:
            for line in arr:
                if line:
                    file.write(line+'\r\n')
        file.close()



