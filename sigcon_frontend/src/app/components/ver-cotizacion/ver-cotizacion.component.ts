import { Component, Input,OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { ConexionService } from 'src/app/services/conexion.service';
import { Location } from '@angular/common';
import Swal from 'sweetalert2';
import { param } from 'jquery';

@Component({
  selector: 'app-ver-cotizacion',
  templateUrl: './ver-cotizacion.component.html',
  styleUrls: ['./ver-cotizacion.component.css']
})
export class VerCotizacionComponent implements OnInit {
  
  id_sol_cotizacion:any
  Data: any;
  importe_administrador: any;
  importe_personallimp: any;
  importe_jardineros: any;
  importe_vigilantes: any;
  importe_total: any;
  TipoPredio = {
    nombre: ''
  };
  Predio = {
    descripcion: '',
    direccion: '',
    ruc: '',
  };
  Solicitante = {
    nombrecompleto: '',
    correo: ''
  };
  Persona = {
    nrodoc: ''
  };
  Rol = {
    descripcion: ''
  };
  Servicio = {
    descripcion: '',
    precio: 0
  };
  Solicitud = {
    id_solicitud: 0,
    id_predio: 0,
    id_solicitante: 0,
    id_servicio: 0,
    area_predio: 0,
    num_casas: 0,
    cant_acomunes: 0,
    area_acomunes: 0,
    cant_vigilantes: 0,
    cant_plimpieza: 0,
    cant_administracion: 0,
    cant_jardineria: 0,
    fecha_solicitud: ''
  };
  solicitudes: any;
  cotizaciones: any;
  page: number = 1;
  count: number = 0;
  tablesize: number = 10;
  tablesizes: any = [5, 10, 15, 20];
 


  constructor(private route: ActivatedRoute, private conexion: ConexionService, private location: Location) {}

  ngOnInit(){
    this.route.params.subscribe(params =>{
      this.id_sol_cotizacion = params['id_sol_cotizacion']
      console.log(this.id_sol_cotizacion)
      this.mostrarDatos(this.id_sol_cotizacion);
    })
  }

  goBack() {
    // Retroceder una página
    this.location.back();
}

  mostrarDatos(id:any){
    this.conexion.getCotizacion(id).subscribe((res: any) => {
      //RECIBE
      this.Data = res['data'];
      this.Solicitud.id_solicitud = this.Data.id_solicitud;
      console.log(this.Solicitud.id_solicitud);
      //this.verificarcoti(this.Solicitud.id_solicitud);
      //SOLICITANTE
      this.Solicitante.nombrecompleto = this.Data.solicitud.solicitante.persona.nombre_completo;
      this.Rol.descripcion = this.Data.solicitud.solicitante.rol.descripcion;
      this.Solicitante.correo = this.Data.solicitud.solicitante.correo;
      //INFO PREDIO
      this.Predio.descripcion = this.Data.solicitud.predio.descripcion;
      this.Predio.direccion = this.Data.solicitud.predio.direccion;
      this.TipoPredio.nombre = this.Data.solicitud.predio.tipo_predio.nomre_predio;
      this.Predio.ruc = this.Data.solicitud.predio.ruc;
      //SERVICIO
      this.Solicitud.cant_administracion = this.Data.solicitud.cant_administracion;
      this.Solicitud.cant_plimpieza = this.Data.solicitud.cant_plimpieza;
      this.Solicitud.cant_jardineria = this.Data.solicitud.cant_jardineria;
      this.Solicitud.cant_vigilantes = this.Data.solicitud.cant_vigilantes;
      this.Servicio.descripcion = this.Data.solicitud.servicio.descripcion;

      //CALCULO COTIZACION

      this.importe_administrador = this.Data.solicitud.cant_administracion * 500;
      this.importe_personallimp = this.Data.solicitud.cant_plimpieza * 300;
      this.importe_jardineros = this.Data.solicitud.cant_jardineria * 300;
      this.importe_vigilantes = this.Data.solicitud.cant_vigilantes * 400;
      this.importe_total = this.importe_administrador + this.importe_personallimp + this.importe_jardineros + this.importe_vigilantes;
    });

  }


}
