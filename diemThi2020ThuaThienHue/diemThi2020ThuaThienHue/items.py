# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Diemthi2020ThuathienhueItem(scrapy.Item):
    sbd = scrapy.Field()
    toan = scrapy.Field()
    van = scrapy.Field()
    ngoai_ngu = scrapy.Field()
    vat_li = scrapy.Field()
    hoa_hoc = scrapy.Field()
    sinh_hoc = scrapy.Field()
    lich_su = scrapy.Field()
    dia_li = scrapy.Field()
    gdcd = scrapy.Field()
    pass
