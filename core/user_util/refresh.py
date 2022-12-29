from fastapi import APIRouter
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi import Security

from core.user_util.jwt_utils import decode_refresh_token

router = APIRouter()
security = HTTPBearer()


# Refresh access token
@router.get('')
def refresh_token(credentials: HTTPAuthorizationCredentials = Security(security)) -> dict:
    token = credentials.credentials
    new_token = decode_refresh_token(token)
    return {
        'access_token': new_token
     }
