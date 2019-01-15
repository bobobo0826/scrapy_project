# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import re
import traceback

import pymongo
import os

from huanqiuNews.items import HuanqiunewsItem


class HuanqiunewsPipeline(object):
    def __init__(self):
        self.client = pymongo.MongoClient("localhost", 27017)
        self.db = self.client["huanqiu_db"]
        self.newsItem = self.db["huanqiu_data"]

    def process_item(self, item, spider):

        if isinstance(item, HuanqiunewsItem):
            self.save_html_to_db(item)
            self.save_content(item)
        return item

    def save_html_to_db(self, item):
        try:
            self.newsItem.insert(dict(item))
        except Exception as e:
            traceback.print_exc()

    def save_content(self, item):
        if item['publish_time'] and item['title'] and item['content'] and item['type']:
            file_path = 'D:/huanqiu/' + item['publish_time']
            self.create_ws(file_path, item)

    def create_ws(self, path, item):
        folder = os.path.exists(path)
        if not folder:  # 判断是否存在文件夹如果不存在则创建为文件夹
            os.makedirs(path)  # makedirs 创建文件时如果路径不存在会创建这个路径
        title = re.sub('[\s+\.\!\/_,$%^*(+\"\')]+|[+——()\|?【】“”！，。？:：、~@#￥%……&*（）>]+', '',item['title'])
        txt_path = path + '/' + item['publish_time'] + '-' + title + ".txt"
        with open(txt_path, mode='w', encoding='utf-8') as f:
            try:
                f.write('%s\r\n' % item['title'])
                if 'publish_time' in item:
                    f.write('%s\r\n' % item['publish_time'])
                if 'source' in item and item['source'] is not None:
                    f.write('来源：%s\r\n' % item['source'])
                else:
                    f.write('来源：环球网\r\n')

                f.write("板块：%s\r\n" % item['type'])
                f.write('\r\n')
                if 'author' in item and item['author'].strip()!='':
                    f.write("       □记者%s\r\n" % item['author'])
                paras = item['content'].split("\n")
                for para in paras:
                    clean_para = para.strip()
                    if clean_para:
                        f.write("       %s\n" % clean_para)
                f.flush()
                f.close()
            except Exception as e:
                traceback.print_exc()




