from sqlmodel import SQLModel, Field
from sqlalchemy import Column, Numeric

from decimal import Decimal
from datetime import datetime




class Product(SQLModel, table=True):
    id:       int | None = Field(default=None, primary_key=True)
    name:     str
    price:    Decimal = Field(sa_column=Column(Numeric(10, 2)))     # 10 Digits before comma, 2 after comma
    quantity: int


class ProductForm(SQLModel):
    name:     str
    price:    Decimal
    quantity: int