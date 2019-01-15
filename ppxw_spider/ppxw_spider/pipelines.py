# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
import re
import traceback

import pymongo

from ppxw_spider.items import ArticleItem

shishi_channels=["中国政库","中南海","舆论场","打虎记","人事风向","法治中国","一号专案","港台来信",
                 "长三角政商","直击现场","暖闻","澎湃质量报告","绿政公署","澎湃国际","外交学人",
                 "澎湃防务","唐人街","澎湃人物","浦江头条","教育家","全景现场","美数课","快看"]
caijing_channels=["10%公司","能见度","地产界","财经上下游","金改实验室","牛市点线面","科技湃",
                  "澎湃商学院","自贸区连线","进博会在线"]
content_path = "D://ppxw/content/"
class PpxwSpiderPipeline(object):


    def __init__(self):
        self.client = pymongo.MongoClient("localhost", 27017)
        self.db = self.client["ppxw_db"]
        self.newsItem = self.db["ppxw_data"]

    def process_item(self, item, spider):

        if isinstance(item, ArticleItem):
            self.save_html_to_db(item)
            self.save_content(item)
        return item

    def save_html_to_db(self, item):
        try:
            self.newsItem.insert(dict(item))
        except Exception as e:
            traceback.print_exc()

    def save_content(self, item):
        if item["channel"] in shishi_channels or item["channel"] in caijing_channels:
            if item['title']:
                if item["content"]:
                    if item["publish_time"]:
                        file_path = 'D:/ppxw/' + item["publish_time"]
                        self.create_ws(file_path, item)

    def create_ws(self, path, item):
        folder = os.path.exists(path)
        if not folder:  # 判断是否存在文件夹如果不存在则创建为文件夹
            os.makedirs(path)  # makedirs 创建文件时如果路径不存在会创建这个路径
        title = re.sub('[\s+\.\!\/_,$%^*(+\"\')]+|[+——()\|?【】“”！，。？:：、~@#￥%……&*（）>]+', '',
                       item["title"])
        txt_path = path + '/' + item["publish_time"] + '-' + title + ".txt"
        with open(txt_path, mode='w', encoding='utf-8') as f:
            try:
                f.write('%s\r\
                n' % item["title"])
                if 'publish_time' in item:
                    f.write('%s\r\n' % item['publish_time'])
                if 'source' in item and item['source'] is not None:
                    f.write('来源：%s\r\n' % item['source'])
                else:
                    f.write('来源：澎湃网\r\n')
                if 'channel' in item and item['channel'] is not None:
                    channel = item['channel']
                    for chan in shishi_channels:
                        if channel == chan:
                            channel = "时事-%s" % channel
                            break
                    else:
                        for chan in caijing_channels:
                            if channel == chan:
                                channel = "财经-%s" % channel
                                break
                    f.write("板块：%s\r\n" % channel)
                f.write('\r\n')
                if 'author' in item and item['author'] is not None:
                    f.write("    □记者%s\r\n" % item['author'])
                paras = item['content'].split("\r\n")
                for para in paras:
                    clean_para = para.strip()
                    if clean_para:
                        f.write("    %s\r\n" % clean_para)
                f.flush()
                f.close()
            except Exception as e:
                traceback.print_exc()

                                    # cache_path = path_prefix + item['publish_time']
        # title = item['title'].strip()
        # if not os.path.exists(cache_path):
        #     os.makedirs(cache_path)
        # file_name = item['publish_time'] + '-' + title
        # file_name = re.sub('[\s+.\\\!/_,$%^*(\"\')<>]+|[+—()|?【】“”！，。？:：、~@#￥%…&*（）]+', '', file_name)
        # tmp = '%s/%s.txt' % (cache_path, file_name)
        # with open(tmp, mode='w', encoding='utf-8') as f:
        #     try:
        #         f.write('%s\r\n' % item['title'])
        #         if 'publish_time' in item:
        #             f.write('%s\r\n' % item['publish_time'])
        #         if 'source' in item and item['source'] is not None:
        #             f.write('来源：%s\r\n' % item['source'])
        #         else:
        #             f.write('来源：澎湃网\r\n')
        #         if 'channel' in item and item['channel'] is not None:
        #             channel = item['channel']
        #             for chan in shishi_channels:
        #                 if channel == chan:
        #                     channel = "时事-%s" %channel
        #                     break
        #             else:
        #                 for chan in caijing_channels:
        #                     if channel == chan:
        #                         channel = "财经-%s" % channel
        #                         break
        #             f.write("板块：%s\r\n" % channel)
        #         f.write('\r\n')
        #         if 'author' in item and item['author'] is not None:
        #             f.write("    □记者%s\r\n" % item['author'])
        #         paras = item['content'].split("\r\n")
        #         for para in paras:
        #             clean_para = para.strip()
        #             if clean_para:
        #                 f.write("    %s\r\n" % clean_para)
        #         f.flush()
        #         f.close()
        #     except Exception as e:
        #         traceback.print_exc()
