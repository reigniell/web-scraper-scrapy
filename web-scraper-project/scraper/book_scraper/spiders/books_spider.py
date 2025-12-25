import scrapy
from scrapy.http import Request
from urllib.parse import urljoin
from book_scraper.items import BookItem
from datetime import datetime

class BooksSpider(scrapy.Spider):
    name = 'books'
    allowed_domains = ['books.toscrape.com']
    start_urls = ['http://books.toscrape.com/']
    
    def parse(self, response):
        # Get all book links
        book_links = response.css('h3 a::attr(href)').getall()
        
        for book_link in book_links:
            absolute_url = urljoin(response.url, book_link)
            yield Request(absolute_url, callback=self.parse_book)
        
        # Pagination
        next_page = response.css('li.next a::attr(href)').get()
        if next_page:
            next_url = urljoin(response.url, next_page)
            yield Request(next_url, callback=self.parse)
    
    def parse_book(self, response):
        item = BookItem()
        
        # Extract data
        item['title'] = response.css('h1::text').get()
        item['price'] = response.css('p.price_color::text').get()
        
        # Rating
        rating = response.css('p.star-rating::attr(class)').get()
        item['rating'] = rating.split()[-1] if rating else None
        
        # Availability
        availability = response.css('p.instock.availability::text').getall()
        item['availability'] = ' '.join([text.strip() for text in availability]).strip()
        
        # Description
        desc = response.xpath('//div[@id="product_description"]/following-sibling::p/text()').get()
        item['description'] = desc.strip() if desc else None
        
        # Category
        item['category'] = response.css('ul.breadcrumb li:nth-last-child(2) a::text').get()
        
        # Image URL
        img = response.css('div.item.active img::attr(src)').get()
        item['image_url'] = urljoin(response.url, img) if img else None
        
        # URLs and timestamp
        item['product_url'] = response.url
        item['scraped_date'] = datetime.now().isoformat()
        
        yield item

