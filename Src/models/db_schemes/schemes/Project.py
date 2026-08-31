from .multi_rag_base import SQLAlchemyBase
from sqlalchemy import Column,Integer,DateTime,func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
 
class Project(SQLAlchemyBase):
    #first thing in database is to define your tables
    __tablename__ = "Projects"
    Projcet_id = Column(Integer,primary_key=True,autoincrement=True)
    #adding unique value to project_id to add security 
    # this column doesnt accept null value must has avalue nullable=False
    Project_uuid = Column(UUID(as_uuid=True),default=uuid.uuid4,unique=True,nullable=False)

    created_at = Column(DateTime(timezone=True),server_default=func.now(),nullable=False)
    updated_at = Column(DateTime(timezone=True),onupdate=func.now(),nullable=True)

    Chunks = relationship(
            "Data_chunk",
            back_populates="Project"
        )

    Assets = relationship(
            "Assets",
            back_populates="Project"
        )
