from .Provider import BM25Provider
from .KeywordSearch_Enum import KeywordSearch_Enum


class KeywordSearch_Provider_Factory:

    def __init__(self, config):
        self.config = config

    def create(self, provider: str):
        if provider == KeywordSearch_Enum.BM25.value:
            return BM25Provider()

        return None