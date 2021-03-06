import os
import time,logging


# get my_logger
def get_logger(domain, start_time):
    print("-----------------getlogger-----------------")
    # 取出配置

    # 创建2个handle
    # logging.FileHandler 需要重新实现

    start_time = start_time[:12]
    path = '/scrapy_spider_logs/'
    if not os.path.exists(path):
        os.makedirs(path)
    path_log = path + start_time
    my_logger = logging.getLogger(domain)

    my_logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(filename)s[line:%(lineno)d] %(message)s')

    scrapy_logger = logging.getLogger('scrapy')
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

    handler_debug = logging.FileHandler('%s_debug.log' % path_log, 'a', encoding='UTF-8')
    handler_debug.setLevel(logging.DEBUG)
    handler_debug.setFormatter(formatter)
    my_logger.addHandler(handler_debug)
    scrapy_logger.addHandler(handler_debug)

    # my_logger.info('Get my_logger success !!!')
    return my_logger


if __name__=="__main__":
    start_time = time.strftime('%Y%m%d%H%M%S', time.localtime())
    my_logger = get_logger("XinHua",start_time)
    my_logger.info('Info logger')


    my_logger.warning('Warning logger')


    my_logger.error('Errorlogger')