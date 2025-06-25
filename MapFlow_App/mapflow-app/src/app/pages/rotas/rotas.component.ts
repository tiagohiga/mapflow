import { Component, signal } from '@angular/core';
import { DatePipe } from '@angular/common'
import { MatListModule } from '@angular/material/list'
import { MatIconModule } from '@angular/material/icon'
import {MatTableModule} from '@angular/material/table';
import { DeliveryRoute } from '../../models/delivery-routes.models';

@Component({
  selector: 'app-rotas',
  imports: [MatListModule, MatIconModule, MatTableModule, DatePipe],
  templateUrl: './rotas.component.html',
  styleUrl: './rotas.component.scss'
})
export class RotasComponent {
   displayedColumns: string[] = ['courier', 'status', 'attendant', 'created_date', 'actions'];

  async ngOnInit(){
    const res = await fetch('http://127.0.0.1:8000/delivery-routes/list-all');
    const data = await res.json();
    this.routes.set(data);
  }  
  
   routes = signal<DeliveryRoute[]>([])

   openRouteURL(delivery: DeliveryRoute){
      window.open(delivery.delivery_route_url)
   }
}
