# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import sys

from itemadapter import ItemAdapter
# ************ Logger
from loguru import logger
# logger.remove()  # 删去import logger之后自动产生的handler，不删除的话会出现重复输出的现象
# handler_id = logger.add(sys.stderr, level="INFO")  # 添加一个可以修改控制的handler
# ********************

class YiliaoPipeline:
    def process_item(self, item, spider):
        logger.info(item)
        return item
