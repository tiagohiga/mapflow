from fastapi import APIRouter, Depends, HTTPException
from dependencies import get_session, validate_token
from sqlalchemy.orm import Session
from schemas import DeliveryRouteSchema, OrderSchema, OrderItemSchema, ResponseOrderSchema
from models import Order, User, OrderItem, DeliveryRoute
from typing import List

#delivery_route_router = APIRouter(prefix="/delivery-routes", tags=["rotas"], dependencies=[Depends(validate_token)])
delivery_route_router = APIRouter(prefix="/delivery-routes", tags=["rotas"])

def get_delivery_url(orders_sorted):
    url = "https://www.google.com/maps/dir/R.+Capitão+Messias,+96+-+Perdizes,+São+Paulo+-+SP,+05004020/"
    for order in orders_sorted:
        url += order.address + "," + order.address_number + " - " + order.neighborhood + "," +  " São Paulo - SP " + ", " + str(order.postal_code).zfill(8) + "/"
    
    ' '.join(url.split())

    return url[:-1].replace(" ", "+")

@delivery_route_router.post("/delivery-route/create_route")
async def create_route(route_schema: DeliveryRouteSchema, session: Session = Depends(get_session)):
    new_route = DeliveryRoute(route_schema.attendant, route_schema.courier)

    session.add(new_route)
    session.commit()

    return {"message": f"Rota gerada com sucesso: {new_route.id}"}

@delivery_route_router.post("/delivery-route/add-order/{order_id}/{route_id}")
async def add_order(order_id: int, route_id: int, session: Session = Depends(get_session)):
    order = session.query(Order).filter(Order.id==order_id).first()
    route = session.query(DeliveryRoute).filter(DeliveryRoute.id==route_id).first()

    if not order:
        raise HTTPException(status_code=404, detail="Pedido não encontrado.")
    if not route:
        raise HTTPException(status_code=404, detail="Rota não encontrada.")
    
    if order.delivery_route is None:
        order.delivery_route = route.id
        session.commit()
        return {
        "message": f"Pedido {order.id} adicionado na Rota {route.id} com sucesso.",
        "order": order,
        "route": route
    }
    else:
        return {
        "message": f"Pedido {order.id} já foi adicionado na Rota {route.id} anteriormente.",
        "order": order,
        "route": route
    }

@delivery_route_router.get("/delivery-route/get-by-id/{route_id}")
async def get_order_by_id(route_id: int, session: Session = Depends(get_session)):
    route = session.query(DeliveryRoute).filter(DeliveryRoute.id==route_id).first()
    return{
        "total_orders": len(route.orders),
        "order": route
    }

@delivery_route_router.get("/delivery-route/get-by-courier/{route_courier}")
async def get_order_by_courier(route_courier: str, session: Session = Depends(get_session)):
    route = session.query(DeliveryRoute).filter(DeliveryRoute.courier==route_courier).first()
    return{
        "total_orders": len(route.orders),
        "order": route
    }

@delivery_route_router.get("/delivery-route/dispatch-order/{route_id}")
async def dispatch_order(route_id: int, session: Session = Depends(get_session)):
    route = session.query(DeliveryRoute).filter(DeliveryRoute.id==route_id).first()

    if not route:
        raise HTTPException(status_code=404, detail="Rota não encontrada.")
    
    temp_list = route.orders
    orders_sorted = []

    while temp_list:
        minimum = temp_list[0].created_date
        item_to_add = temp_list[0]
        for x in temp_list:
            if x.created_date < minimum:
                minimum = x.created_date
                item_to_add = x
        orders_sorted.append(item_to_add)
        temp_list.remove(item_to_add)

    url = get_delivery_url(orders_sorted)

    return{
        "delivery_route_url": url
    }

@delivery_route_router.get("/delivery-route/create_automatic_route")
async def create_automatic_route(session: Session = Depends(get_session)):
    open_orders = session.query(Order).filter(Order.status=="NOVO").order_by(Order.created_date.asc()).limit(5)
    
    if not open_orders:
        return {"message": "Não existem novos pedidos para serem roteados."}
    
    attendant = session.query(User).filter(User.user_type=="ATENDENTE").first()
    courier = session.query(User).filter(User.user_type=="COURIER").first()
    
    new_route = DeliveryRoute(attendant.name, courier.name)
    
    session.add(new_route)

    for order in open_orders:
        order.status = "EM ROTA"
        order.delivery_route = new_route.id

    url = get_delivery_url(open_orders)
    new_route.delivery_route_url = url

    session.commit()

    return {"message": f"Rota gerada com sucesso: {new_route.id}"}

@delivery_route_router.get("/delivery-route/get-by-status/{route_status}")
async def get_by_route_status(route_status: str, session: Session = Depends(get_session)):
    routes = session.query(DeliveryRoute).filter(DeliveryRoute.status==route_status).all()
    return{
        "total_orders": len(routes),
        "order": routes
    }

@delivery_route_router.get("/list-all")
async def get_by_route_status(session: Session = Depends(get_session)):
    routes = session.query(DeliveryRoute).all()
    return routes
