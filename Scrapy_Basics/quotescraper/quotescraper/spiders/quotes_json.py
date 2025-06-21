# method-2 (shortcut to the start method)

# Instead of implementing a start() method that yields Request objects from URLs, you can define a start_urls class attribute with a list of URLs.
# This list will then be used by the default implementation of start() to create the initial requests for your spider.

import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = [
        "https://quotes.toscrape.com/tag/humor/",
    ]

    def parse(self, response, **kwargs):
        for quote in response.css("div.quote"):
            yield {
                "author": quote.xpath("span/small/text()").get(),
                "text": quote.css("span.text::text").get(),
                "tags": quote.css("div.tags a.tag::text").getall(),
            }

        next_page = response.css('li.next a::attr("href")').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)


# Items in Scrapy
# items.py is where you define the data fields (structure) you want to extract from a website.
# run this below spider from bash: scrapy crawl new_quotes -o output/jsonl_files/allNewQuotes.jsonl

from ..items import QuotescraperItem

class NewQuotesSpider(scrapy.Spider):
    name = "new_quotes"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = [
        "https://quotes.toscrape.com/",
    ]

    def parse(self, response, **kwargs):
        for quote in response.css("div.quote"):
            item = QuotescraperItem()
            item["author"] = quote.xpath("span/small/text()").get()
            item["text"] = quote.css("span.text::text").get()
            item["tags"] = quote.css("div.tags a.tag::text").getall()
            yield item

        next_page = response.css('li.next a::attr("href")').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)
