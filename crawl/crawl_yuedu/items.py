# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field

class CrawlYueduItem(Item):
    # define the fields for your item here like:
    # name = Field()
    pass

class BookReview(Item):
    title = Field()
    author = Field()
    content = Field()
    source = Field()
    
    def __str__(self):
        return self.title + '\n' + self.author + '\n' + self.content + '\n' + self.source