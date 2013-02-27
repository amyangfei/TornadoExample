from handlers.index import *

urls = [
    (r'/', IndexHandler),
    (r'/login', LoginHandler),
    (r'/register', RegisterHandler),
]
