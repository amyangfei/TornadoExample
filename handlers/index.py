from model.models import User
from base import BaseHandler

class IndexHandler(BaseHandler):
    def get(self):
        user = self.get_current_user()
        #entityGet = Entity.get('test tornado web project')
        self.render('index.html', username = user, test='xiu')

class LoginHandler(BaseHandler):
    def get(self):
        self.render('login.html', next=self.get_argument("next", "/"))
        
    def post(self):
        email = self.get_argument("email")
        password = self.get_argument("password")
        
        user = self.session.query(User).filter_by(uemail = email).first()
        if user and user.upwd == self.pwdEncrypt(email, password):
            self.set_current_user(user.uname)
            self.redirect("/")
        else:
            self.redirect("/login")
            
class RegisterHandler(BaseHandler):
    def get(self):
        self.render("register.html", next=self.get_argument("next", "/"))
    
    def post(self):
        email = self.get_argument("email", "")
        already_taken = self.session.query(User).filter_by(uemail = email).count()
        if already_taken != 0:
            error_msg = 'email already exists'
            self.render('register.html', error = error_msg)
            return
        
        username = self.get_argument("username", "")
        password = self.get_argument("password", "")
        encryptPwd = self.pwdEncrypt(email, password)
        
        user = User()
        user.uemail = email
        user.uname = username
        user.upwd = encryptPwd
        self.session.add(user)
        self.session.commit()
        self.set_current_user(username)
        
        self.redirect("/")
        