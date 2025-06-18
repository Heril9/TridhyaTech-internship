from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, List

app = FastAPI()


class Category(BaseModel):
    id : int
    name : str = Field(min_length= 3, max_length= 50)

class Product(BaseModel):
    id : int
    name : str = Field(min_length= 3, max_length= 50)
    price : float = Field(gt= 0)
    stock : int = Field(ge=0)
    category_id : Optional[int] = None

Products: List[Product] = []


@app.get("/")
async def home():
    return {"Hello": "FASTAPI"}


@app.post("/products")
async def create_product(product: Product):
    Products.append(product)
    return {"message": f"Product {product.name} added successfully"}



@app.get("/products",  response_model=List[Product])
async def get_products():
    return Products

@app.delete("/products/{product_id}")
async def delete_product(product_id: int):
    for product in Products:
        if product.id == product_id:
            Products.remove(product)
            return {"message": f"Product {product_id} deleted successfully"}
        else:
            raise HTTPException(status_code= 404, detail= "Product not found")



