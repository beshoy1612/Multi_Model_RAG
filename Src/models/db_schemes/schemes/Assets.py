from .multi_rag_base import SQLalchemy_base
from sqlalchemy import Column,Integer,DateTime,func,String,JSONB,ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy import Index
import uuid

class Assets(SQLalchemy_base):
    #first thing in database is to define your tables
    __tablename__ = "Assets"
    
    # id is aprimary key 
    Asset_id = Column(Integer,primary_key=True,autoincrement=True)

    #adding unique value to project_id to add security 
    # this column doesnt accept null value must has avalue nullable=False
    Asset_uuid = Column(UUID(as_uuid=True),default=uuid.uuid4,unique=True,nullable=False)
    Asset_name = Column(String,nullable=False)
    Asset_type = Column(String,nullable=False)
    Asset_size = Column(Integer,nullable=False)
    #can store json file in postgres unlike mongodb(not supported json) we used dict  
    #we used jsonb not json because it has low latency when read 
    Asset_config = Column(JSONB,nullable=True) # dict store metadata of file in mongob but in postgress(json)

    #forignkey(name of table.name of column)
    Asset_project_id = Column(Integer,ForeignKey("Projects.Projcet_id"),nullable=False)

    #we need to make relation between ForeignKey key and primary key to back_populates data from primary to Foreign
    Project = relationship("Projects",back_populates="Assets")

    # if we have ForeignKey then ===>  must create index to make retrive eaiser
    # we want to create index for asset_project_id to get project_id from assets without using loop
    # creatning index for columns that doesnt have unique value beacause postgress create default index for (primary or unique)
    __table_args__ = (
        Index("ix_asset_project_id",Asset_project_id),
        Index("ix_asset_type",Asset_type),
    )
    created_at = Column(DateTime(timezone=True),server_default=func.now(),nullable=False)
    updated_at = Column(DateTime(timezone=True),onupdate=func.now(),nullable=True)

    
