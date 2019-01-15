import re


class SpiderBehavior:
    CONTENT = 1
    LIST = 2
    DENY = 3


pattern = re.compile("(www.xinhuanet.com)|(http://www.news.cn)")



class Rule:

    def __init__(self, url):
        self.url = url
        self.behavior = self.get_behavior(url)

    def get_behavior(self, url):
        if re.search(pattern, url) is None or "english" in url or "video" in url:
            return SpiderBehavior.DENY
        if re.search('\d{4}-\d{2}', url):
            return SpiderBehavior.CONTENT
        return SpiderBehavior.LIST


if __name__ == "__main__":
    a = "dasjfjasdf"
    b = a.split("/")
    print(b)