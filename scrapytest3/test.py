from urllib import request

import chardet

from scrapytest3.spiders.content_parse import search_content_xpath, guess_content

RULE_TEXT = './text() | .//p[not(@style) or @style!="display: none;"]//text()[not(ancestor::li) and not(' \
            'parent::script) and not(parent::a) and not(parent::style)] | .//div/text()[not(ancestor::li)] '
url = "http://stock.hexun.com/2018-12-17/195567725.html"  # 网页地址
wp = request.urlopen(url)  # 打开连接
response = wp.read()
# encoding = chardet.detect(text)['encoding']
# response = text.decode(encoding, 'ignore')
content_xpaths = search_content_xpath(response)
if not content_xpaths:
    dic = search_content_xpath(response)
    paragraphs = dic['paras']
    content_xpaths.append(dic['xpath'])
else:
    for xpath in content_xpaths:
        content_div = response.xpath(xpath)
        if guess_content(content_div):
            paragraphs = content_div.xpath(RULE_TEXT).extract()
            break
        else:
            dic = search_content_xpath(response)
            paragraphs = dic['paras']
            content_xpaths.append(dic['xpath'])
print(paragraphs)