# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import os
import json
import codecs


from .items import HexunFundItem, HexunFundDetailItem

# class FinanceDataPipeline(object):
#     def process_item(self, item, spider):
#         return item

class HexunFundPipeline(object):
    '''
        导出json文件
    '''

    @classmethod
    def from_settings(cls, settings):
        data_dir = settings['DATA_DIR']
        return cls(data_dir)

    def __init__(self, data_dir):
        file_name = os.path.join(data_dir, 'fund.json')
        self.file = codecs.open(file_name, 'w', encoding="utf-8")

        detail_file_name = os.path.join(data_dir, 'fund_detail.json')
        self.detail_file = codecs.open(detail_file_name, 'w', encoding="utf-8")

    def process_item(self, item, spider):
        lines = json.dumps(dict(item), ensure_ascii=False) + "\r\n"
        if isinstance(item, HexunFundItem):
            self.file.write(lines)
        if isinstance(item, HexunFundDetailItem):
            self.detail_file.write(lines)
        return item

    def spider_closed(self, spider):
        self.file.close()
        self.detail_file.close()
