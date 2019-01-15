import re


class SpiderBehavior:
    CONTENT = 1
    LIST = 2
    DENY = 3


pattern = re.compile("cctv.com")
content_list=["news.cctv.com","sports.cctv.com","military.cctv.com","jingji.cctv.com","opinion.cctv.com","travel.cctv.com","food.cctv.com","arts.cctv.com","jiankang.cctv.com"]

class Rule:

    def __init__(self, url):
        self.url = url
        self.behavior = self.get_behavior(url)

    def get_behavior(self, url):
        if re.search(pattern, url) is None or "tv.cctv.com" in url or "english.cctv.com" in url or "espanol.cctv.com" in url or "tibetan,cctv.com" in url:
            return SpiderBehavior.DENY
        if re.search('\d{4}/\d{2}/\d{2}', url):
            for i in content_list:
                if i in url:
                    return SpiderBehavior.CONTENT
        return SpiderBehavior.LIST


if __name__ == "__main__":
    a = "dasjfjasdf"
    b = a.split("/")
    print(b)