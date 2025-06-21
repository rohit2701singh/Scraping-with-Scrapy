import scrapy
from ..items import QuoteItem

class AdvanceQuotesSpider(scrapy.Spider):
    name = "custom_quotes"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["https://quotes.toscrape.com/tag/humor/"]

    custom_settings = {
        'FEEDS': {
            'output_files/files_CustomSettings/quotes.jsonl': {
                'format': 'jsonlines',
                'overwrite': True,
            }
        }
    }

    def parse(self, response, **kwargs):
        for quote in response.css("div.quote"):
            item = QuoteItem()
            item["author"] = quote.xpath("span/small/text()").get()
            item["text"] = quote.css("span.text::text").get()
            item["tags"] = quote.css("div.tags a.tag::text").getall()
            yield item

        next_page = response.css('li.next a::attr("href")').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)



