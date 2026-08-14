from Controllers import Base_Controller,Project_Controller
from langchain_community.document_loaders import TextLoader
from langchain_community.document_loaders import PyMuPdfLoader
import os

class Process_Controller(Base_Controller):
    def __init__(self):
        super().__init__()

    def get_file_ext(self,file_id:str):
        return os.path.splitext(file_id)[-1]

    def get_file_loader(self,file_id:str,project_id:str):
        file_ext = self.get_file_ext(file_id=file_id)
        file_path =os.path.join(
        Project_Controller().get_uploaded_file_path(project_id=project_id),
        file_id 
        )

        if file_ext == ".txt":
            return TextLoader(file_path,encoding ="utf-8")
        
        if file_ext ==".pdf":
            pass