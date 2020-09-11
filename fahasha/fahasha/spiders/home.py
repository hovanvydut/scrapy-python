import scrapy

# Cac thu vien:
# scrapy-fake-useragent
# selenium

# enable middleware


class HomeSpider(scrapy.Spider):
    name = 'home'

    def start_requests(self):
        urls = ['https://www.fahasa.com']
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        boxs = response.css('.ma-box-content')
        for box in boxs:
            title = HomeSpider.get_title_book(box)
            yield {'title': title}

    @staticmethod
    def get_title_book(box):
        x = box.css('.product-name-no-ellipsis a::text')
        if x is None:
            x = box.css('.product-name-no-ellipsis font > font::text')
        return x.get()
