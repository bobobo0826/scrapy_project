import threading

from scrapy.cmdline import execute

execute(['scrapy', 'crawl', 'CanKao','-s','CLOSESPIDER_ITEMCOUNT=10','-o','newschina.csv'])

# execute(['scrapy', 'crawl', 'JingJiShiBao'])
# execute(['scrapy', 'crawl', 'XinHua'])
# execute(['scrapy', 'crawl', 'CanKao'])
# execute(['scrapy', 'crawl', 'PengPai'])
# execute(['scrapy', 'crawl', 'HuanQiu'])
# execute(['scrapy', 'crawl', 'HeXun'])
# execute(['scrapy', 'crawl', 'GuangMing'])
# execute(['scrapy', 'crawl', 'LuTouShe'])
# execute(['scrapy', 'crawl', 'RenMin'])
# execute(['scrapy', 'crawl', 'JingJiCanKao'])
# execute(['scrapy', 'crawl', 'MeiRiDianXun'])
# execute(['scrapy', 'crawl', 'RenMinRiBao'])
# execute(['scrapy', 'crawl', 'ZhongGuoXinWen'])
# execute(['scrapy', 'crawl', 'SoHu'])



class SpiderThread(threading.Thread):
    def __init__(self, spider):
        super(SpiderThread, self).__init__()  # 注意：一定要显式的调用父类的初始化函数。
        self.spider = spider

    def run(self):  # 定义每个线程要运行的函数
        execute(['scrapy', 'crawl', self.spider])


# if __name__ == '__main__':
#     spider_names = ['ZhongGuoXinWen', 'XinHua', 'CanKao', 'PengPai', 'HuanQiu', 'HeXun', 'GuangMing', 'LuTouShe',
#                     'RenMin', 'HeXun', 'JingJiShiBao', 'MeiRiDianXun', 'JingJiCanKao', 'RenMinRiBao', '']
#
#     for spider in spider_names:
#         t = SpiderThread(spider)
#         t.start()
