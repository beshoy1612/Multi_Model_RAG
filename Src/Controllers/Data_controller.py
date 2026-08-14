from Controllers import Base_controller
from models import Project_Enum
from fastapi import UploadFile
from Controllers.Project_Controller import Project_Controller
import re
import os
import uuid

class Data_controller(Base_controller):
    def __init__(self):
        super().__init__()

    def validate_project_files(self,file:UploadFile):

        if file.content_type not in self.app_config.FILES_VALID_CONTENT_TYPE:
            return False ,Project_Enum.FILE_TYPE_NOT_SUPPORTED.value

        if file.size > self.app_config.FILE_VALID_SIZE:
            return False ,Project_Enum.FILE_SIZE_EXCEEDED.value

        return True,Project_Enum.FILE_VALIDATE_SUCCESSFULLY.value


    def get_clean_file_name(self,file_name:str):
        #remove any special characters  except .,_
        clean_file_name = re.sub(r'[^\w.]','',file_name.strip())  

        #replace spaces with underscore
        clean_file_name = clean_file_name .replace(" ","_")

        return clean_file_name 


    def generate_unique_path(self,project_id:str,file_name:str):

        project_path = Project_Controller().get_uploaded_file_path(project_id=project_id)
        cleaned_file_name = self.get_clean_file_name(file_name=file_name)
        unique_id = uuid.uuid4().hex
        unique_file_name = f"{unique_id}_{cleaned_file_name}"

        unique_path = os.path.join(
            project_path ,
            unique_file_name
        )
        while os.path.exists(unique_path):
            unique_id = uuid.uuid4().hex
            unique_file_name = f"{unique_id}_{cleaned_file_name}"
            unique_path = os.path.join(
            project_path ,
            unique_file_name
            )
    #   file_id = unique_id + clened_file_name,
        return  unique_path, unique_file_name
