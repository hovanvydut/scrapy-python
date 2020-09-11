import scrapy
from ..items import Diemthi2020ThuathienhueItem
# thu vien: scrapy-fake-useragent


class DiemthiTtHueSpider(scrapy.Spider):
    name = 'diemthi.spider'
    count = 33007702
    sbd_max = 33012576
    origin_url = 'https://vietnamnet.vn/vn/giao-duc/tra-cuu-diem-thi-thpt/?y=2020&sbd='

    def start_requests(self):
        urls = [DiemthiTtHueSpider.origin_url + str(DiemthiTtHueSpider.count)]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        item = Diemthi2020ThuathienhueItem()
        item['sbd'] = DiemthiTtHueSpider.count
        item['toan'] = response.css('table.thpt td:nth-child(1)::text').get()
        item['van'] = response.css('table.thpt td:nth-child(2)::text').get()
        item['ngoai_ngu'] = response.css('table.thpt td:nth-child(3)::text').get()
        item['vat_li'] = response.css('table.thpt td:nth-child(4)::text').get()
        item['hoa_hoc'] = response.css('table.thpt td:nth-child(5)::text').get()
        item['sinh_hoc'] = response.css('table.thpt td:nth-child(6)::text').get()
        item['lich_su'] = response.css('table.thpt td:nth-child(7)::text').get()
        item['dia_li'] = response.css('table.thpt td:nth-child(8)::text').get()
        item['gdcd'] = response.css('table.thpt td:nth-child(9)::text').get()
        yield item
        DiemthiTtHueSpider.count += 1
        if DiemthiTtHueSpider.count <= DiemthiTtHueSpider.sbd_max:
            yield response.follow(url=DiemthiTtHueSpider.origin_url + str(DiemthiTtHueSpider.count), callback=self.parse, meta={
                'dont_redirect': True,
                'handle_httpstatus_list': [301, 302]
            })
