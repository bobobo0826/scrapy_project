# encoding=utf-8
import re
import datetime

from bs4 import BeautifulSoup
from scrapy.selector import Selector
from scrapy.http import Request
from scrapy.spiders import CrawlSpider

from xhdxNews.items import XhdxnewsItem

import time, os, logging
class Spider(CrawlSpider):
    name = "xhdxNewsSpider"
    allowed_domains =["mrdx.cn"]



    def start_requests(self):
        url="http://mrdx.cn/content/20181214/Articel03003BB.htm"
        yield Request(url=url,callback=self.parse6, dont_filter=True)
        # start = input("Enter your startTime(20181101):")
        # end = input("Enter your endTime(20181101):")
        # index = int(end)
        # while index >= int(start):
        #     cur = '%d' % index
        #     if int(cur[4] + cur[5]) <= 12 and 31 >= int(cur[6] + cur[7]) >= 1:
        #         url = "http://mrdx.cn/content/" + cur[0] + cur[1] + cur[2] + cur[3] + cur[4] + cur[5] + cur[6] + cur[7] + "/Page01HO.htm"
        #         yield Request(url=url, meta={'counter': 3}, callback=self.parse, dont_filter=True)
        #     index = index - 1
    def parse6(self,response):
        html=response.text
        content = self.filter_tags(html)
        print("111111111111111111111111")
        print(content)

        # 假设content为已经拿到的html
        # Ctext取周围k行(k<5),定为3
        blocksWidth = 3
        # 每一个Cblock的长度
        Ctext_len = []
        # Ctext
        lines = content.split('n')
        # 去空格

        for i in range(len(lines)):
            if lines[i] == ' ' or lines[i] == 'n':
                lines[i] = ''
        # 计算纵坐标，每一个Ctext的长度
        for i in range(0, len(lines) - blocksWidth):
            wordsNum = 0
            for j in range(i, i + blocksWidth):
                lines[j] = lines[j].replace("\s", "")
                wordsNum += len(lines[j])
            Ctext_len.append(wordsNum)
        # 开始标识
        start = -1
        # 结束标识
        end = -1
        # 是否开始标识
        boolstart = False
        # 是否结束标识
        boolend = False
        # 行块的长度阈值
        max_text_len = 88
        # 文章主内容
        main_text = []
        # 没有分割出Ctext
        if len(Ctext_len) < 3:
            return '没有正文'
        for i in range(len(Ctext_len) - 3):
            # 如果高于这个阈值
            if (Ctext_len[i] > max_text_len and (not boolstart)):
                # Cblock下面3个都不为0，认为是正文
                if (Ctext_len[i + 1] != 0 or Ctext_len[i + 2] != 0 or Ctext_len[i + 3] != 0):
                    boolstart = True
                    start = i
                    continue
            if (boolstart):
                # Cblock下面3个中有0，则结束
                if (Ctext_len[i] == 0 or Ctext_len[i + 1] == 0):
                    end = i
                    boolend = True
            tmp = []
            # 判断下面还有没有正文
            if (boolend):
                for ii in range(start, end + 1):
                    if (len(lines[ii]) < 5):
                        continue
                    tmp.append(lines[ii] + "n")
                str = "".join(list(tmp))
                # 去掉版权信息
                if ("Copyright" in str or "版权所有" in str):
                    continue
                main_text.append(str)
                boolstart = boolend = False
        # 返回主内容
        result = "".join(list(main_text))




    def filter_tags(self,htmlstr):
        # 先过滤CDATA
        re_cdata = re.compile('//<!\[CDATA\[[^>]*//\]\]>', re.I)  # 匹配CDATA
        re_script = re.compile('<\s*script[^>]*>[^<]*<\s*/\s*script\s*>', re.I)  # Script
        re_style = re.compile('<\s*style[^>]*>[^<]*<\s*/\s*style\s*>', re.I)  # style
        re_br = re.compile('<br\s*?/?>')  # 处理换行
        re_h = re.compile('</?\w+[^>]*>')  # HTML标签
        re_comment = re.compile('<!--[^>]*-->')  # HTML注释
        s = re_cdata.sub('', htmlstr)  # 去掉CDATA
        s = re_script.sub('', s)  # 去掉SCRIPT
        s = re_style.sub('', s)  # 去掉style
        s = re_br.sub('\n', s)  # 将br转换为换行
        s = re_h.sub('', s)  # 去掉HTML 标签
        s = re_comment.sub('', s)  # 去掉HTML注释
        # 去掉多余的空行
        blank_line = re.compile('\n+')
        s = blank_line.sub('\n', s)
        s = self.replaceCharEntity(s)  # 替换实体
        return s

    ##替换常用HTML字符实体.
    # 使用正常的字符替换HTML中特殊的字符实体.
    # 你可以添加新的实体字符到CHAR_ENTITIES中,处理更多HTML字符实体.
    # @param htmlstr HTML字符串.
    def replaceCharEntity(self,htmlstr):
        CHAR_ENTITIES = {'nbsp': ' ', '160': ' ',
                         'lt': '<', '60': '<',
                         'gt': '>', '62': '>',
                         'amp': '&', '38': '&',
                         'quot': '"', '34': '"', }

        re_charEntity = re.compile(r'&#?(?P<name>\w+);')
        sz = re_charEntity.search(htmlstr)
        while sz:
            entity = sz.group()  # entity全称，如&gt;
            key = sz.group('name')  # 去除&;后entity,如&gt;为gt
        try:
            htmlstr = re_charEntity.sub(CHAR_ENTITIES[key], htmlstr, 1)
            sz = re_charEntity.search(htmlstr)
        except KeyError:
            # 以空串代替
            htmlstr = re_charEntity.sub('', htmlstr, 1)
            sz = re_charEntity.search(htmlstr)
        return htmlstr

    def repalce(s, re_exp, repl_string):
        return re_exp.sub(repl_string, s)




    def parse(self, response):
        selector = Selector(response)
        hrefs=selector.xpath('//a[@class="atitle"]/@href').extract()
        rr = re.compile(r'责任编辑：[\u4e00-\u9fa5]+\s*[\u4e00-\u9fa5]*')
        editors = rr.findall(response.text)
        i=0
        editor=''
        for href in hrefs:
            if "Page" in href:
                url=response.url.split("Page")[0]+href
                if i<len(editors):
                    editor=editors[i]
                i=i+1
                yield Request(url=url,meta={'editor': editor},callback=self.parse1,dont_filter=True)




    def parse1(self,response):
        selector = Selector(response)
        hrefs = selector.xpath('//a[@class="atitle"]/@href').extract()
        tt=selector.xpath('//*[@id="table5"]/tbody/tr/td[1]/strong/text()').extract_first()
        e=response.meta['editor']
        for href in hrefs:
            if "Artice" in href:
                url=response.url.split("Page")[0]+href
                yield Request(url=url,meta={'type': tt, 'editor': e},callback=self.parse2)

    def parse2(self,response):
        selector = Selector(response)
        XhdxnewsItems=XhdxnewsItem()
        XhdxnewsItems["url"]=response.url
        XhdxnewsItems["html"]=''
        XhdxnewsItems["type"]=response.meta['type']
        XhdxnewsItems["editor"]=response.meta['editor']
        XhdxnewsItems["content"]=''
        XhdxnewsItems["title"]=''
        XhdxnewsItems["datetime"]=''
        XhdxnewsItems["source"]=''

        XhdxnewsItems["title"]= selector.xpath('//*[@id="contenttext"]/font/table/tbody/tr[2]/td/div/strong/font/text()').extract_first()
        text0 = selector.xpath('//*[@id="contenttext"]/font/table/tbody/tr[5]/td/text()').extract_first()
        if text0:
            XhdxnewsItems["source"] = text0.split("稿件来源：")[1].strip()
            time=text0.split("稿件来源：")[0].split("（")[1].split("）")[0].strip()
            if re.match("^\d{4}-\d{2}-\d{2}$", time):
                ymd = time.split("-")
                XhdxnewsItems["datetime"] = "%s年%s月%s日" % (ymd[0], ymd[1], ymd[2])

        content = ''
        text1 = selector.xpath('//*[@id="contenttext"]/font/div[2]/text()').extract_first()
        if text1:
            content=content+text1+'\n'
        text2 = selector.xpath('//*[@id="contenttext"]/font/div[2]/p/text()').extract()
        if text2:
            content= content + "\r\n".join(text2)
        else:
            text3 = selector.xpath('//*[@id="contenttext"]/font/div[2]/div/text()').extract()
            if text3:
                content = content + "\r\n".join(text3)
        XhdxnewsItems["content"]="      "+content.lstrip()
        yield XhdxnewsItems

    def get_logger(domain, start_time=time.strftime('%Y%m%d%H%M%S', time.localtime())):
        start_time = start_time[:12]

        path = '/home/scrapy/scrapy_spider_logs/'
        if not os.path.exists(path):
            os.makedirs(path)
        path_log = path + start_time
        my_logger = logging.getLogger(domain)
        my_logger.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(filename)s[line:%(lineno)d] %(message)s')
        scrapy_logger = logging.getLogger('scrapy')
        # scrapy_logger = logging.getLogger()
        scrapy_logger.setLevel(logging.WARNING)
        handler_info = logging.FileHandler('%s_info.log' % path_log, 'a', encoding='UTF-8')
        handler_info.setLevel(logging.INFO)
        handler_info.setFormatter(formatter)
        my_logger.addHandler(handler_info)
        scrapy_logger.addHandler(handler_info)
        handler_warning = logging.FileHandler('%s_warning.log' % path_log, 'a', encoding='UTF-8')
        handler_warning.setLevel(logging.WARNING)
        handler_warning.setFormatter(formatter)
        my_logger.addHandler(handler_warning)
        scrapy_logger.addHandler(handler_warning)
        handler_error = logging.FileHandler('%s_error.log' % path_log, 'a', encoding='UTF-8')
        handler_error.setLevel(logging.ERROR)
        handler_error.setFormatter(formatter)
        my_logger.addHandler(handler_error)
        scrapy_logger.addHandler(handler_error)
        my_logger.info('Get my_logger success !!!')
        return my_logger
