from .Base_model import Base_model
from dp_schemes import Project
from .enum.DataBaseEnum import DataBaseEnum


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
    