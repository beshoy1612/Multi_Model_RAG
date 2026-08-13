from fastapi import FastAPI,APIRouter,Depends,UploadFile
from Helper_Function.config import config , load_config
import os
from fastapi.responses import JSONResponse

data_route = APIRouter(
    prefix="/data"
)
@data_route.post("/upload {file_id}")
async def upload(file_id:str,uploded_file:UploadFile,settings : config = Depends(load_config)):
    pass