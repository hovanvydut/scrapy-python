# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import sqlite3


class Diemthi2020ThuathienhuePipeline:
    def __init__(self):
        self.create_connect()
        self.create_table()

    def create_connect(self):
        self.conn = sqlite3.connect('diem_thi.db')
        self.curr = self.conn.cursor()

    def create_table(self):
        # self.curr.execute("""
        #     DROP TABLE IF EXISTS DIEM_THI_TT_HUE
        # """)
        self.curr.execute("""
            CREATE TABLE IF NOT EXISTS DIEM_THI_TT_HUE (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sbd TEXT,
                toan TEXT,
                van TEXT,
                ngoai_ngu TEXT,
                vat_li TEXT,
                hoa_hoc TEXT,
                sinh_hoc TEXT,
                lich_su TEXT,
                dia_li TEXT,
                gdcd TEXT
            )
        """)

    def store_db(self, item):
        self.curr.execute("""
            INSERT INTO DIEM_THI_TT_HUE 
            (sbd, toan, van, ngoai_ngu, vat_li, hoa_hoc, sinh_hoc, lich_su, dia_li, gdcd)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            item['sbd'],
            item['toan'],
            item['van'],
            item['ngoai_ngu'],
            item['vat_li'],
            item['hoa_hoc'],
            item['sinh_hoc'],
            item['lich_su'],
            item['dia_li'],
            item['gdcd']
        ))
        self.conn.commit()

    def process_item(self, item, spider):
        self.store_db(item)
        return item
