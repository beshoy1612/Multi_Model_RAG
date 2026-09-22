from ..Vectordb_Interface import Vectordb_Interface
from ..Vectordb_Enum import DistanceMethod
from qdrant_client import models , QdrantClient
from typing import List
import logging

# we have differnet method to get data (cosine similarty , dot_product )
class Qdrantdb(Vectordb_Interface):
    def __init__(self,db_path: str,distance_method: str):
        self.db_path = db_path
        self.distance_method = None
        self.client = None

        if distance_method == DistanceMethod.COSINE.value:
            self.distance_method = models.Distance.COSINE

        elif distance_method == DistanceMethod.DOT.value:
            self.distance_method ==  models.Distance.DOT

        self.logger = logging.getLogger(__name__)


    def connect(self):
        self.client = QdrantClient(path=self.db_path)

    def disconnect(self):
        # Qdrant desnt has disconnect funcition so we will intiate None
        self.client = None

    def is_collection_existed(self, collection_name):
        # QdrantClient has .collection_exist ready func 
        return self.client.collection_exists(collection_name=collection_name)

    def list_collection(self)->List:
        # QdrantClient has .get_collection ready func 
        return self.client.get_collection()

    def get_collection_info(self, collection_name):
        return self.client.get_collection(collection_name=collection_name)


    def delet_collection(self, collection_name):
        if self.is_collection_existed(collection_name=collection_name):
            # QdrantClient has .delete_collection ready func 
            return self.client.delete_collection(collection_name=collection_name)

    def create_collection(self, collection_name, embadding_size, do_reset = False):
        if do_reset:
            self.delet_collection(collection_name=collection_name)

        if not self.is_collection_existed(collection_name=collection_name):
            # QdrantClient has .create_collection ready func 
            _ = self.client.create_collection(collection_name=collection_name,
                                          vectors_config=models.VectorParams(                                  size = embadding_size,
                                            distance = self.distance_method,
                                            size  = embadding_size
                                                )
                                        )
            return True
        
        return False


    def insert_one(self, collection_name, text, vector, metadata = None, record_id = None):
        if not self.is_collection_existed(collection_name=collection_name):
            self.logger.error("no colllection found")
            return False
        
        # QdrantClient has .upload_records ready func 
        _ = self.client.upload_records(
            collection_name=collection_name,
            records=[
               models.Record(
                   vector=vector,
                   # data of vector
                   payload={
                       "text":text,
                       "metadata":metadata
                   }
               ) 
            ]
        )
        return True

    def insert_many(self, collection_name, texts, vector, metadata = None, record_id = None, batch_size = 50):
         if metadata is None:
             metadata =[None] + len(texts)

         if record_id is None:
             record_id =[None] + len(texts)
               
         if not self.is_collection_existed(collection_name=collection_name):
        
            self.logger.error("no colllection found")

            return False

         for i in range(0,len(texts),batch_size):
            batch_end = i + batch_size
            batch_text = texts[i:batch_end]
            batch_vector = vector[i:batch_end]
            batch_metadata = metadata[i:batch_end]
            batch_record_id = record_id[i:batch_end]
            batch_record = [
                models.Record(
                    id = batch_record_id[x],
                    vector = batch_vector[x],
                    payload={
                        "metadata": batch_metadata[x],
                        "text": batch_text[x]
                    }
                )
                for x in range(len(batch_text))
            ]
            try:
                _ = self.client.upload_records(
                            collection_name=collection_name,
                            records=batch_record
                            )
            except Exception as e:
                self.logger.error(f"error while insert batch {e}")
                return False
            
         return True


    def search_by_vector(self,collection_name: str,vector:list, limit: int):
        # we dont need to get the returned vector db from qdrant only but we intiate 
        # scheme so will use it in a different thing and make it general scheme
        results =  self.client.search(
            collection_name= collection_name,
            query_vector= vector,
            limit= limit
        )
        if not results or len(results) == 0:
            return None

        # return[
        #     Retrived_document(**{
        #         "score":result.score,
        #         "text": result.payload["text"]
        #     })
        #     for result in results
        # ]