from sqlmodel import SQLModel, Field

from decimal import Decimal




class UserBase(SQLModel):
    """Base user model"""
    username:  str  = Field(index=True, unique=True)
    email:     str  | None = None
    full_name: str  | None = None
    disabled:  bool | None = False


class UserDB(UserBase, table=True):
    """Database table model"""
    id:              int | None = Field(default=None, primary_key=True)
    hashed_password: str


class UserCreate(UserBase):
    """New user creation"""
    password: str


class UserRead(UserBase):
    """Read only"""
    id: int