# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from scrapy.http import HtmlResponse
from scrapy.xlib.pydispatch import dispatcher
from scrapy.utils.project import get_project_settings

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class FinanceDataSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class SeleniumDownloaderMiddleware(object):
    '''
    selenium downloader
    '''

    def spider_closed(self, spider):
        '''
        当爬虫退出的时候关闭chrome
        '''
        print("spider closed")
        self.browser.quit()

    def spider_opened(self, spider):
        '''
        当爬虫开始的时候打开chrome
        '''
        # 设置不加载图片
        chrome_opt = Options()
        prefs = {"profile.managed_default_content_settings.images":2}
        chrome_opt.add_experimental_option("prefs", prefs)

        settings = get_project_settings()
        driver_path = settings.get('WEB_DRIVER_PATH')

        self.browser = webdriver.Chrome(executable_path=driver_path, chrome_options=chrome_opt)
        print("spider opened")

    @classmethod
    def from_crawler(cls, crawler):
        middleware = cls()
        crawler.signals.connect(middleware.spider_opened, signals.spider_opened)
        crawler.signals.connect(middleware.spider_closed, signals.spider_closed)
        return middleware

    def process_request(self, request, spider):
        if 'selenium' in request.meta:
            self.browser.get(request.url)
            WebDriverWait(self.browser, 0.5).until(EC.presence_of_element_located((By.ID, 'signdate')))
            # self.browser.implicitly_wait(2)
            return HtmlResponse(url=self.browser.current_url, body=self.browser.page_source, encoding='utf8', request=request)
