from src.exceptions.unicorn_exception import UnicornException
from src.routers.payload.message_payload import MessagePayload


class MessageService:
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = MessageService()
        return cls._instance

    def process_message(self, message: MessagePayload) -> str:
        if message.age <= 0:
            raise UnicornException("Age must be greater than 0")
        if message.weight <= 0:
            raise UnicornException("Weight must be greater than 0")
        return f"Seems like your name is {message.firstname} {message.lastname} " \
               f"and you're {message.age} years old and your weight is {message.weight}"
