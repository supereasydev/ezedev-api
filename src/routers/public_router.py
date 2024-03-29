from fastapi import APIRouter

from src.routers.payload.message_payload import MessagePayload
from src.routers.schemas import PostResult
from src.services.message_service import MessageService

router = APIRouter(
    prefix='',
    tags=['public']
)

message_service = MessageService.get_instance()


@router.get('/makeHandshake')
async def make_handshake():
    return {
        'message': 'Welcome to ezedev backend'
    }


@router.post('/messages', response_model=PostResult)
async def post_message(message_payload: MessagePayload):
    return PostResult(success=True,
                      message=message_service.process_message(message_payload))
