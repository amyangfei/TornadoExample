from base import BaseHandler
from model.models import *
from random import choice
from  sqlalchemy.sql.expression import func
from tornado import escape

# return a random article id    
class ArticleRandomHandler(BaseHandler):
    def get(self):
        user = self.get_current_user()
        randUrl = self.session.query(Article).order_by(func.rand()).limit(1).first()
        #randUrl = self.session.query(User).filter_by(uemail = 'admin@gmail.com').first()
        self.write(escape.json_encode({'short_url':randUrl.aurl}))
        
# get article by id
class ArticleRenderHandler(BaseHandler):
    def get(self, short_url=None):
        user = self.get_current_user()
        _article = self.session.query(Article).filter_by(aurl=short_url).first()
        self.render('article.html', username=user, article=_article)



URL_ENCODE = 'abcdefghijklmnopqrstuvwxyz0123456789'

def url_random(dbsession):
    while True:
        url = ''.join(choice(URL_ENCODE) for i in xrange(choice((6,7,8,9,10))))
        urlCount = dbsession.query(Article).filter_by(aurl = url).count()
        if urlCount <= 0:
            break
    return url

def get_random_url(dbsession):
    pass
