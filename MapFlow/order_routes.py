from fastapi import APIRouter, Depends, HTTPException
from dependencies import get_session, validate_token
from sqlalchemy.orm import Session
from schemas import OrderSchema, OrderItemSchema, ResponseOrderSchema
from models import Order, User, OrderItem
from typing import List

#order_router = APIRouter(prefix="/orders", tags=["pedidos"], dependencies=[Depends(validate_token)])
order_router = APIRouter(prefix="/orders", tags=["pedidos"])

@order_router.post("/order/create_order")
async def create_order(order_schema: OrderSchema, session: Session = Depends(get_session)):
    postal_code_parse = ''.join(i for i in order_schema.postal_code if i.isdigit())
    phone_number_parse = ''.join(i for i in order_schema.phone_number if i.isdigit())

    new_order = Order(user=order_schema.id_user, name=order_schema.name, partner_order_number=order_schema.partner_order_number, address=order_schema.address, address_number=order_schema.address_number, 
                      neighborhood=order_schema.neighborhood, postal_code=postal_code_parse, complement=order_schema.complement, 
                      phone_number=phone_number_parse)
    
    session.add(new_order)
    session.commit()
    return {"message": f"Pedido criado com sucesso com o número: {new_order.id}"}

@order_router.post("/order/cancel-order/{order_id}")
async def cancel_order(order_id: int, session: Session = Depends(get_session)):
    order = session.query(Order).filter(Order.id==order_id).first()
    if not order:
        raise HTTPException(status_code=400, detail="Pedido não encontrado.")
    order.status = "CANCELADO"
    session.commit()
    return {
        "message": f"Pedido {order.id} cancelado com sucesso.",
        "order": order
    }

@order_router.get("/list-all", response_model=List[ResponseOrderSchema])
async def get_all(session: Session = Depends(get_session)):
    orders = session.query(Order).all()
    return orders

@order_router.post("/order/add-item/{order_id}")
async def add_order_item(order_id: int, order_item_schema: OrderItemSchema, session: Session = Depends(get_session)):
#async def add_order_item(order_id: int, order_item_schema: OrderItemSchema, session: Session = Depends(get_session), user: User = Depends(validate_token)):
    order = session.query(Order).filter(Order.id==order_id).first()

    if not order:
        raise HTTPException(status_code=404, detail="Pedido não encontrado.")
    order_item = OrderItem(order_item_schema.name, order_item_schema.quantity, order_item_schema.unit_price, order_id)
    session.add(order_item)
    order.update_total_price()
    session.commit()

    return{
        "message": "Item adicionado com sucesso",
        "order_item_id": order_item.id,
        "total_price": order.total_price
    }

@order_router.post("/order/remove-item/{order_item_id}")
async def remove_order_item(order_item_id: int, session: Session = Depends(get_session)):
#async def remove_order_item(order_item_id: int, session: Session = Depends(get_session), user: User = Depends(validate_token)):
    order_item = session.query(OrderItem).filter(OrderItem.id==order_item_id).first()
    order = session.query(Order).filter(Order.id==order_item.pedido).first()

    if not order_item:
        raise HTTPException(status_code=404, detail="Item não encontrado no pedido.")
    
    session.delete(order_item)
    order.update_total_price()
    session.commit()

    return{
        "message": "Item removido com sucesso",
        "order_items_quantity": len(order.items),
        "total_price": order.total_price,
        "order": order
    }

@order_router.post("/order/finish-order/{order_id}")
async def finish_order(order_id: int, session: Session = Depends(get_session)):
    order = session.query(Order).filter(Order.id==order_id).first()
    if not order:
        raise HTTPException(status_code=400, detail="Pedido não encontrado.")
    order.status = "FINALIZADO"
    session.commit()
    return {
        "message": f"Pedido {order.id} cancelado com sucesso.",
        "order": order
    }

@order_router.get("/order/{order_id}")
async def get_order(order_id: int, session: Session = Depends(get_session)):
    order = session.query(Order).filter(Order.id==order_id).first()
    return order
"""     return{
        "total_items": len(order.items),
        "order": order
    } """

@order_router.get("/order/list-by-user/{user_id}", response_model=List[ResponseOrderSchema])
#async def get_all(session: Session = Depends(get_session), user: User = Depends(validate_token)):
async def get_all_by_user(user_id: int, session: Session = Depends(get_session)):
    orders = session.query(Order).filter(Order.user==user_id).all()
    return orders

@order_router.get("/order/list-by-status/{order_status}", response_model=List[ResponseOrderSchema])
#async def get_all(session: Session = Depends(get_session), user: User = Depends(validate_token)):
async def get_by_status(order_status: str, session: Session = Depends(get_session)):
    orders = session.query(Order).filter(Order.status==order_status).all()
    return orders