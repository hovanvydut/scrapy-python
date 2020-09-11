import scrapy
import re
from ..items import AmazonItem

# Thu vien:scrapy-fake-useragent

class BookSpider(scrapy.Spider):
    name = 'book.spider'

    def start_requests(self):
        urls = [
            'https://www.amazon.com/s?bbn=283155&rh=n%3A283155%2Cp_n_publication_date%3A1250226011&dc&fst=as%3Aoff'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        container_dom = response.css("div[class='a-section a-spacing-medium']")

        for row in container_dom:
            detail_page_link = 'https://www.amazon.com' + row.css('a.a-link-normal.a-text-normal::attr(href)').get()
            yield scrapy.Request(url=detail_page_link, callback=self.parse_detail_page)

        next_page = response.css('.a-last a::attr(href)').get()
        url_next_page = 'https://www.amazon.com' + str(next_page)
        if next_page is not None:
            yield scrapy.Request(url=url_next_page, callback=self.parse)

    def parse_detail_page(self, response):
        items = AmazonItem()

        items['title'] = (response.css('#productTitle::text').get()).strip()
        items['link_img'] = response.css('#imgBlkFront::attr(src)').get()
        items['author'] = ','.join(response.css('.contributorNameID::text').getall()).strip()
        if items['author'] == '':
            items['author'] = ','.join(response.css('#bylineInfo .a-link-normal::text').getall())

        name_format_edition = response.css('#twister .a-color-base::text').getall()
        price_format_edition = response.css('#twister .a-color-price::text').getall()
        edition_price = dict(zip(name_format_edition, price_format_edition))
        items['hardcover_price'] = self.get_price_format_edition('hardcover', edition_price)
        items['kindle_price'] = self.get_price_format_edition('kindle', edition_price)
        items['paperback_price'] = self.get_price_format_edition('paper', edition_price)
        items['audiobook_price'] = self.get_price_format_edition('audio', edition_price)
        items['product_link'] = response.url
        yield items

    @staticmethod
    def get_price_format_edition(name_format, arr):
        x = [value for key, value in arr.items() if re.search(".*" + name_format + ".*", key.lower())]
        if len(x) != 0:
            return x[0].strip()
        else:
            return None
