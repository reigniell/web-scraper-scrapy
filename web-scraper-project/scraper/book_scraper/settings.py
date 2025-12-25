BOT_NAME = 'book_scraper'
SPIDER_MODULES = ['book_scraper.spiders']
NEWSPIDER_MODULE = 'book_scraper.spiders'
ROBOTSTXT_OBEY = True
DOWNLOAD_DELAY = 1
# Comment out MongoDB pipeline if you don't have MongoDB
# ITEM_PIPELINES = {
#     'book_scraper.pipelines.MongoDBPipeline': 300,
# }
# MONGO_URI = 'mongodb://localhost:27017/'
# MONGO_DATABASE = 'books_db'
LOG_LEVEL = 'INFO'
FEEDS = {
    '../data/books.json': {
        'format': 'json',
        'encoding': 'utf8',
        'indent': 4,
    }
}
