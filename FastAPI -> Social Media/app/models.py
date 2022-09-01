
from enum import unique
from sqlalchemy.sql.expression import null, text
from .database import Base
from sqlalchemy import TIMESTAMP, Column, Integer, String, Boolean

class Post(Base):
    
    __tablename__ = "posts"
    
    
    id = Column(Integer,primary_key = True, nullable = False)
    title = Column(String, nullable = False)
    content = Column(String, nullable = False)
    published = Column(Boolean, server_default = "TRUE", nullable = False)
    create_at = Column(TIMESTAMP(timezone=True),nullable = False, server_default=text("now()"))
    
    
class User(Base):
    __tablename__ = "users"
        
        
    #name = Column
    email = Column(String, nullable = False, unique = True)
    password = Column(String, nullable = False)
    id = Column(Integer,primary_key = True, nullable = False)
    create_at = Column(TIMESTAMP(timezone=True),nullable = False, server_default=text("now()"))