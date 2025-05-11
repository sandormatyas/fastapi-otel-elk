from fastapi import FastAPI
from app.routers.v1 import v1_router

app = FastAPI()
app.include_router(v1_router)
