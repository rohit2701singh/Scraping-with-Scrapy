# Web Scraping using Scrapy

## What is Scrapy?
Scrapy is an open-source <u>**Python framework**</u> designed for web scraping and web crawling. It allows developers to efficiently extract structured data from websites, process it, and save it in formats like JSON, CSV, or databases. Scrapy provides tools to handle requests, follow links, and manage crawling rules, making it powerful for data mining, automated testing, and information gathering from the web.  
With Scrapy you write __Spiders__ to retrieve HTML pages from websites and scrape the data you want, clean and validate it, and store it in the data format you want.

## Creating Scrapy Project
Before you start scraping, you will have to set up a new Scrapy project. Enter a directory where you’d like to store your code and run:  
`scrapy startproject <project_name> <project directory name>` for e.g. `scrapy startproject quotescraper`

***Scrapy creates this folder structure:***

```markdown
quotescraper/
├── scrapy.cfg
└── quotescraper/
    ├── __init__.py
    ├── items.py
    ├── middlewares.py
    ├── pipelines.py
    ├── settings.py
    └── spiders/
        └── __init__.py

```

1. `quotescraper/` (outer folder): main project folder, you'll work inside it.
2. `scrapy.cfg` tells scrapy how to run your project. You don’t touch this much. Scrapy uses it to know:
   1. The name of your settings module
   2. Which project to run
3. `quotescraper/`(inner folder): **This is the real python package for your project.**
   1. `items.py` defines the structure of the data you want to scrape. Here you define the fields you want to scrape (e.g. quote, author, tag)
   2. `middlewares.py` handle how requests and responses are processed. (Advanced stuff: like adding custom headers, handling retries, rotating user agents)
   3. `pipelines.py` process scraped data after it's collected. 
   4. `settings.py` configure your spider's behaviour. For e.g. how fast to crawl, which pipelines to run, user-agent etc.
   5. `spiders/` **This is where your actual spider files go.** You create files here. Each spider defines:
      - The website to crawl
      - How to crawl it 
      - What data to extract
      
   
**`scrapy --help` command shows important commands we can use**

```shell
 scrapy --help
Scrapy 2.13.2 - no active project

Usage:
  scrapy <command> [options] [args]

Available commands:
  bench         Run quick benchmark test
  fetch         Fetch a URL using the Scrapy downloader
  genspider     Generate new spider using pre-defined templates
  runspider     Run a self-contained spider (without creating a project)
  settings      Get settings values
  shell         Interactive scraping console
  startproject  Create new project
  version       Print Scrapy version
  view          Open URL in browser, as seen by Scrapy


```

## Example Spider
- scraping a website https://quotes.toscrape.com/ 
- create a python file `quotes_spider.py` inside spiders folder.
- if we use `scrapy genspider <spider_name> <domain>`, it will quickly generate a template spider file.
- put below code inside the file
- run this file using `runspider` command: `scrapy runspider quotes_spider.py -o quotes.jsonl` or `scrapy crawl quotes -o quotes.jsonl`
- when this finishes you will have a `quotes.jsonl` file in JSON Line format, containing the text and author.
- manage output files separately: `scrapy crawl quotes -o output/jsonl_files/quotes.jsonl`

```python
import scrapy

class QuotesSpider(scrapy.Spider):
    name = "quotes"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = [
        "https://quotes.toscrape.com/tag/humor/",
    ]

    def parse(self, response):
        for quote in response.css("div.quote"):
            yield {
                "author": quote.xpath("span/small/text()").get(),
                "text": quote.css("span.text::text").get(),
            }

        next_page = response.css('li.next a::attr("href")').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)
```

### What just happened?
- When you ran the command `scrapy runspider quotes_spider.py`, Scrapy looked for a Spider definition inside it and ran it through its crawler engine.
- `name = "quotes"` defines a spider name. This can be used to run the spider via command line: `scrapy crawl quotes`. Name must be unique within a project.
- `allowed_domains` is an optional setting in your spider that restricts which domains the spider is allowed to crawl. Use it to avoid accidentally crawling unrelated or external websites.
- The crawl started by making requests to the URLs defined in the `start_urls` attribute and called the default callback method `parse`, passing the response object as an argument.
- `parse()` is Scrapy’s default callback method, which is called for requests without an explicitly assigned callback.
- In the `parse` callback, we loop through the quote elements using a <u>CSS Selector</u>, yield a Python dict with the extracted quote text and author.
- Look for a link to the next page and schedule another request using the same parse method as callback.
- `quote.css("span.text::text").get()`, we have added `::text` to the CSS query, this means we want to select only the text elements directly inside `span.text`.


