from fastapi import APIRouter

from .pets import router as pets_router

v1_router = APIRouter(prefix="/v1")
v1_router.include_router(pets_router)
