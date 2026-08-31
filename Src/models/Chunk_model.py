from .Base_model import Base_model
from .db_schemes import Data_chunk
from sqlalchemy.future import select
from sqlalchemy import func,delete
from bson.objectid import ObjectId
class Chunk_model(Base_model):
    def __init__(self, db_client :object):
        super().__init__(db_client = db_client)
        self.db_client = db_client


    @classmethod
    async def create_instance(cls, db_client: object):
        instance = cls(db_client) # call __init__
        return instance

    async def create_chunk(self, chunk:Data_chunk):
        async with self.db_client() as session:
            async with session.begin():
                session.add(chunk)
            await session.commit()
            await session.refresh(chunk)

        return chunk
 
    async def  get_chunk(self, chunk_id:str):
        async with self.db_client() as session:
            async with session.begin():
                result = await session.execute(select(Data_chunk).where(Data_chunk.Chunk_id == chunk_id))
                chunk  = result.scalar_one_or_none()
            return chunk


    async def insert_many_chunks(self, chunks:list, batch_size:int=100):
        async with self.db_client() as session:
            async with session.begin():    
                for i in range(0,len(chunks),batch_size):
                    batch = chunks[i:i+batch_size]
                    session.add_all(batch)
            await session.commit()
        return len(chunks)      

    async def delete_chunk_by_project_id(self,project_id:ObjectId):
        async with self.db_client() as session:
            stmt = delete(Data_chunk).where(Data_chunk.Chunk_project_id == project_id)
            result = await session.execute(stmt)
            await session.commit()
        return result.rowcount       


    async def get_project_chunk(self,project_id:ObjectId,page_no: int = 1,page_size: int = 100):
        async with self.db_client() as session: 
            stmt = select(Data_chunk).where(Data_chunk.Chunk_project_id ==project_id).offset((page_no - 1)*page_size).limit(page_size)
            result = await session.execute(stmt)
            recodrd = result.scalar().all()
        return recodrd