# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
import re
import traceback

import chardet
import pymongo

from ckxx_spider.items import NewsInfoItem
from ckxx_spider.settings import PARA_SEP


class MongoDBPipleline(object):
    def __init__(self):
        clinet = pymongo.MongoClient("localhost", 27017)
        db = clinet["ckxx_db"]
        self.newsItem = db["ckxx_news"]


    def process_item(self, item, spider):
        """ 判断item的类型，并作相应的处理，再入数据库 """
        if isinstance(item, NewsInfoItem):
            try:
                self.newsItem.insert(dict(item))
            except Exception as e:
                print(e)

class LocalStorePipeline(object):


    def process_item(self, item, spider):
        html_path = "D://cankaoxiaoxi/html/"
        content_path = "D://cankaoxiaoxi/content/"

        if isinstance(item, NewsInfoItem):
            self.save_html(item,path_prefix=html_path)
            self.save_content(item,path_prefix=content_path)
        return item

    def save_html(self, item, path_prefix):
        if "title" in item and item["title"] is not None:
            cache_path = path_prefix + item['publish_time']
            file_name = item['publish_time'] + '-' + item['title']
            file_name = re.sub('[\s+\.\!\/_,$%^*(+\"\')]+|[+——()\|?【】“”！，。？:：、~@#￥%……&*（）]+', '', file_name)
        else:
            #解析错误，把网页单独存下来
            cache_path = path_prefix+"parse_error"
            file_name = re.sub('[\s+\.\!\/_,$%^*(+\"\')]+|[+——()\|?【】“”！，。？:：、~@#￥%……&*（）]+', '', item["url"])
        if not os.path.exists(cache_path):
            os.makedirs(cache_path)
        tmp = '%s/%s.dat' % (cache_path, file_name)
        with open(tmp, mode='w', encoding='utf-8') as f:
            try:
                if 'html' in item:
                    f.write(item['html'])
                    f.flush()
                f.close()
            except:
                traceback.print_exc()

    def save_content(self, item, path_prefix):
        #解析错误直接return
        if "title" not in item or item["title"] is None:
            return
        cache_path = path_prefix + item['publish_time']
        if not os.path.exists(cache_path):
            os.makedirs(cache_path)
        file_name = item['publish_time'] + '-' + item['title']
        file_name = re.sub('[\s+\.\!\/_,$%^*(+\"\')]+|[+——()\|?【】“”！，。？:：、~@#￥%……&*（）]+', '', file_name)
        tmp = '%s/%s.txt' % (cache_path, file_name)
        with open(tmp, mode='w', encoding='utf-8') as f:
            try:
                f.write('标题：%s\r\n' % item['title'])
                if 'channel' in item:
                    f.write('版块：%s\r\n' % item['channel'])
                if 'author' in item:
                    f.write('作者：%s\r\n' % item['author'])
                if 'publish_time' in item:
                    f.write('发布时间：%s\r\n' % item['publish_time'])
                if 'source' in item:
                    f.write('来源：%s\r\n' % item['source'])
                if 'url' in item:
                    f.write('源链接：%s\r\n' % item['url'])
                if 'content' in item:
                    lines = item['content'].split(PARA_SEP)
                    if lines and len(lines) > 0:
                        for line in lines:
                            f.write('  '+line+'\r\n')
                f.flush()
                f.close()
            except:
                traceback.print_exc()













