# -*- coding: utf-8 -*-
import json
import scrapy
from scrapy.http import Request
from scrapy.loader import ItemLoader


from ..items import HexunFundItem
from ..items import HexunFundDetailItem, HexunFundDetailItemLoader


class HexunFundSpider(scrapy.Spider):
    name = 'hexun_fund'
    allowed_domains = ['jingzhi.funds.hexun.com']
    start_urls = ['http://jingzhi.funds.hexun.com/jz/kaifang.htm']

    currency_url = 'http://jingzhi.funds.hexun.com/jz/JsonData/HuobiJingz.aspx?subtype={}'
    non_currency_url = 'http://jingzhi.funds.hexun.com/jz/JsonData/KaifangJingz.aspx?subtype={}'

    def parse(self, response):
        '''
        根据不同基金类型去获取请求url, 然后发送请求。
        '''
        fund_types = response.css('.fundSecNav a')

        urls = {}
        for tag in fund_types[1:]:
            type_number = tag.css('::attr(tit)').extract_first()
            type_text = tag.css('::text').extract_first().strip()

            if int(type_number) >= 40:
                url = self.currency_url.format(type_number)
            else:
                url = self.non_currency_url.format(type_number)
            urls.update({url: type_text})

        for url, type_text in urls.items():
            yield Request(url=url, callback=self.parse_fund_item, meta={'fund_type_text': type_text})

    def parse_fund_item(self, response):
        fund_data = json.loads(response.text[9:-1])

        fund_type = response.meta.get("fund_type_text", "")

        # 提取基金的具体字段
        for fund_item in fund_data["list"]:
            item = HexunFundItem()
            item["fund_type"] = fund_type
            item["fund_code"] = fund_item["fundCode"]
            item["fund_name"] = fund_item["fundName"]
            item["fund_link"] = fund_item["fundLink"]
            item["trend_link"] = fund_item["trendLink"]
            item["ba_link"] = fund_item["baLink"]
            item["t_net"] = fund_item["tNet"]
            item["t_amass"] = fund_item["tAmass"]
            item["b_net"] = fund_item["bNet"]
            item["b_amass"] = fund_item["bAmass"]
            item["day_price"] = fund_item["dayPrice"]
            item["this_year"] = fund_item["thisyear"]
            item["cx_level"] = fund_item["cxLevel"]
            item["buy_status"] = fund_item["buyStatus"]
            item["redeem_status"] = fund_item["redeemStatus"]
            item["discount"] = fund_item["discount"]
            item["rate_fee"] = fund_item["ratefee"]

            request = Request(url=item["fund_link"], callback=self.parse_fund_detail)
            request.meta['selenium'] = True
            yield request
            yield item

    def parse_fund_detail(self, response):

        item_loader = HexunFundDetailItemLoader(item=HexunFundDetailItem(), response=response)
        item_loader.add_css('fund_name', ".crumb span::text")
        item_loader.add_css('fund_code', ".crumb span::text")
        item_loader.add_css('fund_type', '.listnum table tr:nth-child(2) td:nth-child(2)::text')
        item_loader.add_css('fund_style', '.listnum table tr:nth-child(2) td:nth-child(4)::text')
        item_loader.add_xpath('found_date', "//span[@id='signdate']/text()")
        item_loader.add_css('manager', '.listnum table tr:nth-child(2) td:nth-child(6) a::text')
        item = item_loader.load_item()
        yield item
