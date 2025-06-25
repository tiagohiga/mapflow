from sqlalchemy import create_engine, Column, String, Integer, Boolean, Float, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.sql import func
from datetime import datetime
#from sqlalchemy_utils.types import ChoiceType

db = create_engine("sqlite:///mapflow.db")

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    name = Column("name", String)
    email = Column("email", String, nullable=False)
    password = Column("password", String, nullable=False)
    user_type = Column("user_type", String)
    is_active = Column("is_active", Boolean)
    admin = Column("admin", Boolean, default=False)

    def __init__(self, name, email, password, user_type, is_active=True, admin=False):
        self.name = name
        self.email = email
        self.password = password
        self.is_active = is_active
        self.admin = admin
        self.user_type = user_type

class Order(Base):
    __tablename__ = "orders"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    status = Column("status", String)
    partner_order_number = Column("partner_order_number", String)
    user = Column("user", ForeignKey("users.id"))
    total_price = Column("total_price", Float)
    name = Column("name", String)
    address = Column("address", String)
    address_number = Column("address_number", String)
    neighborhood = Column("neighborhood", String)
    postal_code = Column("postal_code", String)
    complement = Column("complement", String)
    phone_number = Column("phone_number", String)
    created_date = Column("created_date", DateTime, default=datetime.now)
    delivery_route = Column("delivery_route", ForeignKey("delivery_routes.id"))
    items = relationship("OrderItem", cascade="all, delete")

    def __init__(self, user, name, partner_order_number, address, address_number, neighborhood, postal_code, complement, phone_number, status="NOVO", total_price=0):
        self.user = user
        self.name = name
        self.partner_order_number = partner_order_number
        self.address = address
        self.address_number = address_number
        self.neighborhood = neighborhood
        self.postal_code = postal_code
        self.complement = complement
        self.phone_number = phone_number
        self.status = status
        self.total_price = total_price

    def update_total_price(self):
        self.total_price = sum(i.unit_price * i.quantity for i in self.items)

class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    name = Column("name", String)
    quantity = Column("quantity", Integer)
    unit_price = Column("unit_price", Float)
    order = Column("order", ForeignKey("orders.id"))

    def __init__(self, name, quantity, unit_price, order):
        self.name = name
        self.quantity = quantity
        self.unit_price = unit_price
        self.order = order

class DeliveryRoute(Base):
    __tablename__ = "delivery_routes"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    status = Column("status", String)
    attendant = Column("attendant", String)
    courier = Column("courier", String)
    created_date = Column("created_date", DateTime, default=datetime.now)
    delivery_route_url = Column("delivery_route_url", String)
    orders = relationship("Order", cascade="all")

    def __init__(self, attendant, courier, status="NOVO"):
        self.attendant = attendant
        self.courier = courier
        self.status = status
    