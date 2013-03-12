from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from config import mysql_config

#engine = create_engine(ConnectString, encoding='utf8', convert_unicode=True)
#metadata = MetaData()
#metadata.create_all(engine)        

Base = declarative_base()


#User_Table = Table('y_users', metadata, 
#                   Column('u_id', Integer, primary_key = True), 
#                   Column('u_name', String(45)), 
#                   mysql_charset = 'utf8')

#metadata.create_all(engine)

class User(Base):
    __tablename__ = 'y_users'
    uid = Column('u_id', Integer, primary_key = True)
    uemail = Column('u_email', String(45))
    uname = Column('u_name', String(45))
    upwd = Column('u_password', String(45))

class Article(Base):
    __tablename__ = 'y_articles'
    aid = Column('a_id', Integer, primary_key = True)
    aurl = Column('a_url', String(45))
    atitle = Column('a_title', String(45))
    aauthor = Column('a_author', String(45))
    acontent = Column('a_content', TEXT(4294967295))
    asource = Column('a_source', TEXT(4294967295))
    