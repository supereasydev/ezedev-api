from fastapi import APIRouter

router = APIRouter(
    prefix='',
    tags=['users']
)


@router.get('/makeHandshake')
async def make_handshake():
    return {
        'message': 'Welcome to EZEDEV backend!'
    }
