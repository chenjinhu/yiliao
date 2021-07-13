import hashlib
import scrapy
import sys
# scrapy redis
from scrapy_redis.spiders import RedisSpider

# ************ Logger
from loguru import logger
# logger.remove()  # 删去import logger之后自动产生的handler，不删除的话会出现重复输出的现象
# handler_id = logger.add(sys.stderr, level="DEBUG")  # 添加一个可以修改控制的handler
# ********************

class CheckPhoneSpider(RedisSpider):
    name = 'check_phone'

    allowed_domains = ['changtalk.com']
    redis_key = 'list_china_phone'

    def make_requests_from_url(self, phone):
        cloudtoken = 'FmDiUHlIhCZpbgFYdpFXKKkwIz3EgUH594pjul0kgLs=@iyzc.cn.rongnav.com;iyzc.cn.rongcfg.com'
        uid = '81678'
        path = '/im/v1/users/query/86/' + str(phone)
        mactoken = self.md5encrypt(cloudtoken, uid, path)
        headers = {
            'mactoken': mactoken,
            'cloudtoken': cloudtoken,
            'user-agent': 'okhttp/3.11.0',
            'Host': 'www.changtalk.com'
        }
        return scrapy.Request('https://www.changtalk.com' + path, headers=headers, callback=self.parse,
                             meta={'phone': phone})
    def parse(self, response):
        phone = response.meta['phone']

        statu = True if len(response.text) > 0 else False

        if statu:
            print("{} 已注册".format(phone))
            logger.info("{} 已注册".format(phone))
        else:
            logger.debug("{} 未注册".format(phone))



    def md5encrypt(self, cloudtoken, uid, path):
        data = cloudtoken + uid + path
        data = data.encode()
        return hashlib.md5(data).hexdigest()
