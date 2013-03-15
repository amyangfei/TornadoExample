from sqlalchemy.types import *
from sqlalchemy.schema import Column
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class CrawlArticle(Base):
    __tablename__ = 'cr_douban_book_review'
    bid = Column('b_id', Integer, primary_key = True)
    btitle = Column('b_title', String(45))
    bauthor = Column('b_author', String(45))
    bcontent = Column('b_content', TEXT(4294967295))
    bsource = Column('b_source', TEXT(4294967295))
    bisproduct = Column('b_isproduct', Boolean)

class CrawlUrlRecord(Base):
    __tablename__ = 'cr_douban_book_url'
    uid = Column('u_id', Integer, primary_key = True)
    uurl = Column('u_url', String(45))
    ucrawled = Column('u_crawled', Boolean)
    utype = Column('u_type', Integer)
    
    