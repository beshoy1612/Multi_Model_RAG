from Helper_Function.config import config, load_config
import os
from pydantic import BaseModel

#base controller cant take basemodel
class Base_controller:
    def __init__(self):
        self.app_config = load_config()
        self.base_dir = os.path.dirname(os.path.dirname(__file__))
        self.file_dir = os.path.join(
            self.base_dir,
            "Assets/File"
        )
        self.database_dir = os.path.join(
            self.base_dir,
            "Assets/vector_database"
        )
    def get_database_path(self,db_name: str):
        database_path = os.path.join(
            self.database_dir,
            db_name
        )
        if not os.path.exists(database_path):
            os.makedirs(database_path)
            
        return database_path