import scrapy
from ..items import BookItem
# scrapy-fake-useragent
# If want store into Database, please enable pipeline in settings.py


class BookSpider(scrapy.Spider):
    name = 'book'
    page = 1
    myUrl = 'https://tiki.vn/nong-lam-ngu-nghiep/c882' + '?page='
    countError = 0

    def start_requests(self):
        urls = [self.next_page_url()]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        if response.status == '404':
            BookSpider.countError += 1
            if BookSpider.countError <= 3:
                BookSpider.page += 1
                return scrapy.Request(url=self.next_page_url(), callback=self.parse)

        product_lists = response.css('.product-box-list .product-item')
        for product in product_lists:
            detail_page_url = 'https://tiki.vn' + product.css('a::attr(href)').get()
            yield scrapy.Request(url=detail_page_url, callback=self.parse_detail_page)

        next_btn = response.css('.next::attr(href)').get()
        if next_btn is not None:
            BookSpider.page += 1
            yield scrapy.Request(url=self.next_page_url(), callback=self.parse)

    @staticmethod
    def parse_detail_page(response):
        item = BookItem()
        item['title'] = response.css('h1.title::text').get()
        item['authors'] = response.css('h6:nth-child(1) a::text').get()
        item['cover_type'] = response.css('h6+ h6 a::text').get()
        item['link_img'] = response.css('.container img::attr(src)').get()
        tmp = response.css('meta[itemprop=price]::attr(content)').get()
        item['price'] = float(tmp) if tmp else None
        item['currency'] = response.css('meta[itemprop=priceCurrency]::attr(content)').get()
        item['link_book'] = response.url
        yield item

    @staticmethod
    def next_page_url():
        return BookSpider.myUrl + str(BookSpider.page)
