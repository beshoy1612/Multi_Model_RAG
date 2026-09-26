from abc import ABC,abstractmethod
from typing import List
class Vectordb_Interface(ABC):

    # in any connection in database we must create 2 important function ===> (connect & disconnect)
    #   we deal with it like no_sql database collection not tables  
    # it store data in vetcor
    @abstractmethod
    def connect(self):
        pass
    
    @abstractmethod
    def disconnect(self):
        pass

    @abstractmethod
    def is_collection_existed(self,collection_name:str)->bool:
        pass
    
    @abstractmethod
    def list_collection(self)->List:
        pass

    @abstractmethod
    def get_collection_info(self,collection_name:str)->dict:
        pass

    @abstractmethod
    def delet_collection(self,collection_name:str):
        pass

    # we store data in vector so we will need to know embadding_size that we will store from .env
    @abstractmethod
    def create_collection(self,collection_name: str,embadding_size: int,do_reset: bool = False):
        pass

    # we need data about data thats we call ==> metadata , record id to mark each vector must be unique ,
    # text we will store
    @abstractmethod
    def insert_one (self,collection_name: str,text:str,
                    vector: list, metadata :dict = None, record_id: str = None):
        pass

    @abstractmethod
    def insert_many (self,collection_name: str,texts: list,
                    vector: list, metadata :list = None,
                    record_id: list = None, batch_size: int = 50 ):
        pass

    # we have multibe ways of search but we will create seacrh by vector first , then  search by text or hybird search 
    # limit much of return 
    # vector what we will search 
    # we have multible collection so we want to know whats collection name we wiil search in  
    @abstractmethod
    def search_by_vector(self,collection_name: str,vector: list,limit: int):
        pass

    ## adding here new search  !!!!!!!!!!!!!!=====================