# encoding=utf-8
"""经济普查公报"""
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
    name = "qgrkpcSpider"


    def start_requests(self):
        url = "http://www.stats.gov.cn/tjsj/tjgb/rkpcgb/qgrkpcgb/"
        yield Request(url=url, callback=self.parse, dont_filter=True)

    def parse(self, response):
        selector = Selector(response)
        urls=selector.xpath('//ul[@class="center_list_contlist"]/li/a/@href').extract()

        for item in urls:
            if "./" in item:
                url="http://www.stats.gov.cn/tjsj/tjgb/rkpcgb/qgrkpcgb/"+item.split("./")[1]
            else:
                url="http://www.stats.gov.cn"+item
            yield Request(url=url,callback=self.parse_url_to_html)



    def parse_url_to_html(self, response):
        """
        解析URL，返回HTML内容
        """

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
        # name=re.sub('[\s+\.\!\/_,$%^*+\"\')]+|[+——\|?【】“”！，。？:：、~@#￥%……&*>]+', '',title)
        name = re.sub('[\s+\!\/_,$%^*(+\"\')]+|[+——()\|?【】“”！，？:：、~@#￥%……&*（）>]+', '', title)
        name = name.replace(".", "。")
        html_path = 'D:/gjtjj/qgrkpc/html'
        folder = os.path.exists(html_path)
        if not folder:
            os.makedirs(html_path)
        with open(html_path+'/'+name+'.html', 'wb') as f:
            f.write(html)
        self.html_to_pdf(html_path,name)


    def html_to_pdf(self,html_path,name):
        html_name=html_path+'/'+name+'.html'
        pdf_path='D:/gjtjj/qgrkpc/pdf'
        folder = os.path.exists(pdf_path)
        if not folder:
            os.makedirs(pdf_path)
        pdf_name=pdf_path+'/'+name+'.pdf'
        pdfkit.from_file(html_name, pdf_name)










