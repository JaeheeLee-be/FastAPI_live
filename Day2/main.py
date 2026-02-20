# 실습1
# from fastapi import FastAPI
# from pydantic import BaseModel, Field
# from typing import List
#
# app = FastAPI()
#
# class Item(BaseModel):
#     name: str
#     quantity: int = Field(..., ge=1, description="quantity는 1이상이어야함")
#
# class Order(BaseModel):
#     id: int
#     items: List[Item]
#     total_price: float = Field(..., ge=0, description="total_price는 0이상")
#
# @app.post("/orders/")
# def create_order(order: Order):
#     return {"order": order}

# 실습2
# from fastapi import FastAPI
# from pydantic import BaseModel, field_validator, Field
# from datetime import datetime, timezone
#
# app = FastAPI()
#
# class Reservation(BaseModel):
#     name: str = Field(..., max_length=50, description="이름 길이 50자 이내 작성")
#     email: str = Field(..., description="이메일 입력하세요")
#     date: datetime
#     special_requests: str = Field(default="", description="옵션 요청 입력")
#
#     # @field_validator("name")
#     # @classmethod
#     # def validate_name_length(cls, value: str):
#     #     if len(value) > 50:
#     #         raise ValueError("이름은 50자를 초과하면 안됩니다")
#     #     return value
#
#     @field_validator("date")
#     @classmethod
#     def validate_date(cls, value: datetime):
#         if value < datetime.now(timezone.utc): # 과거시간
#             raise ValueError("과거 날짜입니다")
#         return value
#
#
# @app.post("/reservations/")
# def create_reservation(reservation: Reservation):
#     return {"reservation": reservation}

# 실습3
# from fastapi import FastAPI
# from pydantic import BaseModel, model_validator, EmailStr
# import re
#
# app = FastAPI()
#
# EMAIL_REGEX = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
#
# class ContactInfo(BaseModel):
#     email: EmailStr | None = None
#     phone_number: str | None = None
#
#     # BEFORE: 입력 데이터 전처리
#     @model_validator(mode="before")
#     @classmethod
#     def preprocess_email(cls, data):
#         if isinstance(data, dict) and data.get("email"):
#             data["email"] = data["email"].lower()
#         return data
#
#     # AFTER: 비즈니스 로직 처리
#     @model_validator(mode="after")
#     def validate_contact_info(self):
#         if not self.email and not self.phone_number:
#             raise ValueError("email과 phone_number 중 하나는 입력되어야합니다")
#
#         if self.email and not re.match(EMAIL_REGEX, self.email):
#             raise ValueError("email 포맷이 아닙니다")
#
#         return self
#
#
# @app.post("/contact")
# def create_contact(contact: ContactInfo):
#     return {
#         "message": "Contact info accepted",
#         "data": contact
#     }

# 실습4
# from fastapi import FastAPI
# from pydantic import BaseModel, computed_field, field_validator
#
# app = FastAPI()
#
#
# class Product(BaseModel):
#     name: str
#     price: float
#     discount: float = 0
#
#     @field_validator("discount")
#     @classmethod
#     def validate_discount(cls, value):
#         if not (0 <= value <= 100):
#             raise ValueError("할인율은 0-100% 사이")
#         return value
#
#     @computed_field
#     @property
#     def final_price(self) -> float:
#         return round(self.price * (1 - self.discount / 100), 1)
#
#
# @app.post("/products")
# def create_product(product: Product):
#     return product

# 실습5
from fastapi import FastAPI
from pydantic import BaseModel, Field
import uuid
from datetime import datetime


app = FastAPI()

class User(BaseModel):
    user_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    role: str = "user"
    created_at: str = Field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"))


@app.post("/users")
def create_user(user: User):
    return user