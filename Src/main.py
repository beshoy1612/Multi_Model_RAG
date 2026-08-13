from Routes import base,data
from fastapi import FastAPI,APIRouter

app =FastAPI()
app.include_router(base.base_app)
app.include_router(data.data_route)