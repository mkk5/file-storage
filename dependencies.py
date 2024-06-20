from pydantic import BaseModel, UUID4, EmailStr, Field
from fastapi import HTTPException, Cookie
from typing import Annotated
import jwt


class Email(BaseModel):
    address: EmailStr
    is_primary: bool
    is_verified: bool


class User(BaseModel):
    id: UUID4 = Field(validation_alias="sub")
    email: Email


async def get_current_user(hanko: Annotated[str | None, Cookie()] = None) -> User:
    if hanko is None:
        raise HTTPException(status_code=302, detail="Unauthorized: Missing Token", headers={"Location": "/"})
    jwks_client = jwt.PyJWKClient(
        "https://example.hanko.io/.well-known/jwks.json"
    )
    try:
        data = jwt.decode(
            hanko,
            jwks_client.get_signing_key_from_jwt(hanko).key,
            algorithms=["RS256"],
            audience="localhost",
        )
    except Exception:
        raise HTTPException(status_code=302, detail="Unauthorized: Invalid Token", headers={"Location": "/"})
    return User(**data)
