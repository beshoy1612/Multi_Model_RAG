from .multi_rag_base import SQLalchemy_base
from sqlalchemy import Column,Integer,DateTime
class Project(SQLalchemy_base):
    #first thing in database is to define your tables
    __tablename__ = "Projects"
    Projcet_id = Column(Integer,primary_key=True,autoincrement=True)
        