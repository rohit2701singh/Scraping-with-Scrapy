# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from .items import QuoteItem, BookItem


class AdvanceQuotesPipeline:
    def process_item(self, item, spider):
        if isinstance(item, QuoteItem):
            item['text'] = item['text'].replace('“', '').replace('”', '').strip()
            item['author'] = item['author'].upper()
        return item


class BookStorePipeline:
    def process_item(self, item, spider):
        if isinstance(item, BookItem):
            item['title'] = item['title'].strip()
            item['price'] = item['price'].replace('£', '').strip()
        return item