## Extracting data using Scrapy Shell
- We can extract data with Scrapy using `Scrapy Shell`  
- In the terminal run: `scrapy shell "https://quotes.toscrape.com/tag/humor/"`

```bash
# In the bash terminal run: scrapy shell "https://quotes.toscrape.com/tag/humor/"

>>> response.css("title")
[<Selector query='descendant-or-self::title' data='<title>Quotes to Scrape</title>'>]

>>> response.css("title").getall()
['<title>Quotes to Scrape</title>']

>>> response.css("title").get()
'<title>Quotes to Scrape</title>'

>>> response.css("title::text").getall()
['Quotes to Scrape']

>>> response.css("title::text").get()
'Quotes to Scrape'

>>> view(response)
True

>>> response.xpath("//title")
[<Selector query='//title' data='<title>Quotes to Scrape</title>'>]

>>> response.xpath("//title/text()").get()
'Quotes to Scrape'

# extracting quotes, authors and tags
>>> quote = response.css("div.quote")[0]
>>> text = quote.css("span.text::text").get()
>>> text
'“The person, be it gentleman or lady, who has not pleasure in a good novel, must be intolerably stupid.”'

>>> author = quote.css("small.author::text").get()
>>> author
'Jane Austen'

>>> tags = quote.css("div.tags a.tag::text").getall()
>>> tags
['aliteracy', 'books', 'classic', 'humor']

# we can iterate over all the quote elements and put them together into a Python dictionary
>>> for quote in response.css("div.quote"):
...     text = quote.css("span.text::text").get()
...     author = quote.css("small.author::text").get()
...     tags = quote.css("div.tags a.tag::text").getall()
...     print(dict(text=text, author=author, tags=tags))
{'text': '“The person, be it gentleman or lady, who has not pleasure in a good novel, must be intolerably stupid.”', 'author': 'Jane Austen', 'tags': ['aliteracy', 'books', 'classic', 'humor']}
{'text': '“A day without sunshine is like, you know, night.”', 'author': 'Steve Martin', 'tags': ['humor', 'obvious', 'simile']}
....

```
### Explanation
- `response`: HTML response object Scrapy gets from a URL.
- `.css("title")`: a **CSS selector** that finds the `<title>` tag in the HTML.
- The result is a **SelectorList** (a list of selector objects)
- `response.css("title").getall()` returns a list of strings, each being the full HTML string of the matched tag.
- `response.css("title").get()` returns just the first match as a string.
- `response.css("title::text").getall()` returns a list of text contents inside the `title` tag.
- `response.css("title::text").get()` returns the first text content inside the `title` tag.
- `view(response)` opens the response HTML in your default web browser.


**Note:** 
- Besides CSS, Scrapy selectors also support using XPath expressions: `response.xpath("//title")`
- XPath expressions are very powerful, and are the foundation of Scrapy Selectors. In fact, CSS selectors are converted to XPath under-the-hood.

```shell
>>> response.css("div.quote")
>>> response.xpath("//div[@class='quote']")
```
Both return the same `<div class="quote">` blocks.

## Storing the scraped data
- Simplest way to store the scraped data by command: `scrapy crawl quotes -o quotes.jsonl`
- `scrapy crawl quotes` runs the spider named `quotes`. This is defined in your spider class.
- `-o quotes.jsonl` tells Scrapy to save the scraped data into a file named `quotes.jsonl` in **JSON Lines** format.
- JSON Lines is like JSON but <u>each line is a separate JSON object</u>.
- The `-O` command-line switch **overwrites** any existing file; use `-o` instead to **append** new content to any existing file. However, appending to a `JSON file(quotes.json)` makes the file contents invalid JSON. When appending to a file, consider using a different serialization format, such as `JSON Lines(quotes.jsonl)`.
- JSON data is held memory in an array and new data is appended to it, for e.g.

   ```
   [
       {"name": "Color TV", "price": "1200"},
       {"name": "DVD player", "price": "200"}
   ]
   ```
   
   As a result, it is advised to use JSON lines format if you want to save data in JSON.
   ```
   {"name": "Color TV", "price": "1200"}
   {"name": "DVD player", "price": "200"}
   ```

