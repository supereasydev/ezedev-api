from fastapi import APIRouter

from src.routers.payload.message_payload import MessagePayload

router = APIRouter(
    prefix='',
    tags=['users']
)


@router.get('/makeHandshake')
async def make_handshake():
    return {
        'message': 'Welcome to EZEDEV backend!'
    }


@router.post('/messages')
async def post_message(message_payload: MessagePayload):
    return {
        "postedSuccessfully": True,
        "message": f"Seems like your name is {message_payload.firstname} {message_payload.lastname} "
                   f"and you're {message_payload.age} years old and your weight is {message_payload.weight}",
        "error": None
    }
