import re
import time

allChannels = ["china", "world","photo", "mil", "column", "finance", "culture", "science", "sports","ihl","society"]
denyChannels = ["photo","society"]



class SpiderBehavior:
    CONTENT = 1
    LIST = 2
    DENY = 3


class Rule:

    def __init__(self, url):
        self.url = url
        self.publish_time = None
        self.channel = self.get_channel(url)
        self.behavior = self.get_behavior(url,self.channel)

    def get_channel(self, url):
        for channel in allChannels:
            match_obj = re.search(re.compile(channel), url)
            if match_obj is not None:
                return channel
        return None

    def get_behavior(self, url, channel):
        if re.search(r'^.+\.(html|shtml)$', url) is None:
            return SpiderBehavior.DENY
        if channel is not None and channel in denyChannels:
            return SpiderBehavior.DENY
        else:
            url_segments = url.split("/")
            if len(url_segments) > 2 and self.is_date(url_segments[-2]):
                if(len(url_segments[-2]) == 8):
                    time_str = url_segments[-2][0:4]+'-'+url_segments[-2][4:6]+'-'+url_segments[-2][6:8]
                else:
                    time_str = url_segments[-3]+'-'+url_segments[-2][0:2]+'-'+url_segments[-2][2:4]
                self.publish_time = time_str
                return SpiderBehavior.CONTENT
            else:
                return SpiderBehavior.LIST

    def is_date(self,str_arg):
        length = len(str_arg)
        pattern = re.compile('\\d{' + str(length) + '}')
        if re.match(pattern, str_arg) is None:
            return False
        if length != 4 and length != 8:
             return False
        sub_str = str_arg[-4:]
        if sub_str >= "0101" and sub_str <= "1230":
            return True
        else:
            return False


if __name__ == "__main__":

    url = "http://www.cankaoxiaoxi.com/busy.html"
    rule = Rule(url)
    print(rule.publish_time)
    print(rule.channel)
    print(rule.behavior)
