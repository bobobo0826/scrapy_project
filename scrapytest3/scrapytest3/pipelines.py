# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import datetime
import json
import re
import traceback

import pymongo
import os

from scrapy import log

from scrapytest3.items import Scrapytest3Item

import time
from scrapytest3.logging import get_logger


# start_time = time.strftime('%Y%m%d%H%M%S', time.localtime())
# get_logger('XinHua', start_time)
from scrapytest3.settings import ROOT_DIR


class Scrapytest3Pipeline(object):
    def __init__(self):
        self.client = pymongo.MongoClient("localhost", 27017)
        # db_name = item['website'] + '_db'
        self.db = self.client["xinhua_db"]
        self.newsItem = self.db["url"]

    def process_item(self, item, spider):
        self.save_url_to_db(item)
        self.save_content(item)
        return item

    def save_url_to_db(self, item):
        try:
            self.newsItem.insert(dict(item))
        except Exception as e:
            log.msg("This is a error", level=log.ERROR)

    def save_content(self, item):
        now_time = datetime.datetime.now().strftime('%Y-%m-%d')
        if item['publish_time'] and item['title'] and item['text'] and item['cate']:
            file_path = ROOT_DIR + now_time + '/' + item['website'] + '/' + item['publish_time']
            self.create_ws(file_path, item)

    def create_ws(self, path, item):
        folder = os.path.exists(path)
        if not folder:  # 判断是否存在文件夹如果不存在则创建为文件夹
            os.makedirs(path)  # makedirs 创建文件时如果路径不存在会创建这个路径
        title = re.sub('[\s+\.\!\/_,$%^*(+\"\')]+|[+——()\|?【】“”！，。？:：、~@#￥%……&*（）>]+', '', item['title'])
        txt_path = path + '/' + item['publish_time'] + '-' + title + ".txt"
        with open(txt_path, mode='w', encoding='utf-8') as f:
            try:
                f.write('%s\r\n' % item['title'])
                if 'publish_time' in item:
                    f.write('%s\r\n' % item['publish_time'])
                if 'source' in item and item['source'] is not None:
                    f.write('来源：%s\r\n' % item['source'])
                else:
                    f.write('来源：\r\n')

                f.write("板块：%s\r\n" % item['cate'])
                f.write('\r\n')
                if 'author' in item and item['author'] is not None:
                    f.write("    □记者%s\r\n" % item['author'])
                paras = item['text'].split("\r\n")
                for para in paras:
                    clean_para = para.strip()
                    if clean_para:
                        f.write("    %s\r\n" % clean_para)
                f.flush()
                f.close()
            except Exception as e:
                log.msg("This is a error", level=log.ERROR)

                # def open_spider(self, spider):
    #     self.file = open('newschina.json', 'w')
    #     self.file.write("[")
    #     pass
    #
    # def close_spider(self, spider):
    #     self.file.write("]")
    #     self.file.close()
    #     pass
    #
    # def process_item(self, item, spider):
    #     line = json.dumps(
    #         dict(item),
    #         sort_keys=True,
    #         indent=4,
    #         separators=(',', ': ')
    #     ) + ",\n"
    #     self.file.write(line)
    #     '''
    #     file = open(item['link_text']+ '.txt', 'w')
    #     file.write(item['text'])
    #     file.close()
    #     file = open(item['link_text']+ '.html', 'w')
    #     file.write(item['html'])
    #     file.close()
    #     '''
    #     #print('============='+line)
    #     return item
