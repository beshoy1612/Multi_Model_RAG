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
    #SettingsConfigDict tells Pydantic where and how to load environment variables
    # we must call same varaible name

    model_config = SettingsConfigDict(
        env_file = ".env",
        env_file_encoding = "utf-8" 
    )

def load_config():
    return config() # dont forget () its class
