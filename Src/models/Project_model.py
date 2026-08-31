from .Base_model import Base_model
from db_schemes import Project
from sqlalchemy.future import select
from sqlalchemy import func

class Project_model(Base_model):
    def __init__(self, db_client :object):
        super().__init__(db_client = db_client)
        self.db_client = db_client


    @classmethod
    async def create_instance(cls, db_client: object):
        instance = cls(db_client) # call __init__
        return instance

    async def create_project(self,project:Project):
        async with self.db_client() as session:
            async with session.begin():
                session.add(project)
            await session.commit()
            await session.refresh(project)

        return project

    async def get_project_or_create_one(self,project_id:int):
        async with self.db_client() as session:
            async with session.begin():    
                query = select(Project).where(Project.Projcet_id == project_id)
                result = await session.execute(query)
                project_rec = result.scalar_one_or_none()

                if project_rec is None:
                    fill_table = Project(
                        Projcet_id = project_id
                    )
                    project_rec = await self.create_project(project = fill_table)
                    return project_rec
                else :
                    return project_rec 


    async def get_all_projects(self,page: int=1,page_size: int=10):
        async with self.db_client() as session:
            async with session.begin(): 
                total_documents = await session.execute(select(
                    func.count(Project.Projcet_id)
                ))
                total_documents =total_documents.scalar_one()   
                total_pages = total_documents // page_size
                if total_documents % page_size > 0:
                    total_page += 1       

            query = select(Project).offset((page - 1 ) + page_size).limit(page_size)
            projects = await session.execute(query).scalar().all()

            return projects,total_pages 