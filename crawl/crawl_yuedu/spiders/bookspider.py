from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request
from crawl.crawl_yuedu.items import BookReview
import re

class BookSpider(BaseSpider):
    name = "bookspider"
    allowed_domains = ["book.douban.com"]
    
    #start_urls = ['http://book.douban.com/tag/']
    start_urls = ["http://book.douban.com/subject/1770782/reviews?score=&start=25", ]
    
    tags_pattern = re.compile('http://book.douban.com/tag/$')
    tag_list_pattern = re.compile('http://book.douban.com/tag/[\s\S]+')
    subject_pattern = re.compile('http://book.douban.com/subject/[0-9]+/$')
    review_list_pattern = re.compile('http://book.douban.com/subject/[0-9]+/reviews')
    review_pattern = re.compile('http://book.douban.com/review/[0-9]+/$')
    
    patterns = [tags_pattern, tag_list_pattern, subject_pattern, review_list_pattern, review_pattern]
    types = ['tags_pattern', 'tag_list', 'subject_pattern', 'review_list', 'review']
    
    review_list_index_pattern = re.compile('http://book.douban.com/subject/[0-9]+/reviews$')
    review_list_add_pattern = re.compile('(http://book.douban.com/subject/[0-9]+/reviews\?[a-zA-Z&=]*?start=)([0-9]+)$')
    
    extend_new_urls = []
    
    def parse(self, response):
      
        for i in xrange(len(self.patterns)):
            if self.patterns[i].match(response.url) != None:
                page_type = self.types[i]
                break
                  
#        page_type = response.url.split("/")[3]
#        page_sub_type = response.url.split("/")[4]
#        if page_type == 'tag' and page_sub_type == '':
#            page_type = 'tags'
        self._handle_page(response, page_type)
        
        #yield self.make_requests_from_url('http://book.douban.com/review/2923366/')
        for url in self.extend_new_urls:
            yield self.make_requests_from_url(url)
            self.extend_new_urls.remove(url)
    
    def _parse_tags_page(self, response):
        pass
    
    def _parse_tag_list_page(self, response):
        print ''
        pass
    
    def _parse_subject_page(self, response):
        pass
    
    def _parse_review_list_page(self, response):
        page_step = 25
        extendurls = []
        
        ret = self.review_list_index_pattern.match(response.url)
        if ret != None:
            extendurls.append(ret.group(0)+'?score=&start='+str(page_step))
        else:
            ret = self.review_list_add_pattern.match(response.url)
            if ret != None:
                page_index = int(ret.group(2)) + page_step
                extendurls.append(ret.group(1) + str(page_index))
        
        hxs = HtmlXPathSelector(response)
        link_divs =hxs.select('//div[@class="nlst"]')
        for link_div in link_divs:
            new_url = link_div.select('h3/a/@href')[0].extract()
            extendurls.append(new_url)
        
        self._extend_urls(extendurls)
    
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
#        parse_page = {'tags' : self._parse_tags_page(response),
#                      'tag_list' : self._parse_tag_list_page(response),
#                      'subject' : self._parse_subject_page(response),
#                      'review_list' : self._parse_review_list_page(response),
#                      'review' : self._parse_review_page(response),
#                      }
#        return parse_page[page_type](response)

        if page_type == 'tags':
            self._parse_tags_page(response)
        elif page_type == 'tag_list':
            self._parse_tag_list_page(response)
        elif page_type == 'subject':
            self._parse_subject_page(response)
        elif page_type == 'review_list':
            self._parse_review_list_page(response)
        elif page_type == 'review':
            self._parse_review_page(response)

    def _extend_urls(self, urls):
        print 'extends...'
        self.extend_new_urls[:] = []
        self.extend_new_urls.extend(urls)
#        for url in urls:
#            #self.start_urls.append(url)
#            yield self.make_requests_from_url(url)#.replace(callback=self.parse)
#            #request = Request(url, callback=self.parse, meta={'depth', 3})
#            #yield request
            
            