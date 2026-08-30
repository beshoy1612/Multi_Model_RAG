from .Base_model import Base_model
from db_schemes import Data_chunk
from sqlalchemy.future import select
from sqlalchemy import func
class Chunk_model(Base_model):
    def __init__(self, db_client :object):
        super().__init__(db_client = db_client)
        self.db_client = db_client

    # we must call init__connection with constructor to make index just the project_model called
    # and we cant  call init_collection in __init__ because its async and __init__ cannot to be async
    # because constructor shouldnt be async and we cant use await in __init__  
    #so we create function that call __init__ and init_collection function will be static 
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


# ======================================================stop here=========================
    async def insert_many_chunks(self, chunks:list, batch_size:int=100):
        for i in range(0,len(chunks),batch_size):
            batch = chunks[i:i+batch_size]
            operation = [
                InsertOne(chunk.dict(by_alias=True,exclude_unset=True))
                for chunk in batch
            ]
            await self.connection.bulk_write(operation)

        return len(chunks)       

    async def get_project_chunk(self,project_id:ObjectId,page_no: int = 1,page_size: int = 100):
        result = await self.connection.find({
            "chunk_project_id": project_id
        }).skip((page_no - 1)*page_size).limit(page_size).to_list(length = None)

        return[
            Data_chunk(**rec)
            for rec in result
        ]