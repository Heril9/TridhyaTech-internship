from pydantic import BaseModel, Field, EmailStr
from typing import Optional

# Category Schemas
class CategoryBase(BaseModel):
    name: str = Field(min_length=2, max_length=50)

class CategoryCreate(CategoryBase):
    pass

class CategoryResponse(CategoryBase):
    id: int

    class Config:
        orm_mode = True

# Product Schemas
class ProductBase(BaseModel):
    name: str = Field( min_length=2, max_length=100)
    description: Optional[str] = None
    price: float = Field( gt=0)
    category_id: int

class ProductCreate(ProductBase):
    pass


class ProductResponse(ProductBase):
    id: int
    category: Optional[CategoryResponse]

    class Config:
        from_attributes = True

# Order Schemas
class OrderBase(BaseModel):
    product_id: int
    quantity: int = Field(gt=0)
    total: float = Field(gt=0)

class OrderCreate(OrderBase):
    email: str

class OrderResponse(OrderBase):
    id: int
    email: str

    class Config:
        from_attributes = True


#User Schemas

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str = Field(min_length=8)
    role : str = Field(enum=["user", "admin"])


class UserResponse(UserBase):
    id: int
    role: str
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str


