from enum import Enum
class LLMenum(Enum):
    #store any name of provider we will use 
    COHERE = "COHERE"
    GEMENI = "GEMENI"

class CoHereEnum(Enum):
    SYSTEM = "SYSTEM" 
    USER = "USER"
    ASSISTANT = "CHATBOT"
    DOCUMENT = "search_document"
    QUERY = "search_query"

class DocumentTypeEnum(Enum):
    DOCUMENT = "document" 
    QUERY = "query"   