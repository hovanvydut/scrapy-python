# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import sqlite3


class TikiPipeline:
    def __init__(self):
        self.connect_db()
        self.create_table()

    def connect_db(self):
        self.conn = sqlite3.connect('books.db')
        self.curr = self.conn.cursor()

    def create_table(self):
        self.curr.execute("""
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                authors TEXT,
                cover_type TEXT,
                link_img TEXT,
                price FLOAT,
                CURRENCY TEXT,
                CATEGORY TEXT,
                link_book TEXT
            )
        """)

    def store_db(self, item):
        self.curr.execute("""
            INSERT INTO books (title, authors, cover_type, link_img, price, currency, category, link_book)
            VALUES (?, ?, ?, ?, ?, ?, ? , ?)
        """, (
            item['title'],
            item['authors'],
            item['cover_type'],
            item['link_img'],
            item['price'],
            item['currency'],
            'sgk/dh_cd',
            item['link_book']
        ))
        self.conn.commit()
    def process_item(self, item, spider):
        self.store_db(item)
        return item
