from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from crawl.crawl_yuedu.items import BookReview

class BookSpider(BaseSpider):
    name = "bookspider"
    allowed_domains = ["book.douban.com"]
    
    start_urls = ['http://book.douban.com/tag/']
    
    def parse(self, response):
        page_type = response.url.split("/")[3]
        self._handle_page(response, page_type)
    
    def _parse_tag_page(self, response):
        print ''
        pass
    
    def _parse_subject_page(self, response):
        pass
    
    def _parse_review_page(self, response):
        hxs = HtmlXPathSelector(response)
        review_content = hxs.select('//div[@id="content"]')
        review_title = review_content[0].select('h1').select('text()')[0].extract()
        
        review_info = hxs.select('//span[@class="pl2"]')
        review_author = review_info[0].select('a/span').select('text()')[0].extract()
        review_author += review_info[0].select('text()')[1].extract().strip()
        
        review_article_original = hxs.select('//div[@id="link-report"]/span')[0].select('text()')
        review_article = '<p>'
        for ar_con in review_article_original:
            cont = ar_con.extract()
            if len(cont) <= 3 and cont[-1] == '\r':
                review_article += '</p><p>'
            else:
                review_article += cont
        review_article += '</p>'
        
        item = BookReview()
        item['title'] = review_title
        item['author'] = review_author
        item['content'] = review_article
        item['source'] = response.url
        
        #print str(item)
        
    def _handle_page(self, response, page_type):
        parse_page = {'tag' : self._parse_tag_page(self, response),
                      'subject' : self._parse_subject_page(self, response),
                      'review' : self._parse_review_page(self, response)
                      }
        return parse_page[page_type](self, response)

    