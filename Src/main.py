from Routes import base,data
from fastapi import FastAPI,APIRouter
from Helper_Function import config,load_config
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
    
@app.on_event("shutdown")
async def shutdown_db_client():
    app.db_engine.dispose()

app.include_router(base.base_app)
app.include_router(data.data_route)