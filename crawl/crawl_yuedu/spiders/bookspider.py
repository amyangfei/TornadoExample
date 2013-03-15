from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from crawl.crawl_yuedu.items import BookReview
import re, sys
from Queue import PriorityQueue
from utils.db import ConnectDB
from crawl.crawl_yuedu.crawl_models import CrawlArticle, CrawlUrlRecord

class BookSpider(BaseSpider):
    name = 'bookspider'
    allowed_domains = ["book.douban.com"]
    
    #start_urls = ["http://book.douban.com/subject/1770782/reviews?score=&start=25", ]
    #start_urls = ['http://book.douban.com/subject/1770782/', ]
    #start_urls = ['http://book.douban.com/tag/']
    start_urls = ['http://book.douban.com/tag/%E6%96%87%E5%AD%A6']
    
    tags_pattern = re.compile('http://book.douban.com/tag/$')
    tag_list_pattern = re.compile('http://book.douban.com/tag/[\s\S]+')
    subject_pattern = re.compile('http://book.douban.com/subject/[0-9]+/$')
    review_list_pattern = re.compile('http://book.douban.com/subject/[0-9]+/reviews')
    review_pattern = re.compile('http://book.douban.com/review/[0-9]+/$')
    
    patterns = [tags_pattern, tag_list_pattern, subject_pattern, review_list_pattern, review_pattern]
    types = ['tags', 'tag_list', 'subject', 'review_list', 'review']
    
    review_list_index_pattern = re.compile('http://book.douban.com/subject/[0-9]+/reviews$')
    review_list_add_pattern = re.compile('(http://book.douban.com/subject/[0-9]+/reviews\?[a-zA-Z&=]*?start=)([0-9]+)$')
    
    tag_list_index_pattern = re.compile('http://book.douban.com/tag/[\s\S]+$')
    tag_list_add_pattern = re.compile('(http://book.douban.com/tag/[\s\S]+\?start=)([0-9]+?)[a-zA-Z&=]*$')
    
    tags_url_base = 'http://book.douban.com/tag/'
    
    priority_dict = {'tags' : 128,
                     'tag_list' : 64,
                     'subject' : 32,
                     'review_list' : 16,
                     'review' : 8
                     }
    
    crawl_url_type = {'book' : 1,
                      'review' : 2,
                      }
    
    def __init__(self, **kwargs):
        self.session = ConnectDB()
        self.extend_url_queue = PriorityQueue()
        self.crawled_url_set = set()
        self._get_crawled_urls()
        BaseSpider.__init__(self, name=None, **kwargs)
    
    def parse(self, response):
      
        for i in xrange(len(self.patterns)):
            if self.patterns[i].match(response.url) != None:
                page_type = self.types[i]
                break
                        
        self._handle_page(response, page_type)
        
        if not self.extend_url_queue.empty():
            p_url = self.extend_url_queue.get()
            yield self.make_requests_from_url(p_url[1])
    
    def _parse_tags_page(self, response):
        hxs = HtmlXPathSelector(response)
        hrefs = hxs.select('//table[@class="tagCol"]/tbody/tr/td/a/@href').extract()
        hreflist = []
        for tag_href in hrefs:
            tag = re.match('\./([\s\S]+)$', tag_href).group(1)
            p_url = PriorityUrl(self.tags_url_base + tag, self.priority_dict['tag_list'])
            hreflist.append(p_url)
        self._extend_urls(hreflist)
        
    def _parse_tag_list_page(self, response):
        page_step = 20
        extendurls = []

        ret = self.tag_list_index_pattern.match(response.url)
        if ret != None:
            p_url = PriorityUrl(ret.group(0) + '?start=' + str(page_step), self.priority_dict['tag_list'])
            extendurls.append(p_url)
        else:
            ret = self.tag_list_add_pattern.match(response.url)
            if ret != None:
                page_index = int(ret.group(2)) + page_step
                if page_index < 2 * page_step:
                    p_url = PriorityUrl(ret.group(1) + str(page_index), self.priority_dict['tag_list'])
                    extendurls.append(p_url)
        
        hxs = HtmlXPathSelector(response)
        info_div = hxs.select('//div[@class="info"]')
        for info in info_div:
            new_url = info.select('h2/a/@href')[0].extract()
            p_url = PriorityUrl(new_url, self.priority_dict['subject'])
            extendurls.append(p_url)
            
        self._extend_urls(extendurls)
    
    def _parse_subject_page(self, response):
        hxs = HtmlXPathSelector(response)
        reviews_href = hxs.select('//div[@id="reviews"]/h2/span/a/@href').extract()
        if len(reviews_href) <= 0:
            return
        p_url = PriorityUrl(reviews_href[0], self.priority_dict['review_list'])
        self._extend_urls([p_url])
    
    def _parse_review_list_page(self, response):
        page_step = 25
        extendurls = []
        
        ret = self.review_list_index_pattern.match(response.url)
        if ret != None:
            p_url = PriorityUrl(ret.group(0)+'?score=&start='+str(page_step), self.priority_dict['review_list'])
            extendurls.append(p_url)
        else:
            ret = self.review_list_add_pattern.match(response.url)
            if ret != None:
                page_index = int(ret.group(2)) + page_step
                if page_index < 2 * page_step:
                    p_url = PriorityUrl(ret.group(1) + str(page_index), self.priority_dict['review_list'])
                    extendurls.append(p_url)
        
        hxs = HtmlXPathSelector(response)
        link_divs = hxs.select('//div[@class="nlst"]')
        for link_div in link_divs:
            new_url = link_div.select('h3/a/@href')[0].extract()
            p_url = PriorityUrl(new_url, self.priority_dict['review'])
            extendurls.append(p_url)
        
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
            if len(cont.strip()) == 0:
                continue
            else:
                review_article += cont.replace('\r', '</p><p>')
        review_article += '</p>'
        
        item = BookReview()
        item['title'] = review_title
        item['author'] = review_author
        item['content'] = review_article
        item['source'] = response.url
        
        article_dict = {'title' : (review_title!=None and [review_title] or [''])[0],
                        'author' : (review_author!=None and [review_author] or ['unknown author'])[0],
                        'content': (review_article!=None and [review_article] or [''])[0],
                        'source' : (response.url!=None and [response.url] or ['unknown source'])[0],
                        }
        
        self._save_douban_review(article_dict)
        
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

    def _extend_urls(self, p_urls):
        #print 'extends...'
        for p_url in p_urls:
            if p_url.url not in self.crawled_url_set:
                self.extend_url_queue.put((p_url.priority, p_url.url))
#        for url in urls:
#            yield self.make_requests_from_url(url)#.replace(callback=self.parse)
#            #request = Request(url, callback=self.parse, meta={'depth', 3})

    def _save_douban_review(self, article_dic):
        craw_article = CrawlArticle()
        craw_article.btitle = article_dic['title']
        craw_article.bauthor = article_dic['author']
        craw_article.bcontent = article_dic['content']
        craw_article.bsource = article_dic['source']
        craw_article.bisproduct = False
        
        self.session.add(craw_article)  
        self._set_url_as_crawled(article_dic['source'], self.crawl_url_type['review'])
        self.session.commit()
        
    def _get_crawled_urls(self):
        crawled_urls = self.session.query(CrawlUrlRecord.uurl).filter(CrawlUrlRecord.ucrawled==True).all()
        for crawled_url in crawled_urls:
            self.crawled_url_set.add(crawled_url[0])
    
    def _set_url_as_crawled(self, url, url_type):
        cur = CrawlUrlRecord()
        cur.uurl = url
        cur.ucrawled = True
        cur.utype = url_type
        self.session.add(cur)
        self.crawled_url_set.add(url)

class PriorityUrl:
    def __init__(self, url, priority=sys.maxint):
        self.url = url
        self.priority = priority
        
            