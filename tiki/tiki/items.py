# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BookItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    authors = scrapy.Field()
    cover_type = scrapy.Field()
    link_img = scrapy.Field()
    price = scrapy.Field()
    currency = scrapy.Field()
    link_book = scrapy.Field()
