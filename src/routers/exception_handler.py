from starlette.requests import Request
from starlette.responses import JSONResponse

from src.exceptions.unicorn_exception import UnicornException
from src.routers.schemas import PostResult


async def unicorn_error(request: Request, exc: UnicornException):
    return JSONResponse(content=PostResult(success=False, error=exc.error).__dict__)
