# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from scrapy.http import HtmlResponse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter

options = webdriver.ChromeOptions()
# options.add_argument('headless')
options.add_argument('window-size=1200x600')
# remember driver.quit() after finish
driver = webdriver.Chrome(chrome_options=options)


class FahashaSpiderMiddleware:
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

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
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


class FahashaDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(s.spider_closed, signal=signals.spider_closed)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        if request.url != 'https://www.fahasa.com':
            return None
        driver.implicitly_wait(10)
        driver.get(request.url)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".ma-box-content"))
        )
        scroll_2(driver, 1)
        body = driver.page_source

        return HtmlResponse(driver.current_url, body=body, encoding='utf-8', request=request)

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        # return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)

    def spider_closed(self, spider):
        spider.logger.info('Spider closed: %s' % spider.name)
        driver.quit()

def scroll_1(driver_selenium, timeout):
    scroll_pause_time = timeout

    # Get scroll height
    last_height = driver_selenium.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to bottom
        # driver_selenium.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        driver_selenium.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(scroll_pause_time)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver_selenium.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            # If heights are the same it will exit the function
            break
        last_height = new_height


def scroll_2(driver_selenium, timeout):
    scroll_pause_time = timeout

    # Get scroll height
    window_height = driver_selenium.execute_script("return window.innerHeight")
    scroll_height = driver_selenium.execute_script("return document.documentElement.scrollTop")
    offset_height = driver_selenium.execute_script("return document.body.offsetHeight")
    start = 500
    while window_height + scroll_height < offset_height:
        # Scroll down to bottom
        driver_selenium.execute_script("window.scrollTo(0, {});".format(start))

        start = start + 500
        # Wait to load page
        time.sleep(scroll_pause_time)

        window_height = driver_selenium.execute_script("return window.innerHeight")
        scroll_height = driver_selenium.execute_script("return document.documentElement.scrollTop")
        offset_height = driver_selenium.execute_script("return document.body.offsetHeight")

