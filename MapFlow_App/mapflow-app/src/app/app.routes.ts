import { Routes } from '@angular/router';
import { DashboardComponent } from './pages/dashboard/dashboard.component';
import { PedidosComponent } from './pages/pedidos/pedidos.component';
import { RotasComponent } from './pages/rotas/rotas.component';
import { ConfiguracoesComponent } from './pages/configuracoes/configuracoes.component';

export const routes: Routes = [
    {
        path: '',
        pathMatch: 'full',
        redirectTo: 'dashboard'
    },
    {
        path: 'dashboard',
        component: DashboardComponent,
    },
    {
        path: 'orders',
        component: PedidosComponent,
    },
    {
        path: 'delivery-routes',
        component: RotasComponent,
    },
    {
        path: 'configuracoes',
        component: ConfiguracoesComponent,
    }
];
