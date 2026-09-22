from .Providers import Qdrantdb
from .Vectordb_Enum import Vectordb_Enum
from Controllers.Base_Controller import Base_controller
class Vectordb_Provider_Factory:
    def __init__(self,config):
        self.config = config
        self.base_controller = Base_controller()

    def create(self ,provider: str):
        if provider == Vectordb_Enum.QDRANT.value:
            db_path = self.base_controller.get_database_path(db_name=self.config.VECTOR_DB_PATH)
            return Qdrantdb(
                db_path=db_path,
                distance_method=self.config.VECTOR_DB_DISTANNCE_METHOD
            )
        return None