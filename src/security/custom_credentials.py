from typing import Any, Dict, List, Optional, Union

from fastapi.exceptions import HTTPException
from fastapi.openapi.models import OAuth2 as OAuth2Model
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel
from fastapi.param_functions import Form
from fastapi.security.base import SecurityBase
from fastapi.security.utils import get_authorization_scheme_param
from starlette.requests import Request
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN


class OAuth2PasswordRequestCustomForm:

    def __init__(
            self,
            phone: str = Form(),
            password: str = Form(),
    ):
        self.grant_type = None
        self.phone = phone
        self.password = password
        self.scopes = ""
        self.client_id = None
        self.client_secret = None
