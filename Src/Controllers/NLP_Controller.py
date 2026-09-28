from .Base_Controller import Base_controller
from models.db_schemes import Project,Data_chunk
from ..stores.LLM.LLMenum import DocumentTypeEnum
from typing import List
import json


#===============================================================================||
# we will implement all logic about semantic search , retrival here !!!!!!!!    ||
# so we will need generation_client,embadding_client,vectordb_client            ||
#===============================================================================||

class NLP_Controller(Base_controller):
    def __init__(self,generation_client,embadding_client,vectordb_client,reranker_client,keyword_search_client):
        super().__init__()
        self.generation_client = generation_client
        self.embadding_client = embadding_client
        self.vectordb_client = vectordb_client
        self.reranker_client = reranker_client
        self.keyword_search_client = keyword_search_client


    # we will use this function in  each function in this controller 
    def create_collection_name(self , project_id:str):
        return f"collection_{project_id}".strip()

    def reset_vector_db_collection(self,project:Project):
        collection_name = self.create_collection_name(project_id = project.id)


        # this function delete_collection(collection_name = collection_name) from ====> Qdrantdb we implemented before
        return self.vectordb_client.delete_collection(collection_name = collection_name)

    def get_vetor_db_collection_info(self,project:Project) :
        collection_name = self.create_collection_name(project_id = project.id)
        collection_info = self.vectordb_client.get_collection_info(collection_name = collection_name)
        return json.loads(
            json.dumps(collection_info,default=lambda x:x.__dict__)
        )


    
    # this is the most important function in this level =============important==================

    def index_into_vector_db(self,project:Project,chunk:List[Data_chunk],
                             chunk_ids:List[int],
                             do_reset:bool = False):
        
        #step 1: get collection name
        collection_name = self.create_collection_name(project_id = project.id)

        #step 2: manage items
        text = [c.chunk_text for c in chunk]
        meta_data = [c.chunk_metadata for c in chunk]
        vectors = [
            self.embadding_client.embed_text(text = i ,document_type = DocumentTypeEnum.DOCUMENT.value )
            for i in text
        ]

        #step 3: create collection 
        _ = self.vectordb_client.create_collection(
            collection_name = collection_name,
            embedding_size = self.embadding_client.embedding_size,
            do_reset = do_reset
            ) 
        
        #step 4: insert into database
        _ = self.vectordb_client.insert_many(
            collection_name = collection_name ,
            text = text ,
            vector = vectors,
            metadata = meta_data,
            record_id = chunk_ids,
            )
        return True

    
    def search_vector_db_collection (self,project:Project ,text :str ,limit:int = 10):
        # 1 - get collection name
        collection_name = self.create_collection_name(project_id = project.id)

        # 2 - get text embedding vector
        vector  = self.embadding_client.embed_text(text = text,document_type = DocumentTypeEnum.QUERY.value)
        if not vector or len(vector) == 0:
            return False
        
        # 3 - do semantic search
        result = self.vectordb_client.search_by_vector(
            collection_name = collection_name,
            vector = vector,
            limit = limit
                )
        if not result :
            return False
        
        return result


    # Keyword Search Indexing
    def index_into_keyword_search(self,project: Project,chunk: List[Data_chunk],chunk_ids: List[int]):

        collection_name = self.create_collection_name(
            project_id=project.id
        )

        text = [
            c.chunk_text
            for c in chunk
        ]

        result = self.keyword_search_client.add_documents(
            collection_name=collection_name,
            texts=text,
            ids=chunk_ids
        )

        return result

    # Keyword Search
    def search_keyword_search_collection(self,project: Project,text: str,limit: int = 10):

        collection_name = self.create_collection_name(
            project_id=project.id
        )

        result = self.keyword_search_client.search(
            collection_name=collection_name,
            query=text,
            limit=limit
        )

        if not result:
            return False

        return result

    def RRF(self,vector_results: list, keyword_results: list, k: int = 60):
        scores = {}

        # Vector results
        for rank, result in enumerate(vector_results, start=1):
            doc_id = result["id"]

            scores[doc_id] = scores.get(doc_id, 0) + (
                1 / (k + rank)
            )

        # Keyword results
        for rank, result in enumerate(keyword_results, start=1):
            doc_id = result["id"]

            scores[doc_id] = scores.get(doc_id, 0) + (
                1 / (k + rank)
            )

        results = [
            {
                "id": doc_id,
                "score": score
            }
            for doc_id, score in scores.items()
        ]

        results.sort(
            key=lambda x: x["score"],
            reverse=True
        )

        return results

    
    async def rerank(self,query: str,rrf_results: list,limit: int = 5):
        if not rrf_results:
            return []

        chunk_ids = [
            result["id"]
            for result in rrf_results
        ]

        chunks = await self.get_chunks_by_ids(
            chunk_ids=chunk_ids
        )

        if not chunks:
            return []

        documents = [
            chunk.chunk_text
            for chunk in chunks
        ]

        rerank_results = self.reranker_client.rerank(
            query=query,
            documents=documents,
            limit=limit
        )

        return rerank_results

    # this function  has all logic about search_keyword_search_collection & search_vector_db_collection
    # and RRF & RERANK  and we will call it in NLP route
    
    async def hybrid_search(self,project: Project,query: str,limit: int = 5):
        # 1. Vector Search
        vector_results = self.search_vector_db_collection(
            project=project,
            text=query,
            limit=10
        )

        # 2. BM25 Search
        keyword_results = self.search_keyword_search_collection(
            project=project,
            text=query,
            limit=10
        )

        # 3. RRF
        rrf_results = self.reciprocal_rank_fusion(
            vector_results=vector_results,
            keyword_results=keyword_results
        )

        # 4. Rerank
        final_results = await self.rerank(
            query=query,
            rrf_results=rrf_results,
            limit=limit
        )

        return final_results