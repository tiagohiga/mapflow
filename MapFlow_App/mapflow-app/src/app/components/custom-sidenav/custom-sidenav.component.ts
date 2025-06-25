import { Component, signal } from '@angular/core'
import { CommonModule } from '@angular/common'
import { MatListModule } from '@angular/material/list'
import { MatIconModule } from '@angular/material/icon'
import { RouterModule } from '@angular/router'

export type MenuItem = {
  icon: string;
  label: string,
  route: string
}

@Component({
  selector: 'app-custom-sidenav',
  imports: [CommonModule, MatListModule, MatIconModule, RouterModule],
  templateUrl: './custom-sidenav.component.html',
  styleUrl: './custom-sidenav.component.scss'
})
export class CustomSidenavComponent {
  menuItems = signal<MenuItem[]>([
    {
      icon: 'dashboard',
      label: 'Dashboard',
      route: 'dashboard'
    },
    {
      icon: 'receipt',
      label: 'Pedidos',
      route: 'orders'
    },
    {
      icon: 'local_shipping',
      label: 'Rotas',
      route: 'delivery-routes'
    },
    {
      icon: 'settings',
      label: 'Configurações',
      route: 'configuracoes'
    }
  ])
}
