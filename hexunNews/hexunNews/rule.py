import re


class SpiderBehavior:
    CONTENT = 1
    LIST = 2
    DENY = 3


pattern = re.compile("hexun.com")
content_list=["news.hexun.com","roll.hexun.com","stock.hexun.com","funds.hexun.com","p2p.hexun.com","tech.hexun.com",
              "futures.hexun.com","crudeoil.hexun.com","insurance.hexun.com","bank.hexun.com","opinion.hexun.com",
              "money.hexun.com","trust.hexun.com","bond.hexun.com","iof.hexun.com","dazong.hexun.com","qizhi.hexun.com",
              "gold.hexun.com","forex.hexun.com","nj.house.hexun.com","auto.hexun.com","haiwai.hexun.com"]
deny_list=[".jpg","bbs.hexun.com","t.hexun.com","jingzhi.funds.hexun.com","qq.com","fmall.hexun.com","yanbao","licaike","stockdata","http://bwh.photo.hexun.com/"]
class Rule:

    def __init__(self, url):
        self.url = url
        self.behavior = self.get_behavior(url)

    def get_behavior(self, url):
        for j in deny_list:
            if j in url:
                return SpiderBehavior.DENY
        if re.search(pattern, url) is None:
            return SpiderBehavior.DENY
        if re.search('\d{4}-\d{2}-\d{2}', url):
            for i in content_list:
                if i in url:
                    return SpiderBehavior.CONTENT

        return SpiderBehavior.LIST


if __name__ == "__main__":
    a = "dasjfjasdf"
    b = a.split("/")
    print(b)