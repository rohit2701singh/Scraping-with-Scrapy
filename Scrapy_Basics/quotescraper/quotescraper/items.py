# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class QuotescraperItem(scrapy.Item):
    # define the fields for your item here like:
    author = scrapy.Field()
    text = scrapy.Field()
    tags = scrapy.Field()
