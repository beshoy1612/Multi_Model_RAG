from Helper_Function.config import config , load_config
from fastapi import FastAPI, APIRouter, Depends

base_app = APIRouter(
    prefix="/info"
)

@base_app.get("/test")
async def app_infiormation(app_config : config = Depends(load_config)):
    return{
        "app_name" : app_config.APP_NAME,
        "app_version" : app_config.APP_VERSION
    }