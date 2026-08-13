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