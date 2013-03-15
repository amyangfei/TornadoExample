from utils.db import ConnectDB
from utils.random_url import GetRandomUrl
from crawl.crawl_yuedu.crawl_models import CrawlArticle, CrawlUrlRecord
from model.models import Article

def move_main():
    dbsession = ConnectDB()
    articles = dbsession.query(CrawlArticle).filter(CrawlArticle.bisproduct==False).all()
    for c_article in articles:
        ran_url = GetRandomUrl(dbsession)
        #pt_article = CrawlArt2ProductArt(c_article, ran_url)
        #dbsession.add(pt_article)
        dbsession.execute(
            Article.__table__.insert(),
            [{'a_url':ran_url, 'a_title':c_article.btitle, 'a_author':c_article.bauthor,
              'a_content':c_article.bcontent, 'a_source':c_article.bsource
              }]
        )
        dbsession.query(CrawlArticle).filter(CrawlArticle.bid == c_article.bid).update({
            CrawlArticle.bisproduct : True
        })
    dbsession.commit()

if __name__ == '__main__':
    move_main()