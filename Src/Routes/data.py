from fastapi import FastAPI,APIRouter,Depends,UploadFile,status,Request
from Helper_Function import config , load_config
from fastapi.responses import JSONResponse
from Controllers import Data_controller,Process_Controller
from models import Project_Enum
from logging import Logger
from models import Project_model,Chunk_model,Asset_model,Base_model
from models import Data_chunk,Assets

# log = Logger.error("")
data_route = APIRouter(
    prefix="/data"
)
@data_route.post("/upload/{project_id}")
async def upload(request:Request,project_id:str,uploded_file:UploadFile,settings : config = Depends(load_config)):

   project_model = Project_model( db_client = request.app.db_client)
   project = await project_model.get_project_or_create_one(project_id = int(project_id))

   
   
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
   asset_model = Asset_model(
   db_client=request.app.db_client
   )

   asset = Assets(
      Asset_name=file_id,
      Asset_type="file",
      Asset_size=0,  
      Asset_project_id=project.Projcet_id
   )

   await asset_model.create_Asset(asset)

   return JSONResponse(
      content={
         "signal": Project_Enum.FILE_UPLOADED_SUCCESSFULLY.value,
         "file_id": file_id,
         "file_path": file_path,
         "asset_id": asset.Asset_id
      }
   )
   # return JSONResponse(
   #          content={
   #             "signal":Project_Enum.FILE_UPLOADED_SUCCESSFULLY.value,
   #             "file_id":file_id,
   #             "file_path":file_path
   #          }
   #       )

@data_route.post("Process_file/{project_id}/{file_id}")
async def process_file(request:Request,project_id:str,file_id:str):

   project_model = Project_model(db_client = request.app.db_client)
   project = await project_model.get_project_or_create_one(project_id = int(project_id))

   asset_model =  Asset_model(db_client=request.app.db_client)
   asset_record = await asset_model.get_Asset_record(asset_project_id=project.Projcet_id,asset_name=file_id)
   
   if asset_record is None:
      return JSONResponse(
         status_code=status.HTTP_400_BAD_REQUEST,
         content={
            "signal":Project_Enum.NO_FILE_EXIST.value
         }
      )
   
   Process_Control = Process_Controller()
   file_content = Process_Control.get_file_content(file_id=file_id,project_id=int(project_id))

   if not file_content:
      return JSONResponse(
         status_code=status.HTTP_400_BAD_REQUEST,
         content={
            "signal":[
               Project_Enum.PROCESSING_FAILED.value,
               Project_Enum.File_NOT_FOUND_OR_COULD_NOT_BE_LOADED.value
                      ]
         }
      )
   file_chunks = Process_Control.process_file_content(file_content=file_content)

   if not file_chunks:
      return JSONResponse(
         status_code=status.HTTP_400_BAD_REQUEST,
         content={
               "signal": [
                  Project_Enum.PROCESSING_FAILED.value,
                  Project_Enum.FILE_COULD_NOT_BE_SPLIT.value
               ]
         }
      )
   
   # return JSONResponse(
   #    content={
   #       "signal": Project_Enum.PROCESSING_SUCCESS.value,
   #       "chunks_count": len(file_chunks),
   #       "chunks": [
   #             {
   #                "content": chunk.page_content,
   #                "metadata": chunk.metadata
   #             }
   #             for chunk in file_chunks
   #       ]
   #    }
   # )
   file_chunk_record = [
      Data_chunk(
            Chunk_text = chunk.page_content,
            Chunk_metadata = chunk.metadata,
            Chunk_project_id = project.Projcet_id,
            Chunk_assets_id = asset_record.Asset_id
            )
            for chunk in file_chunks
      ]
   chunk_model = Chunk_model(db_client=request.app.db_client)
   insert_chunk = await chunk_model.insert_many_chunks(chunks=file_chunk_record)
   return JSONResponse(
      content={
         "signal":Project_Enum.PROCESSING_SUCCESS.value,
         "inserted_chunks":insert_chunk
      }
   )