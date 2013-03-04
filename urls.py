from handlers.index import *
from handlers.article import *

urls = [
    (r'/test', TestHandler),
    (r'/', IndexHandler),
    (r'/login', LoginHandler),
    (r'/logout', LogoutHandler),
    (r'/register', RegisterHandler),
    (r'/article/random', ArticleRandomHandler),
    (r'/article/([\w]+)', ArticleRenderHandler),
]
