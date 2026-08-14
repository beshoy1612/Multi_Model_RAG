from fastapi import FastAPI,APIRouter,Depends,UploadFile,status
from Helper_Function import config , load_config
from fastapi.responses import JSONResponse
from Controllers import Data_controller
from models import Project_Enum
from logging import Logger
# log = Logger.error("")
data_route = APIRouter(
    prefix="/data"
)
@data_route.post("/upload/{project_id}")
async def upload(project_id:str,uploded_file:UploadFile,settings : config = Depends(load_config)):
   
   is_success,signal = Data_controller().validate_project_files(file=uploded_file)

   if not is_success :
      return JSONResponse(
         status_code = status.HTTP_400_BAD_REQUEST,
         content={
            "signal":signal
         }
      )
   
   file_path,file_id = Data_controller().generate_unique_path(project_id=project_id,file_name=uploded_file.filename)

   try:
      with open(file_path, "wb") as f:
         while content := await uploded_file.read(settings.FILE_CHUNK_SIZE):
            f.write(content)
   except Exception as error:
      return JSONResponse(
         status_code=status.HTTP_400_BAD_REQUEST,
         content={
            "signal":Project_Enum.FILE_UPLOADED_FAILED.value,
            "error":str(error)
         }
      )
   return JSONResponse(
            content={
               "signal":Project_Enum.FILE_UPLOADED_SUCCESSFULLY.value,
               "file_id":file_id,
               "file_path":file_path
            }
         )
