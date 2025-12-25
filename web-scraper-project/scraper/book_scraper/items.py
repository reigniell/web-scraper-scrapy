import scrapy

class BookItem(scrapy.Item):
    title = scrapy.Field()
    price = scrapy.Field()
    rating = scrapy.Field()
    availability = scrapy.Field()
    description = scrapy.Field()
    category = scrapy.Field()
    image_url = scrapy.Field()
    product_url = scrapy.Field()
    scraped_date = scrapy.Field()
