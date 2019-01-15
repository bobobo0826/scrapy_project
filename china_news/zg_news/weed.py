# -*- coding:utf-8 -*-
import pymongo
import re
from html.parser import HTMLParser # 将字符串格式的html文本转成html
import os


class weed(object):

    def __init__(self):
        self.client = pymongo.MongoClient("mongodb://localhost:27017/")

    def run(self):
        db_name = 'zg_news'
        db = self.client[db_name]
        col=db["news"]
        for item in col.find():
            if item["datetime"]:
                file_path = 'D:/origin/'+item["datetime"]
                self.create_ws(file_path,item)



    def create_ws(self,path,item):
        folder = os.path.exists(path)
        if not folder:  # 判断是否存在文件夹如果不存在则创建为文件夹
            os.makedirs(path)  # makedirs 创建文件时如果路径不存在会创建这个路径
        title =re.sub('[\s+\.\!\/_,$%^*(+\"\')]+|[+——()\|?【】“”！，。？:：、~@#￥%……&*（）]+', '', item["title"])
        txt_path = path + '/'+item["datetime"] + '-' + title+".txt"
        file = open(txt_path, 'w',encoding='utf-8')

        file.write(title+"\n")
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




if __name__ == '__main__':
    mongo_obj = weed()
    mongo_obj.run()
