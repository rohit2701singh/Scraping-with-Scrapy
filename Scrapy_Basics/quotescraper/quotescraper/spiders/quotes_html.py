from pathlib import Path
import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes_html"

    def start_requests(self):
        urls = [
            "https://quotes.toscrape.com/page/1/",
            "https://quotes.toscrape.com/page/2/",
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response, **kwargs):
        page = response.url.split("/")[-2]
        filename = f"quotes-{page}.html"

        # __file__ points to quotes_html.py, .parent gives you spiders/, .parent.parent gives quotescraper/
        # Go up one level from the spider folder
        base_dir = Path(__file__).parent.parent
        output_dir = base_dir / "output_files" / "html_files"
        output_dir.mkdir(parents=True, exist_ok=True)

        file_path = output_dir / filename
        file_path.write_bytes(response.body)
        self.log(f"Saved file: {file_path}")
