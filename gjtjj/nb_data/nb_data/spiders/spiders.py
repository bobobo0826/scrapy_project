# encoding=utf-8
"""全国年度统计公报"""
import re
import datetime
import pdfkit
from bs4 import BeautifulSoup
from scrapy.selector import Selector
from scrapy.http import Request
from scrapy.spiders import CrawlSpider
import os
html_template = """ 
<!DOCTYPE html> 
<html lang="en"> 
<head> 
    <meta charset="UTF-8"> 
</head> 
<body> 
{content} 
</body> 
</html> 

"""
class Spider(CrawlSpider):
    name = "nbSpider"
    host = "http://dz.jjckb.cn"


    def start_requests(self):
        url = "http://www.stats.gov.cn/tjsj/tjgb/ndtjgb/"
        # url="http://www.stats.gov.cn/tjsj/tjgb/ndtjgb/qgndtjgb/200302/t20030228_30016.html"
        yield Request(url=url, callback=self.parse, dont_filter=True)

    def parse(self, response):
        selector = Selector(response)
        urls=selector.xpath('//ul[@class="center_list_contlist"]/li/a/@href').extract()
        for item in urls:
            if "./" in item:
                url="http://www.stats.gov.cn/tjsj/tjgb/ndtjgb/"+item.split("./")[1]
            else:
                url="http://www.stats.gov.cn"+item
            yield Request(url=url,callback=self.parse_url_to_html)
        arr=selector.xpath('//a[@class="bai12_22h"]').extract()
        for a in arr:
            soup=BeautifulSoup(a,'html.parser')
            item=soup.find('a')
            if "下一页" in item.get_text():
                next_url = "http://www.stats.gov.cn/tjsj/tjgb/ndtjgb/" +item['href']
                yield Request(url=next_url,callback=self.parse)


    def parse_url_to_html(self, response):
        """
        解析URL，返回HTML内容
        """
        #年报发布时间
        # selector=Selector(response)
        # text0=selector.xpath('//font[@class="xilan_titf"]/font/text()').extract()
        # if text0:
        #     for i in text0:
        #         if "发布时间" in i:
        #             time = i.split("发布时间：")[1].split("\xa00")[0]
        #             print(time)
        #             if re.match("^\d{4}-\d{2}-\d{2}$", time):
        #                 ymd = time.split("-")
        #                 publish_time= "%s年%s月%s日" % (ymd[0], ymd[1], ymd[2])

        selector=Selector(response)
        text0=selector.xpath('//div[@class="center"]').extract_first()


        # 标题
        title = selector.xpath('//h2[@class="xilan_tit"]/text()').extract_first()


        html = text0.replace('lang="EN-US"','').replace("楷体","宋体")
        # body中的img标签的src相对路径的改成绝对路径
        soup = BeautifulSoup(response.text, 'html.parser')
        imgs=soup.find_all('img')
        for each in imgs:
            if "_r75" in each.get('src'):
                src=each.get('src').split("/")[1]
                url = response.url.split("/")
                start_url = ''
                for index in range(len(url) - 1):
                    start_url = start_url + url[index] + "/"
                whole_url=start_url+src
                html=html.replace(each.get('src'),whole_url)
        html = html_template.format(content=html)
        html = html.encode("utf-8")
        name=re.sub('[\s+\.\!\/_,$%^*(+\"\')]+|[+——()\|?【】“”！，。？:：、~@#￥%……&*（）>]+', '',title)
        if "统计公报" not in name:
            name=name+"国民经济和社会发展统计公报"
        html_path = 'D:/gjtjj/html'
        folder = os.path.exists(html_path)
        if not folder:
            os.makedirs(html_path)
        with open(html_path+'/'+name+'.html', 'wb') as f:
            f.write(html)
        self.html_to_pdf(html_path,name)


    def html_to_pdf(self,html_path,name):
        html_name=html_path+'/'+name+'.html'
        pdf_path='D:/gjtjj/pdf'
        folder = os.path.exists(pdf_path)
        if not folder:
            os.makedirs(pdf_path)
        pdf_name=pdf_path+'/'+name+'.pdf'
        pdfkit.from_file(html_name, pdf_name)










