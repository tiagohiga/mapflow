export interface Order{
    id: number;
    status: string;
    total_price: number;
    created_date: Date;
    user: number;
    name: string;
    delivery_route: number;
    partner_order_number: string;
    address: string;
    address_number: string;
    neighborhood: string;
    postal_code: string;
    complement: string;
    phone_number: string;
    items: OrderItem[];
}

export interface OrderItem{
    id: number;
    order: number;
    name: string;
    quantity: number;
    unit_price: number;
}