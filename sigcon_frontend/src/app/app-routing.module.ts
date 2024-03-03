import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { AppComponent } from './app.component';
import { RecaudacionComponent } from './components/recaudacion/recaudacion.component';
import { SeguimientoComponent } from './components/seguimiento/seguimiento.component';
import { CotizacionComponent } from './components/cotizacion/cotizacion.component';
import { MantenimientoRecibosComponent } from './components/mantenimiento-recibos/mantenimiento-recibos.component';
import { PrincipalComponent } from './components/principal/principal.component';
import { MenuPrincipalComponent } from './components/menu-principal/menu-principal.component';
import { SolicitarCotizacionComponent } from './components/solicitar-cotizacion/solicitar-cotizacion.component';
import { LoginComponent } from './components/login/login.component';
import { VerCatalogoComponent } from './components/ver-catalogo/ver-catalogo.component';
import { FormatoSolicitudComponent } from './components/formato-solicitud/formato-solicitud.component';
import { RegistrarUsuarioComponent } from './components/registrar-usuario/registrar-usuario.component';
import { VerCotizacionComponent } from './components/ver-cotizacion/ver-cotizacion.component';
import { Login2Component } from './components/Firmar/auth/login/login.component';
import { DashboardComponent } from './components/Firmar/pages/dashboard/dashboard.component';
import { HeaderComponent } from './components/Firmar/shared/header/header.component';
import { ContratosComponent } from './components/Firmar/contratos/contratos.component'

const routes: Routes = [
  {
    path:'RegistrarRecaudacion', component:RecaudacionComponent,
  },
  {
    path: 'SeguimientoCotizacion', component:SeguimientoComponent,
  },
  {
    path: 'SeguimientoCotizacion/cotizacion/:id_solicitud', component:CotizacionComponent,
  },
  {
    path: 'SeguimientoCotizacion/ver-cotizacion/:id_sol_cotizacion', component: VerCotizacionComponent,
  },
  {
    path:'inicio',component:HeaderComponent
  },
  {
    path:'iniciar-sesion',component:Login2Component
  },
  {
    path: 'contratos/:tipo/:id', component: ContratosComponent, 
  },
  {
    path: 'EmitirRecibos', component:MantenimientoRecibosComponent,
  },
  { path: '', redirectTo: '/principal', pathMatch: 'full' }, //Indicamos que ni bien se ejecuta,se tenga la pagina1 de entrada
  { path: 'principal', component: PrincipalComponent },
  { path: 'login', component: LoginComponent },
  { path: 'menu-principal', component: MenuPrincipalComponent },
  { path: 'solicitar-cotizacion', component: SolicitarCotizacionComponent },
  { path: 'ver-catalogo', component: VerCatalogoComponent },
  { path: 'formato-solicitud', component: FormatoSolicitudComponent},
  { path: 'registro', component: RegistrarUsuarioComponent}
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
