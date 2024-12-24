from pydantic import BaseModel
from typing import Optional


class ProductBase(BaseModel):
    name: str
    description: str
    price: float
    category: str


class ProductCreateUpdate(ProductBase):
    pass


class ProductResponse(ProductBase):
    id: int
    image_path: str
    user: str  

    class Config:
        from_attributes = True
