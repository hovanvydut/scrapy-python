# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class AmazonItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    author = scrapy.Field()
    link_img = scrapy.Field()
    hardcover_price = scrapy.Field()
    kindle_price = scrapy.Field()
    audiobook_price = scrapy.Field()
    paperback_price = scrapy.Field()
    product_link = scrapy.Field()
