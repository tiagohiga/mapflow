import { Component, inject, signal } from '@angular/core';
import { CommonModule, DatePipe } from '@angular/common'
import { PrimaryButtonComponent } from '../../components/primary-button/primary-button.component';
import { MatListModule } from '@angular/material/list'
import { MatIconModule } from '@angular/material/icon'
import { Order } from '../../models/orders.models';
import {MatTableModule} from '@angular/material/table';
import { MessageResponse } from '../../models/generic-responses.models';
import { MatSnackBar } from '@angular/material/snack-bar';

@Component({
  selector: 'app-pedidos',
  imports: [PrimaryButtonComponent, MatListModule, MatIconModule, MatTableModule, DatePipe, CommonModule],
  templateUrl: './pedidos.component.html',
  styleUrl: './pedidos.component.scss'
})
export class PedidosComponent {
  private snackBar = inject(MatSnackBar);
 showButtonClicked(){
 }

 async ngOnInit(){
    const res = await fetch('http://127.0.0.1:8000/orders/list-all');
    const data = await res.json();
    this.orders.set(data);
 }

 displayedColumns: string[] = ['partner_order_number', 'name', 'status', 'created_date', 'address', 'postal_code', 'complement', 'delivery_route', 'actions', 'items'];
  orders = signal<Order[]>([])

  async generateDeliveryRoute(){
    const res = await fetch('http://127.0.0.1:8000/delivery-routes/delivery-route/create_automatic_route');
    const data = await res.json();
    const message = data as MessageResponse;
    this.snackBar.open(message.message, 'Fechar', {
      duration: 5000
    });
  }

}
