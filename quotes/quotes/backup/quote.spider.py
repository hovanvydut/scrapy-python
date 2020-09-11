import scrapy
from ..items import QuotesItem


class QuoteSpider(scrapy.Spider):
    name = 'quotes'

    def start_requests(self):
        urls = ['http://quotes.toscrape.com/']

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
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

        next_page = response.css('li.next a::attr(href)').get()

        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(url=next_page, callback=self.parse)
