import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { NgxPaginationModule } from 'ngx-pagination';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { ConexionService } from './services/conexion.service';
import { HttpClientModule } from '@angular/common/http';
import { RecaudacionComponent } from './components/recaudacion/recaudacion.component';
import { CotizacionComponent } from './components/cotizacion/cotizacion.component';
import { SeguimientoComponent } from './components/seguimiento/seguimiento.component';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { FilterPipe } from './pipes/filter.pipe';
import { ReciboComponent } from './components/recibo/recibo.component';
import { RegistrarGastoCasaComponent } from './components/registrar-gasto-casa/registrar-gasto-casa.component';
import { RegistrarGastoPredioComponent } from './components/registrar-gasto-predio/registrar-gasto-predio.component';
import { MantenimientoRecibosComponent } from './components/mantenimiento-recibos/mantenimiento-recibos.component';
import { NgSelectModule } from '@ng-select/ng-select';
import { PrincipalComponent } from './components/principal/principal.component';
import { SolicitarCotizacionComponent } from './components/solicitar-cotizacion/solicitar-cotizacion.component';
import { MenuPrincipalComponent } from './components/menu-principal/menu-principal.component';
import { LoginComponent } from './components/login/login.component';
import { RegistrarUsuarioComponent } from './components/registrar-usuario/registrar-usuario.component';
import { RegistrarPredioComponent } from './components/registrar-predio/registrar-predio.component';
import { VerCatalogoComponent } from './components/ver-catalogo/ver-catalogo.component';
import { FormatoSolicitudComponent } from './components/formato-solicitud/formato-solicitud.component';
import { VerCotizacionComponent } from './components/ver-cotizacion/ver-cotizacion.component';

import { HeaderComponent } from './components/Firmar/shared/header/header.component';
import { FooterComponent } from './components/Firmar/shared/footer/footer.component';
import { DashboardComponent } from './components/Firmar/pages/dashboard/dashboard.component';
import { Login2Component } from './components/Firmar/auth/login/login.component';
import { ContratosComponent } from './components/Firmar/contratos/contratos.component';
import { NavComponent } from './components/Firmar/shared/nav/nav.component';

import { CommonModule } from '@angular/common';


@NgModule({
  declarations: [
    AppComponent,
    RecaudacionComponent,
    CotizacionComponent,
    SeguimientoComponent,
    FilterPipe,
    ReciboComponent,
    RegistrarGastoCasaComponent,
    RegistrarGastoPredioComponent,
    MantenimientoRecibosComponent,
    PrincipalComponent,
    SolicitarCotizacionComponent,
    MenuPrincipalComponent,
    LoginComponent,
    RegistrarUsuarioComponent,
    RegistrarPredioComponent,
    VerCatalogoComponent,
    FormatoSolicitudComponent,
    VerCotizacionComponent,
    AppComponent,
    RecaudacionComponent,
    CotizacionComponent,
    SeguimientoComponent,
    FilterPipe,
    ReciboComponent,
    RegistrarGastoCasaComponent,
    RegistrarGastoPredioComponent,
    MantenimientoRecibosComponent,
    AppComponent,
    HeaderComponent,
    FooterComponent,
    DashboardComponent,
    Login2Component,
    ContratosComponent,
    NavComponent
  ],
  imports: [
    CommonModule,
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,
    NgxPaginationModule,
    FormsModule,
    ReactiveFormsModule,
    NgSelectModule
  ],
  providers: [ConexionService],
  bootstrap: [AppComponent]
})
export class AppModule { }
