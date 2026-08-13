from Routes import base
from fastapi import FastAPI,APIRouter

app =FastAPI()
app.include_router(base.base_app)