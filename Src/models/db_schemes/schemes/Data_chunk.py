from .multi_rag_base import SQLAlchemyBase
from sqlalchemy import Column,Integer,DateTime,func,String,ForeignKey
from sqlalchemy.dialects.postgresql import UUID,JSONB
from sqlalchemy.orm import relationship
from sqlalchemy import Index
import uuid

class Data_chunk(SQLAlchemyBase):
    #first thing in database is to define your tables
    __tablename__ = "Chunks"
    
    # id is aprimary key 
    Chunk_id = Column(Integer,primary_key=True,autoincrement=True)
    Chunk_uuid = Column(UUID(as_uuid=True),default=uuid.uuid4,unique=True,nullable=False)
    Chunk_text = Column(String,nullable=False)
    Chunk_metadata = Column(JSONB,nullable=True) # dict store metadata of file in mongob but in postgress(json)

    #we have two forignkey(name of table.name of column)
    Chunk_project_id = Column(Integer,ForeignKey("Projects.Projcet_id"),nullable=False)
    Chunk_assets_id = Column(Integer,ForeignKey("Assets.Asset_id"),nullable=False)


    #we need to make relation between ForeignKey key and primary key to back_populates data from primary to ForeignKey
    Project = relationship("Projects",back_populates="Chunks")
    Assets  =relationship("Assets",back_populates="Chunks")

    created_at = Column(DateTime(timezone=True),server_default=func.now(),nullable=False)
    updated_at = Column(DateTime(timezone=True),onupdate=func.now(),nullable=True)

    # if we have ForeignKey then ===>  must create index to make retrive eaiser
    # we want to create index for asset_project_id to get project_id from assets without using loop
    # creatning index for columns that doesnt have unique value beacause postgress create default index for (primary or unique)
    __table_args__ = (
        Index("ix_Chunk_project_id",Chunk_project_id),
        Index("ix_Chunk_assets_id",Chunk_assets_id),
    )

    
