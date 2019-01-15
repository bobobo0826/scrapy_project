import re


class SpiderBehavior:
    CONTENT = 1
    LIST = 2
    DENY = 3


pattern = re.compile("huanqiu.com")
content_list=["world.huanqiu.com","china.huanqiu.com","mil.huanqiu.com","taiwan.huanqiu.com","opinion.huanqiu.com",
              "finance.huanqiu.com","tech.huanqiu.com","art.huanqiu.com","go.huanqiu.com","health.huanqiu.com"]
deny_list=["weapon"]
class Rule:

    def __init__(self, url):
        self.url = url
        self.behavior = self.get_behavior(url)

    def get_behavior(self, url):
        for i in deny_list:
            if i in url:
                return SpiderBehavior.DENY
        if re.search(pattern, url) is None:
            return SpiderBehavior.DENY
        if re.search('\d{4}-\d{2}', url):
            return SpiderBehavior.CONTENT

        return SpiderBehavior.LIST


if __name__ == "__main__":
    a = "dasjfjasdf"
    b = a.split("/")
    print(b)