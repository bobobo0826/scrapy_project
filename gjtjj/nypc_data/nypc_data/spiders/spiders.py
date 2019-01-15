# encoding=utf-8
"""地方人口普查"""
import re
import datetime
import urllib

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
    name = "nypcSpider"


    def start_requests(self):
        url = "http://www.stats.gov.cn/tjsj/tjgb/nypcgb/"
        yield Request(url=url, callback=self.parse, dont_filter=True)

    def parse(self, response):
        selector = Selector(response)
        urls=selector.xpath('//ul[@class="center_list_contlist"]/li/a/@href').extract()
        for item in urls:
            if "./" in item:
                url="http://www.stats.gov.cn/tjsj/tjgb/nypcgb/"+item.split("./")[1]
                yield Request(url=url,callback=self.parse_url_to_html)




    def parse_url_to_html(self, response):
        """
        解析URL，返回HTML内容
        """

        selector=Selector(response)
        text0=selector.xpath('//div[@class="center"]').extract_first()
        # 标题
        title = selector.xpath('//h2[@class="xilan_tit"]/text()').extract_first()

        url = response.url.split("/")
        start_url = ''
        for index in range(len(url) - 1):
            start_url = start_url + url[index] + "/"

        html = text0.replace('lang="EN-US"','').replace("楷体","宋体").replace("(res://ietag.dll/#34/#1001)","")
        # body中的img标签的src相对路径的改成绝对路径
        soup = BeautifulSoup(response.text, 'html.parser')
        imgs=soup.find_all('img')
        for each in imgs:
            if "_r75" in each.get('src'):
                src=each.get('src').split("/")[1]
                whole_url=start_url+src
                html=html.replace(each.get('src'),whole_url)

        html = html_template.format(content=html)
        html = html.encode("utf-8")
        name = re.sub('[\s+\!\/_,$^*+\"\')]+|[+——\|?【】“”！，？:：、~@#￥……&*>]+', '', title)
        name = name.replace(".", "。")
        html_path = 'D:/gjtjj/nypc/html'
        pdf_path = 'D:/gjtjj/nypc/pdf'
        folder1 = os.path.exists(html_path)
        if not folder1:
            os.makedirs(html_path)
        folder2= os.path.exists(pdf_path)
        if not folder2:
            os.makedirs(pdf_path)
        html_name = html_path + '/' + name + '.html'
        html_name=self.check_filename_available(html_name,0)
        with open(html_name, 'wb') as f:
            f.write(html)
        pdf_name = pdf_path + '/' + name + '.pdf'
        pdf_name=self.check_filename_available(pdf_name,0)
        self.html_to_pdf(html_name,pdf_name)
        if "相关附件" in text0:
            fujian=selector.xpath('//ul[@class="wenzhang_list"]/li/a')
            for i in fujian:
                fujian_url=i.xpath('@href').extract_first()
                fujian_name=i.xpath('text()').extract_first()
                download_url=start_url+fujian_url.split("./")[1]
                if ".pdf" in download_url or ".doc" in download_url or ".xlsx" in download_url:
                    self.download(download_url,name,fujian_name,pdf_path)



    def html_to_pdf(self,html_name,pdf_name):
        pdfkit.from_file(html_name, pdf_name)

    def download(self,download_url,name,fujian_name,pdf_path):
        user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:53.0) Gecko/20100101 Firefox/53.0"
        headers = {"User-agent": user_agent}
        req = urllib.request.Request(download_url, headers=headers)
        u = urllib.request.urlopen(req)
        f = open(pdf_path+'/'+name+'-'+'附件：'+fujian_name, 'wb')
        if '.pdf' in download_url:
            block_sz = 8192
            while True:
                buffer = u.read(block_sz)
                if not buffer:
                    break
                f.write(buffer)
            f.close()
            print("Sucessful to download pdf")
        if '.xlsx' in download_url or '.doc' in download_url:
            data = u.read()
            f.write(data)
            print("Sucessful to download xlsx/doc")

    def check_filename_available(self,filename,n):
        file_name_new = filename
        if os.path.exists(filename):
            n=n+1
            file_name_new = filename[:filename.rfind('.')] + '_'+str(n) + filename[filename.rfind('.'):]
            return self.check_filename_available(file_name_new,n)
        else:
            return file_name_new











