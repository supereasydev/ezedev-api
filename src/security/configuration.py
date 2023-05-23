from fastapi_users.authentication import BearerTransport, JWTStrategy, AuthenticationBackend

from src.config import Config

SECRET = Config.get_instance().jwt_secret
bearer_transport = BearerTransport(tokenUrl="login")


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)
