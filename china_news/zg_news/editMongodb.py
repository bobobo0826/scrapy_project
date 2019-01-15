# -*- coding:utf-8 -*-
import pymongo
import re
from html.parser import HTMLParser # 将字符串格式的html文本转成html


class editMongodb(object):

    def __init__(self):
        self.client = pymongo.MongoClient("mongodb://localhost:27017/")


    def run(self):
        db_name = 'zg_news'
        db = self.client[db_name]
        col=db["news"]
        list=col.find_one()
        html=list["html"]

        # 新闻标题
        pattern1= re.compile(r"(?<=<title>).*?([\u4E00-\u9FA5])(?=</title>)")
        match1 = pattern1.search(html)
        title=match1.group(0)
        print(title)

        # parser = MyHTMLParser()



#
# class MyHTMLParser(HTMLParser):
#     def __init__(self):
#         HTMLParser.__init__(self)
#         self.data = []
#     def handle_startendtag(self, tag, attrs):
#         pass
#     def handle_endtag(self, tag):
#         pass
#     def handle_data(self, data):
#         if data.count('\n') == 0:
#             self.data.append(data)





if __name__ == '__main__':
    mongo_obj = editMongodb()
    mongo_obj.run()
