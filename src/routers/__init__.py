from fastapi import APIRouter
from src.routers.public_router import router as public_router
from src.routers.authorized_router import router as authorized_router
from src.security.auth import get_auth_router
from src.security.configuration import auth_backend
from src.security.user_manager import get_user_manager

root_router = APIRouter(
    prefix=''
)

root_router.include_router(public_router)
root_router.include_router(authorized_router)

root_router.include_router(
    get_auth_router(auth_backend, get_user_manager),
    prefix="",
)