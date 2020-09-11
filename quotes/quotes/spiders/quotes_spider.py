import scrapy
from scrapy.http import FormRequest
from ..items import QuotesItem


# Enable pipeline trong file settings.py
# Thay user-agent trong file settings.py bang user-agent cua Goolgle Bot
# hoac dung thu vien scrapy-fake-useragent
# spider --> items(tempore container) --> pipeline --> store DB

# CLI:
# scrapy startproject crawl
# scrapy genspider quote http://quotes.toscrape.com/
# scrapy crawl quotes_spider -o abcxyz.csv

class QuoteSpider(scrapy.Spider):
    # spider's name
    name = 'quotes_spider'

    def start_requests(self):
        urls = ['http://quotes.toscrape.com/login']
        for url in urls:
            # sau khi gui request toi url --> server gui response --> callback self.parse excute voi response parameter
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # Dang nhap
        token = response.css('form > input::attr(value)').get()
        return FormRequest.from_response(response, formdata={
            'csrf_token': token,
            'username': 'hovanvydut',
            'password': '123456'
            #    Sau khi dang nhap thanh cong, server redirect sang trang khac, sau do goi
            #     ham self.start_scraping de cao cai trang vua moi duoc redirect
        }, callback=self.start_scraping)

    def start_scraping(self, response):
        # tempore container
        items = QuotesItem()

        all_div_quotes = response.css("div.quote")
        for div_quote in all_div_quotes:
            title = div_quote.css('span.text::text').get()
            author = div_quote.css('.author::text').get()
            tags = div_quote.css('.tag::text').getall()

            items['title'] = title
            items['author'] = author
            items['tags'] = tags
            yield items

        # crawl data next page
        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(url=next_page, callback=self.start_scraping)
