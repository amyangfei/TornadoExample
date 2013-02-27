import tornado.web

import hashlib

class BaseHandler(tornado.web.RequestHandler):
    @property
    def db(self):
        return self.application.db
    @property
    def session(self):
        return self.application.session
    
    def pwdEncrypt(self, email, pwd):
        return hashlib.sha1(str(email) + str(pwd) + "yuedu").hexdigest()
    
    def get_current_user(self):
        user_json = self.get_secure_cookie("user")
        if user_json:
            return tornado.escape.json_decode(user_json)
        else:
            return None
    
    def set_current_user(self, user_email):
        print "setting " + user_email
        if user_email:
            self.set_secure_cookie("user", tornado.escape.json_encode(user_email))
        else:
            self.clear_cookie("user")
