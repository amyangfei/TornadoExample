from handlers.index import *

urls = [
    (r'/test', TestHandler),
    (r'/', IndexHandler),
    (r'/login', LoginHandler),
    (r'/logout', LogoutHandler),
    (r'/register', RegisterHandler),
]
