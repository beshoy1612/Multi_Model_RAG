from Helper_Function import load_config,config

class Base_model():
    def __init__(self,  db_client: object):
        self.db_client =db_client
        self.app_setting = load_config()
        