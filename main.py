# Day1
# from fastapi import FastAPI
#
# app = FastAPI()
#
# 실습1
# @app.get("/")
# async def root():
#     return {"message": "Hello World"}
#
# 실습2
# @app.get("/users/{user_id}")
# def get_user(user_id: int):
#     return {"user_id": user_id, "status": "active"}
#
# 실습3
# @app.get("/products/")
# def get_products(category: str = "all", page: int = 1):
#     return {"category": category,"page": page}
#
# 실습4
# @app.get("/orders/{order_id}")
# def get_order(order_id: int, show_items: bool = False):
#     if show_items:
#         return {"order_id": order_id, "items": ["item1", "item2"]}
#     return {"order_id": order_id}

# 실습5
# import asyncio
# from fastapi import FastAPI
#
# app = FastAPI()
#
# @app.get("/")
# async def get_async_items():
#     await asyncio.sleep(1)
#     return {"message": "async 연습"}

# 실습6
from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()

class Product(BaseModel):
    name: str
    price: float = Field(..., gt=0, description="Price must be greater than 0")
    description: str = "No description"

@app.post("/products/")
def create_product(product: Product):
    return {"product": product}