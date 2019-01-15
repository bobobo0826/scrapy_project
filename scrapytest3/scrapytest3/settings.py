# -*- coding: utf-8 -*-

# Scrapy settings for scrapytest3 project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'scrapytest3'

SPIDER_MODULES = ['scrapytest3.spiders']
NEWSPIDER_MODULE = 'scrapytest3.spiders'
ROOT_DIR = 'D://news_data/'
LOG_LEVEL = "INFO"
LOG_FILE = 'xinhua_log.log'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False
COOKIES_ENABLES = False
# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'scrapytest3.pipelines.Scrapytest3Pipeline': 300,
}

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
DEPTH_PRIORITY = 1  # 广度爬取
HTTPCACHE_ENABLED = True
HTTPCACHE_EXPIRATION_SECS = 0
HTTPCACHE_DIR = 'httpcache'
HTTPCACHE_IGNORE_HTTP_CODES = []
HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
EXTENSIONS = {'scrapytest3.latencies.Latencies': 500, }
LATENCIES_INTERVAL = 5
