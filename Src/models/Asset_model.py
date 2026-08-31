from .Base_model import Base_model
from .db_schemes import Assets
from sqlalchemy.future import select
from sqlalchemy import func,delete
class Asset_model(Base_model):
    def __init__(self, db_client :object):
        super().__init__(db_client = db_client)
        self.db_client = db_client


    @classmethod
    async def create_instance(cls, db_client: object):
        instance = cls(db_client) # call __init__
        return instance


    async def create_Asset(self, asset:Assets):
        async with self.db_client() as session:
            async with session.begin():       
                session.add(asset)
            await session.commit()
            await session.refresh(asset)
    
    
    async def get_all_project_files(self,asset_project_id:str,asset_type:str):
        async with self.db_client() as session:
            stmt = select(Assets).where(
                Assets.Asset_project_id == asset_project_id,
                Assets.Asset_type == asset_type
            )
            result = await session.execute(stmt)
            records = result.scalar().all()
        return records

         
    async def get_Asset_record(self, asset_project_id:str,asset_name:str):
        async with self.db_client() as session:
            stmt = select(Assets).where(
                Assets.Asset_project_id == asset_project_id,
                Assets.Asset_type == asset_name
            )
            result = await session.execute(stmt)
            records = result.scalar_one_or_none()
        return records