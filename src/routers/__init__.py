from fastapi import APIRouter
from src.routers.public_router import router as public_router

root_router = APIRouter(
    prefix=''
)

root_router.include_router(public_router)
