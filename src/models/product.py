from sqlmodel import SQLModel, Field
from sqlalchemy import Column, Numeric

from decimal import Decimal




class Product(SQLModel, table=True):
    """Database table model"""
    id:       int | None = Field(default=None, primary_key=True)
    name:     str        = Field(index=True)
    price:    Decimal    = Field(sa_column=Column(Numeric(10, 2)))
    quantity: int




class ProductCreate(SQLModel):
    """Creation of a new product"""
    
    name:     str     = Field(min_length=1, max_length=255)
    price:    Decimal = Field(gt=0, decimal_places=2)
    quantity: int     = Field(ge=0)


class ProductUpdate(SQLModel):
    """Update for an existing product"""
    
    name:     str     | None = Field(default=None, min_length=1, max_length=255)
    price:    Decimal | None = Field(default=None, gt=0, decimal_places=2)
    quantity: int     | None = Field(default=None, ge=0)


class ProductRead(SQLModel):
    """Client read only"""
    
    id:       int
    name:     str
    price:    Decimal
    quantity: int