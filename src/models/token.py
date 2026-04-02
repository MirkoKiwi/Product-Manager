from sqlmodel import SQLModel




class Token(SQLModel):
    """Login response"""
    access_token: str
    token_type:   str


class TokenData(SQLModel):
    """Inside payload"""
    username: str | None = None