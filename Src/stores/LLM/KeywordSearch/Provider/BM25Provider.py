from ..KeywordSearch_Interface import KeywordSearch_Interface
import logging
from rank_bm25 import BM25Okapi
from typing import List,Tuple
import re

class BM25Provider(KeywordSearch_Interface):

    ARABIC_CHARACTERS = re.compile(r"[\u0617-\u061A\u064B-\u0652\u0640]")
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.collections = {}

    def is_collection_existed(self, collection_name):
        return collection_name in self.collections

    def delete_collection(self, collection_name):
        if self.is_collection_existed(collection_name):
            del self.collections[collection_name]
            return True
        return False

    def tokenize(self, text: str) -> List[str]:
        text = text.lower()                         
        text = self.ARABIC_CHARACTERS.sub("", text)  
        text = re.sub("[إأآ]", "ا", text)           
        text = text.replace("ى", "ي")               
        return re.findall(r"\w+", text)   


    def add_documents(self,collection_name: str,texts: List[str],ids: List[int]) -> bool:

        if not texts or len(texts) != len(ids):
            self.logger.error(
                "texts and ids must be non-empty and have the same length"
            )
            return False

        #  Create collection if it doesn't exist
        if not self.is_collection_existed(collection_name):
            self.collections[collection_name] = {
                "ids": [],
                "texts": [],
                "tokenized": [],
                "bm25": None
            }

        col = self.collections[collection_name]

        #  Add documents
        col["ids"].extend(ids)
        col["texts"].extend(texts)

        #  Tokenize documents
        tokenized_texts = [
            self.tokenize(text)
            for text in texts
            ]

        col["tokenized"].extend(tokenized_texts)

        # Rebuild BM25 index
        col["bm25"] = BM25Okapi(col["tokenized"])

        return True

    def search(self,collection_name: str,query: str,limit: int) -> List[Tuple[int, float]]:

        # Check collection
        col = self.collections.get(collection_name)

        if not col or col["bm25"] is None:
            return []

        # Validate limit
        if limit <= 0:
            return []

        # Tokenize query
        query_tokens = self.tokenize(query)

        if not query_tokens:
            return []

        #  Calculate BM25 score for every document
        scores = col["bm25"].get_scores(query_tokens)

        #  Get top documents
        top_indexes = sorted(
            range(len(scores)),
            key=lambda i: scores[i],
            reverse=True
        )[:limit]

        # Return document IDs with their scores
        return [
            (col["ids"][i], float(scores[i]))
            for i in top_indexes
            if scores[i] > 0
        ]