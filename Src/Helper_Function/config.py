from pydantic_settings import BaseSettings, SettingsConfigDict

class config(BaseSettings):

    APP_NAME :str
    APP_VERSION :str
    FILES_VALID_CONTENT_TYPE :list
    FILE_VALID_SIZE:int
    FILE_CHUNK_SIZE:int
    POSTGRES_USERNAME:str
    POSTGRES_PASSWORD:str
    POSTGRES_HOST:str
    POSTGRES_PORT:int
    POSTGRES_MAIN_DATABASE:str

    ####### Gemeni , COHERE providers  ##########
    
    # COHERE
    COHERE_API_KEY :str
    GENERATION_MODEL_ID :str
    EMBEDDING_MODEL_ID :str
    EMBEDDING_MODEL_SIZE :int

    default_input_max_character :int  = None
    default_output_max_character :int  = None
    default_generation_temprature :float  = None 
    
    #GEMENI
    GEMINI_API_KEY :str
    default_output_max_tokens: int
    VLM_MODEL_ID: str

    # vector db config
    VECTOR_DB: str
    VECTOR_DB_PATH: str
    VECTOR_DB_DISTANNCE_METHOD: str = None

    GENERATION_BACKEND: str
    EMBEDDING_BACKEND: str
    #SettingsConfigDict tells Pydantic where and how to load environment variables
    # we must call same varaible name

    model_config = SettingsConfigDict(
        env_file = ".env",
        env_file_encoding = "utf-8" 
    )

def load_config():
    return config() # dont forget () its class
