from fastapi import Header, HTTPException, status

from core.auth_utils.auth import decode_access_token


def get_user_by_token(authorization: str = Header(..., alias="authorization")) -> int:
    try:
        type_, token = authorization.split()
        if type_ != "Bearer":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not using the Bearer schema",
            )
    except ValueError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return decode_access_token(token)
