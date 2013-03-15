from random import choice
from model.models import Article

URL_ENCODE = 'abcdefghijklmnopqrstuvwxyz0123456789'

def GetRandomUrl(dbsession):
    while True:
        url = ''.join(choice(URL_ENCODE) for i in xrange(choice((7,8,9,10))))
        urlCount = dbsession.query(Article).filter_by(aurl = url).count()
        if urlCount <= 0:
            break
    return url