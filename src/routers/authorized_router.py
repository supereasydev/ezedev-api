from fastapi import APIRouter, Depends, Security
from fastapi.security import APIKeyHeader
from fastapi_users import FastAPIUsers

from src.persistence.models.user_model import UserModel
from src.security.configuration import auth_backend
from src.security.user_manager import get_user_manager

fastapi_users = FastAPIUsers[UserModel, int](
    get_user_manager,
    [auth_backend],
)

router = APIRouter(
    prefix='',
    tags=['authorized']
)

current_user = fastapi_users.current_user()
auth_header = APIKeyHeader(name='Authorization', scheme_name='Bearer token')


@router.get('/current_profile')
async def get_current_profile(header_value=Security(auth_header), user=Depends(current_user)):

    return {
        'name': f'{user.firstname} {user.lastname}',
        'age': user.age
    }
