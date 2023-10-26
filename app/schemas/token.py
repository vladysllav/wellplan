from typing import Optional

from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    refresh_token: str


class RefreshToken(Token):
    access_token: Optional[str] = None
    refresh_token: Optional[str] = None
