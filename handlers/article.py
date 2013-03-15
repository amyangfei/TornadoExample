from handlers.base import BaseHandler
from model.models import *
from random import choice
from  sqlalchemy.sql.expression import func
from tornado import escape

# return a random article id    
class ArticleRandomHandler(BaseHandler):
    def get(self):
        user = self.get_current_user()
        randUrl = self.session.query(Article).order_by(func.rand()).limit(1).first()
        self.write(escape.json_encode({'short_url':randUrl.aurl}))
        
# get article by id
class ArticleRenderHandler(BaseHandler):
    def get(self, short_url=None):
        user = self.get_current_user()
        _article = self.session.query(Article).filter_by(aurl=short_url).first()
        self.render('article.html', username=user, article=_article)

def get_random_url(dbsession):
    pass
