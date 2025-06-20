from pathlib import Path
import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes_html"

    async def start(self):
        urls = [
            "https://quotes.toscrape.com/page/1/",
            "https://quotes.toscrape.com/page/2/",
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response, **kwargs):
        page = response.url.split("/")[-2]
        filename = f"quotes-{page}.html"

        # Make sure the folder 'output/html_files' exists or create it
        output_dir = Path("output/html_files")
        output_dir.mkdir(parents=True, exist_ok=True)  # creates folder if not exists

        file_path = output_dir / filename
        file_path.write_bytes(response.body)
        self.log(f"Saved file {filename}")
