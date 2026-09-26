from fastapi import FastAPI, APIRouter,Depends,UploadFile,status,Request
from fastapi.responses import JSONResponse
from models.Project_model import Project_model
from Controllers import NLP_Conroller
from models import Project_Enum
from models.Chunk_model import Chunk_model
from typing import Optional
from pydantic import BaseModel
import os
import logging

logger = logging.getLogger("uvicorn.error")

nlp_router = APIRouter(
    prefix="/api/v1/nlp"
)

class Push_Request(BaseModel):
    do_reset:Optional[int] = 0

class Search_Request(BaseModel):
    text: str
    limit:Optional[int] = 5



# here we will use all logic we built in (NLP_Controller) we could implement all logic here but what is the benefit from (MVC) ?
# we hust call fuctions that we implemented in NLP_Controller


#first: end point to store embedding text into vector db 
@nlp_router.post("/index/push/{project_id}")
async def index_project(request:Request,project_id:str,push_request:Push_Request):
   
    project_model = Project_model(db_client = request.app.db_client)
    project = await project_model.get_project_or_create_one(project_id = int(project_id))

    if not project :
        return JSONResponse(
            status_code = status.HTTP_400_BAD_REQUEST,
            content = {
                "siganl" : Project_Enum.PROJECT_NOT_FOUND_ERROR.value 
            }
        )
    nlpcontroller = NLP_Conroller(
        vectordb_client = request.app.vectordb_client,
        embedding_client = request.app.embedding_client,
        generation_client = request.app.generation_client,
        # template_parser=request.app.template_parser
    )

    # now we will get chunk for project to push it in vector database 
    chunkmodel = await Chunk_model(db_client = request.app.db_client)

    is_record = True
    page_no = 1
    inserted_count = 0
    idx = 0

    while(is_record):

        page_chunks = await chunkmodel.get_project_chunk(project_id=project.Projcet_id,page_no=page_no)

        if len(page_chunks):
            page_no+=1

        if len(page_chunks) == 0 or not page_chunks :
            is_record = False
            break

        chunk_id = list(range(idx,idx+len(page_chunks)))
        idx += len(page_chunks)
        
        is_inserted = nlpcontroller.index_into_vector_db(
            project = project,
            chunk = page_chunks,
            do_reset = push_request.do_reset,
            chunk_ids= chunk_id
            )   
        if not is_inserted:
            return JSONResponse(
                status_code= status.HTTP_400_BAD_REQUEST,
                content={
                    "signal" : Project_Enum.INSERT_INTO_VECTOR_DB_ERROR.value
                }
            )
        inserted_count+= len(page_chunks)

    return JSONResponse(
        content={
            "signal" : Project_Enum.INSERT_INTO_VECTOR_DB_SUCESS.value,
            "inserted_item_count": inserted_count
        }
    )