## Following Links
- This means telling your spider to go to the next page (or any other link) and continue scraping from there.
- Let’s say, instead of just scraping the stuff from the first two pages from https://quotes.toscrape.com, you want quotes from all the pages in the website.
- First thing to do is extract the link to the page we want to follow. 

```shell
# In bash terminal type: scrapy shell https://quotes.toscrape.com

>>> response.css("li.next a").get()
'<a href="/page/2/">Next <span aria-hidden="true">→</span></a>'

>>> response.css("li.next a::attr(href)").get()
'/page/2/'

```
Note: `::attr(attribute_name)` can be used to extract any attribute of an HTML tag using CSS selectors in Scrapy.

```python
import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = [
        "https://quotes.toscrape.com/page/1/",
    ]

    def parse(self, response):
        for quote in response.css("div.quote"):
            yield {
                "text": quote.css("span.text::text").get(),
                "author": quote.css("span small::text").get(),
                "tags": quote.css("div.tags a.tag::text").getall(),
            }

        next_page = response.css("li.next a::attr(href)").get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

```

You can also pass a selector to `response.follow` instead of a string; this selector should extract necessary attributes:
```shell
for href in response.css("ul.pager a::attr(href)"):
    yield response.follow(href, callback=self.parse)
```

For `<a>` elements there is a shortcut: `response.follow` uses their href attribute automatically. So the code can be shortened further:
```shell
for a in response.css("ul.pager a"):
    yield response.follow(a, callback=self.parse)
```

To create multiple requests from an iterable, you can use `response.follow_all` instead:
```shell
yield from response.follow_all(css="ul.pager a", callback=self.parse)
```


# Advance Scrapy

## Items in Scrapy (items.py)
- Scrapy Items are a predefined data structure that holds your data.
- Instead of yielding your scraped data in the form of a dictionary for example, you define an Item schema beforehand in your items.py file and use this schema when scraping data.
- This enables you to quickly and easily check what structured data you are collecting in your project.
- In Scrapy, `items.py` is where you define the data fields (structure) you want to extract from a website.

### How to use items.py
1. Define fields in `items.py`

```python
import scrapy

class QuotescraperItem(scrapy.Item):
    # define the fields for your item here like:
    author = scrapy.Field()
    text = scrapy.Field()
    tags = scrapy.Field()

```
2. Use the item in your spider

```python
import scrapy 

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

```

3. Run your spider and save output.
```shell
scrapy crawl -o output/csv_files/allNewQuotes.csv
```

## Scrapy Pipelines (pipelines.py)

- Item Pipelines are the data processors of Scrapy, which all our scraped Items will pass through and from where we can clean, process, validate, and store our data.
- Using Scrapy Pipelines we can:

   - Clean our data (ex. remove currency signs from prices)
   - Format our data (ex. convert strings to ints)
   - Enrich our data (ex. convert relative links to absolute links)
   - Valdiate our data (ex. make sure the price scraped is a viable price)
   - Store our data in databases, queues, files or object storage buckets

### How to use Pipelines in Scrapy

1. **Task**
   - convert author names in uppercase.
   - remove quotation marks from text.

2. **Steps**

   - Create a pipeline in `pipelines.py`
   ```python
      class QuotescraperPipeline:
      def process_item(self, item, spider):
          item["author"] = item["author"].upper()
          item['text'] = item['text'].replace('“', '').replace('”', '').replace('"', '').strip()
          return item
   ```  
   
   - spider file `quotes_advance.py`
   ```python
    # spider file: quotes_advance.py
    
    import scrapy
    from ..items import QuotescraperItem
    
    class NewQuotesSpider(scrapy.Spider):
        name = "advance_quotes"
        allowed_domains = ["quotes.toscrape.com"]
        start_urls = [
            "https://quotes.toscrape.com/tag/humor/",
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

   ``` 

   - Enable pipeline in `settings.py`. The number (300) is priority. Lower = runs earlier.
   ```python
    ITEM_PIPELINES = {
        'quotescraper.pipelines.QuotescraperPipeline': 300,
    }
   ```
   **Note: Each item scraped will now go through process_item() in your pipeline.**

   **Save output: `scrapy crawl advance_quotes -o output/jsonl_files/advance_quotes.jsonl`**
   
    **Final result:**
    ```
   {"author": "JANE AUSTEN", "text": "The person, be it gentleman or lady, who has not pleasure in a good novel, must be intolerably stupid.", "tags": ["aliteracy", "books", "classic", "humor"]} 
    ```
   
