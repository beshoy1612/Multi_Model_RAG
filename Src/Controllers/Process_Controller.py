from Controllers.Base_Controller import Base_controller
from Controllers.Project_Controller import Project_Controller
from langchain_community.document_loaders import TextLoader
# from langchain_community.document_loaders import PyMuPdfLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os

class Process_Controller(Base_controller):
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
        return None

    def get_file_content(self,file_id:str,project_id:str):
        load_data = self.get_file_loader(file_id=file_id,project_id = project_id)
        if load_data :
            # return file as a list of content
            return load_data.load()
        return None


    def process_file_content(self,file_content:list,chunk_size=100,overlap_size=20):
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size = chunk_size,
            chunk_overlap = overlap_size,
            length_function = len
        )
        chunks = text_splitter.split_documents(file_content)

        return chunks
