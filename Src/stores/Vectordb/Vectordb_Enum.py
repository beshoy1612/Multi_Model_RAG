from enum import Enum

class Vectordb_Enum(Enum):
    # dont need to engine like mongo_db , postgress (engine based data base)
    # file base database , memory database like pinecorn, pgvector , qdrant
    # we will not find url database like mongo but we will pass path or memoery
    QDRANT = "QDRANT"

class DistanceMethod(Enum):
    COSINE = "cosine"
    DOT = "dot"