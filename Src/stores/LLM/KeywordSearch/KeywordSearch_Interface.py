from abc import ABC, abstractmethod
from typing import List, Tuple


class KeywordSearch_Interface(ABC):

    @abstractmethod
    def is_collection_existed(self, collection_name: str) -> bool:
        pass

    @abstractmethod
    def delete_collection(self, collection_name: str):
        pass


    @abstractmethod
    def add_documents(self, collection_name: str, texts: List[str], ids: List[int]) -> bool:
        pass

    # return sorted list from retrivel text from most suitable to less
    @abstractmethod
    def search(self, collection_name: str, query: str, limit: int) -> List[Tuple[int, float]]:
        pass