# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html
import re
import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst, Join


class HexunFundItem(scrapy.Item):
    '''
     fields for hexun fund
    '''
    fund_type = scrapy.Field()
    fund_code = scrapy.Field()
    fund_name = scrapy.Field()
    fund_link = scrapy.Field()
    trend_link = scrapy.Field()
    ba_link = scrapy.Field() #（吧）
    t_net = scrapy.Field()
    t_amass = scrapy.Field()
    b_net = scrapy.Field() #上一日净值
    b_amass = scrapy.Field() #上一日累计净值
    day_price = scrapy.Field() #日涨跌
    this_year = scrapy.Field() # 今年回报
    cx_level = scrapy.Field() #晨星三年评级
    buy_status = scrapy.Field()
    redeem_status = scrapy.Field()
    discount = scrapy.Field()
    rate_fee = scrapy.Field() # 费率



class HexunFundDetailItemLoader(ItemLoader):
    #自定义itemloader
    default_output_processor = TakeFirst()


def get_code(value):
    match = re.match(r".*\((.*)\).*", value)
    return match.group(1)


def get_name(value):
    match = re.match(r"(.*)\(.*", value)
    return match.group(1)


class HexunFundDetailItem(scrapy.Item):
    '''
     fields for hexun fund detail
    '''
    fund_code = scrapy.Field(input_processor=MapCompose(get_code))
    fund_name = scrapy.Field(input_processor=MapCompose(get_name))
    fund_type = scrapy.Field()
    fund_style = scrapy.Field()
    found_date = scrapy.Field()
    manager = scrapy.Field(output_processor=Join(","))
