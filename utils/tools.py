from crawl.crawl_yuedu.crawl_models import CrawlArticle
from model.models import Article

def CrawlArt2ProductArt(crawl_article, ran_url):
    pt_article = Article()
    pt_article.aurl = ran_url
    pt_article.atitle = crawl_article.btitle
    pt_article.aauthor = crawl_article.bauthor
    pt_article.acontent = crawl_article.bcontent
    pt_article.asource = crawl_article.bsource
    return pt_article
    