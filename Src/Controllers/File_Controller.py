from Base_Controller import Base_controller
from ..Helper_Function.config import config,load_config
import os


class File_controller(Base_controller):
    def __init__(self):
        super().__init__()

    def get_uploaded_file_path(self,project_id:str):
        path_of_project = os.path.join(
            self.file_dir,
            project_id
        )
        # make folder for each project 
        if not os.path.exists(path_of_project):
            os.makedirs(path_of_project)

        return path_of_project