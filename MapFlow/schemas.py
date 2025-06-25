from datetime import datetime
from pydantic import BaseModel
from typing import Optional, List

class UserSchema(BaseModel):
    name: str
    email: str
    password: str
    user_type: str
    is_active: Optional[bool]
    admin: Optional[bool]

    class Config:
        from_attributes = True

class OrderSchema(BaseModel):
    id_user: int
    name: str
    partner_order_number: str
    address: str
    address_number: str
    neighborhood: str
    postal_code: str
    complement: str
    phone_number: str

    class Config:
        from_attributes = True

class LoginSchema(BaseModel):
    email: str
    password: str
    
    class Config:
        from_attributes = True

class OrderItemSchema(BaseModel):
    name: str
    quantity: int
    unit_price: float

    class Config:
        from_attributes = True

class ResponseOrderSchema(BaseModel):
    id: int
    status: str
    total_price: float
    name: str
    partner_order_number: str
    address: str
    address_number: str
    neighborhood: str
    postal_code: str
    complement: str
    phone_number: str
    created_date: datetime
    items: List[OrderItemSchema]

    class Config:
        from_attributes = True

class DeliveryRouteSchema(BaseModel):
    attendant: str
    courier: str

    class Config:
        from_attributes = True