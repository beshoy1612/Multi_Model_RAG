from pydantic_settings import BaseSettings, SettingsConfigDict

class config(BaseSettings):

    APP_NAME :str
    APP_VERSION :str

    #SettingsConfigDict tells Pydantic where and how to load environment variables
    # we must call same varaible name

    model_config = SettingsConfigDict(
        env_file = ".env",
        env_file_encoding = "utf-8" 
    )

def load_config():
    return config() # dont forget () its class
