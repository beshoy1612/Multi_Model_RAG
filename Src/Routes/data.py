from fastapi import FastAPI,APIRouter,Depends,UploadFile,status
from Helper_Function.config import config , load_config
from fastapi.responses import JSONResponse
from Controllers.Data_controller import Data_controller

data_route = APIRouter(
    prefix="/data"
)
@data_route.post("/upload {file_id}")
async def upload(file_id:str,uploded_file:UploadFile,settings : config = Depends(load_config)):
   
   is_success,signal = Data_controller().validate_project_files(file=uploded_file)

   if not is_success :
      return JSONResponse(
         status_code = status.HTTP_400_BAD_REQUEST,
         content={
            "signal":signal
         }
      )
   
   file_path,file_id = Data_controller().generate_unique_path(file_id=file_id,file_name=uploded_file.filename)

   return file_path,file_id