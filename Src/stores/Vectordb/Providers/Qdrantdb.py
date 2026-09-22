from ..Vectordb_Interface import Vectordb_Interface
import logging

class Qdrantdb(Vectordb_Interface):
    def __init__(self):
        super().__init__()