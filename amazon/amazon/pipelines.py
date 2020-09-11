# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import sqlite3


class AmazonPipeline:
    def __init__(self):
        self.create_connection()
        self.create_table()

    def create_connection(self):
        self.conn = sqlite3.connect('amazon_book.db')
        self.curr = self.conn.cursor()

    def create_table(self):
        self.curr.execute(""" DROP TABLE IF EXISTS AMAZON_BOOK""")
        self.curr.execute("""
            CREATE TABLE AMAZON_BOOK (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                author TEXT,
                link_img TEXT,
                hardcover_price TEXT,
                kindle_price TEXT,
                audiobook_price TEXT,
                paperback_price TEXT,
                product_link TEXT
            )
        """)

    def store_db(self, item):
        self.curr.execute("""
            INSERT INTO AMAZON_BOOK (title, author, link_img, hardcover_price, kindle_price, 
                                    audiobook_price, paperback_price, product_link)
            VALUES(?, ?, ?, ?, ?, ?, ?, ?)
            """, (
            item['title'],
            item['author'],
            item['link_img'],
            item['hardcover_price'],
            item['kindle_price'],
            item['audiobook_price'],
            item['paperback_price'],
            item['product_link']
        ))
        self.conn.commit()

    def process_item(self, item, spider):
        self.store_db(item)
        return item

