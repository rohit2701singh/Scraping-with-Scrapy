import scrapy
from scrapy.http import FormRequest
from scrapy.utils.response import open_in_browser


class LoginSpider(scrapy.Spider):
    name = 'login_quotes'
    start_urls = ['https://quotes.toscrape.com/login']

    def parse(self, response):
        # Send a POST request with the login form
        return FormRequest.from_response(
            response,
            formdata={'username': 'admin', 'password': 'admin'},
            callback=self.after_login
        )

    def after_login(self, response):
        # We're now logged in if credentials are correct
        if "Logout" in response.text:
            self.logger.info("✅ Login successful!")
        else:
            self.logger.error("❌ Login failed!")

        # Proceed to scrape after login
        return response.follow("/tag/humor/", callback=self.parse_quotes)

    def parse_quotes(self, response):
        open_in_browser(response)   # open page in browser
        # for quote in response.css("div.quote"):
        #     yield {
        #         "author": quote.css("small::text").get(),
        #         "text": quote.css("span.text::text").get(),
        #         "tags": quote.css("a.tag::text").getall(),
        #     }
