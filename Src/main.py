from .Routes import base,data
from fastapi import FastAPI,APIRouter
from .Helper_Function import config,load_config
from stores.LLM.LLMProviderFactory import LLMProviderFactory
from stores.Vectordb.Vectordb_Provider_Factory import Vectordb_Provider_Factory
#library to mange postgres database
#take postgres connection ==> create_async_engine
from sqlalchemy.ext.asyncio import create_async_engine,AsyncSession   
from sqlalchemy.orm import sessionmaker 

app =FastAPI()
@app.on_event("startup")
async def startup_app():
    settings = load_config()
    postgres_conn = f"postgresql+asyncpg://{settings.POSTGRES_USERNAME}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_MAIN_DATABASE}"
    app.dp_engine = create_async_engine(postgres_conn)
    app.db_client = sessionmaker(
        # class_ = AsyncSession to Benfit from async in fast api not normal database
        # DONT EXPIRE SESSION WHEN COMMIT ==> expire_on_commit=False
        app.dp_engine,class_ = AsyncSession,expire_on_commit=False
    )
    llm_provider_factory =  LLMProviderFactory(settings)
    vectordb_provider_factory = Vectordb_Provider_Factory(settings)

    #generation client 
    app.generation_client = llm_provider_factory.create(provider=settings.GENERATION_BACKEND)
    app.generation_client.set_generation_model(model_id= settings.GENERATION_MODEL_ID)

    #embadding client 
    app.embadding_client = llm_provider_factory.create(provider=settings.EMBEDDING_BACKEND)
    app.embadding_client.set_embedding_model(model_id= settings.EMBEDDING_MODEL_ID,
                                             embedding_size=settings.EMBEDDING_MODEL_SIZE)

    #vectordb_client
    app.vectordb_client = vectordb_provider_factory.create(provider= settings.VECTOR_DB)
    app.vectordb_client.connect()

@app.on_event("shutdown")
async def shutdown_db_client():
    app.db_engine.dispose()
    app.vectordb_client.disconnect()

app.include_router(base.base_app)
app.include_router(data.data_route)