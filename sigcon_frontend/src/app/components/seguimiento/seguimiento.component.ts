import { Component, OnChanges, OnDestroy, OnInit, Pipe, SimpleChanges, Output, EventEmitter } from '@angular/core';
import { Subscription } from 'rxjs';
import { ConexionService } from 'src/app/services/conexion.service';
import { ActivatedRoute, Router } from '@angular/router';
import { NgxPaginationModule } from 'ngx-pagination';
import * as pdfMake from 'pdfmake/build/pdfMake';
import * as pdfFont from 'pdfmake/build/vfs_fonts';
(pdfMake as any).vfs = pdfFont.pdfMake.vfs;

import Swal from 'sweetalert2';
@Component({
  selector: 'app-seguimiento',
  templateUrl: './seguimiento.component.html',
  styleUrls: ['./seguimiento.component.css']
})
export class SeguimientoComponent implements OnInit, OnChanges, OnDestroy {

  @Output() id_solicitud: EventEmitter<any> = new EventEmitter<any>();
  @Output() nombre_completo: EventEmitter<any> = new EventEmitter<any>();
  @Output() datosEnviados = new EventEmitter<any>();


  Data: any;
  importe_administrador: any;
  importe_personallimp: any;
  importe_jardineros: any;
  importe_vigilantes: any;
  importe_total: any;
  importe_impuesto: any;
  importe_neto: any;
  fecha:any;
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
    correo: '',
    ndocumento: '',
    telefono: 0
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
  suscription: Subscription;

  constructor(private conexion: ConexionService, private route: Router, private aroute: ActivatedRoute) {
    conexion.getSolicitudes().subscribe((res: any) => {
      this.solicitudes = res['data_pendientes'];
      console.log(this.solicitudes);
    });
    conexion.getCotizaciones().subscribe((res: any) => {
      this.cotizaciones = res['data_completadas'];
      console.log(this.cotizaciones);
    });
    this.suscription = conexion.refresh$.subscribe(() => {
      conexion.getSolicitudes().subscribe((res: any) => {
        this.solicitudes = res['data_pendientes'];
        console.log(this.solicitudes);
      });
      conexion.getCotizaciones().subscribe((res: any) => {
        this.cotizaciones = res['data_completadas'];
        console.log(this.cotizaciones);
      });
    });

  }


  verCotizacion(id_sol_cotizacion:any){
    console.log(id_sol_cotizacion)
    Swal.fire({
      title: '¿Recopilando informacion?',
      icon: 'info',
      showCancelButton: true,
      confirmButtonColor: '#3085d6',
      cancelButtonColor: '#d33',
      confirmButtonText: 'Si',
      cancelButtonText: 'No'
      
    }).then((result) => {
      if (result.isConfirmed) {
            this.route.navigate(['SeguimientoCotizacion/ver-cotizacion',id_sol_cotizacion]);
      }
    })
  }

  ngOnInit(): void {
    this.actualizarTabla();
  }
  ngOnDestroy(): void {
    this.suscription.unsubscribe();
    console.log('Obervable cerrado');
  }
  ngOnChanges(changes: SimpleChanges): void {
    console.log(changes);
  }
  onTableDataChanges(event: any) {
    this.page = event;
    this.actualizarTabla();
  }
  onTableSizeChanges(event: any): void {
    this.tablesize = event.target.value;
    this.page = 1;
    this.actualizarTabla();
  }
  actualizarTabla() {
    this.conexion.getSolicitudes().subscribe((res: any) => {
      this.solicitudes = res['data_pendientes'];
      console.log(this.solicitudes);
    });
    this.conexion.getCotizaciones().subscribe((res: any) => {
      this.cotizaciones = res['data_completadas'];
      console.log(this.cotizaciones);
    });
  }
  formatear_id(id: any): string {
    const numeroStr: string = id.toString();
    const cerosRestantes: number = 6 - numeroStr.length;
    let numeroRelleno: string = "";
    if (cerosRestantes >= 0) {
      numeroRelleno = "0".repeat(cerosRestantes) + numeroStr;
    }
    return numeroRelleno;
  }
  Cotizar(id_sol: any) {
    Swal.fire({

      title: '¿Deseas continuar con la cotización?',
      icon: 'warning',
      showCancelButton: true,
      confirmButtonColor: '#3085d6',
      cancelButtonColor: '#d33',
      confirmButtonText: 'Continuar',
      cancelButtonText: 'Cancelar'

    }).then((result) => {
      if (result.isConfirmed) {
        this.conexion.getCotizar(id_sol).subscribe((res: any) => {
          this.Data = res['data'];
          //this.Solicitante.nombrecompleto = this.Data.solicitante.persona.nombre_completo;
          this.Solicitud.id_solicitud = this.Data.id_solicitud;
          this.Solicitante.nombrecompleto = this.Data.solicitante.persona.nombre_completo;
          // Navegación a la nueva URL
          console.log(this.Solicitud.id_solicitud);
          console.log(this.Solicitante.nombrecompleto);
          this.id_solicitud.emit(this.Solicitud.id_solicitud);
          this.nombre_completo.emit(this.Solicitante.nombrecompleto);
          this.route.navigate(['/SeguimientoCotizacion/cotizacion', this.Solicitud.id_solicitud]);
        });
      }
    });
  }
  pdf(id_sol: any){
    console.log(id_sol);
    this.conexion.getCotizacion(id_sol).subscribe((res: any) => {
      this.Data = res['data'];
      this.Solicitud.id_solicitud = this.Data.id_solicitud;
      //this.verificarcoti(this.Solicitud.id_solicitud);
      //SOLICITANTE
      this.Solicitante.nombrecompleto = this.Data.solicitud.solicitante.persona.nombre_completo;
      this.Solicitante.ndocumento = this.Data.solicitud.solicitante.persona.ndocumento;
      this.Rol.descripcion = this.Data.solicitud.solicitante.rol.descripcion;
      this.Solicitante.correo = this.Data.solicitud.solicitante.correo;
      this.Solicitante.telefono = this.Data.solicitud.solicitante.telefono;
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
      this.fecha = this.Data.fecha_cotizacion;
      this.importe_administrador = this.Data.solicitud.cant_administracion * 500;
      this.importe_personallimp = this.Data.solicitud.cant_plimpieza * 300;
      this.importe_jardineros = this.Data.solicitud.cant_jardineria * 300;
      this.importe_vigilantes = this.Data.solicitud.cant_vigilantes * 400;
      this.importe_total = this.importe_administrador + this.importe_personallimp + this.importe_jardineros + this.importe_vigilantes;
      this.importe_impuesto = this.importe_total*0.18;
      this.importe_neto = this.importe_total - this.importe_impuesto;

      const docDefinition:any = {
        content: [
          {text: 'CONDOSA S.A.', style: 'header'},
          {canvas: [{ type: 'line', x1: 0, y1: 0, x2: 515, y2: 0 ,lineWidth: 5}]}, // Linea horizontal
          {text: 'COTIZACION DE SERVICIOS', style: 'subheader',bold: true, alignment: 'center', fontSize: 30},
          {
            alignment: 'center',
            columns: [
              {
                text: `ID-SOLICITUD: ${this.formatear_id(id_sol)} `
              },
              {
                text: `Fecha: ${this.fecha}`
              }
            ]
          }

          ,
          '\n',
          {text: 'Solicitante \n', italics: true,bold: true, fontSize: 15}
          ,
          '\n',
          `Nombre: ${this.Solicitante.nombrecompleto} - ${this.Rol.descripcion}\n`
          ,
          '\n',
          {
            alignment: 'justify',
            columns: [
              {
                text: `Nro Documento: ${this.Solicitante.ndocumento}\n
                       Predio: ${this.Predio.descripcion}\n
                       Tipo Predio: ${this.TipoPredio.nombre}\n`
              },
              {
                text: `Correo: ${this.Solicitante.correo}\n
                       Telefono: ${this.Solicitante.telefono}\n
                       R.U.C.: ${this.Predio.ruc}\n
                       `
              }
            ]
          },
          '\n',
          {text: 'Servicios \n', italics: true,bold: true, fontSize: 15}
          ,
          '\n',
          `Tipo de Servicio: ${this.Servicio.descripcion}\n`
          ,
          '\n',
          {
            alignment: 'justify',
            columns: [
              {
                text: `Cantidad de administradores: ${this.Solicitud.cant_administracion}\n
                       Cantidad de jardineros: ${this.Solicitud.cant_jardineria}\n`
              },
              {
                text: `Cantidad de per. limpieza: ${this.Solicitud.cant_plimpieza}\n
                       Cantidad de vigilantes: ${this.Solicitud.cant_vigilantes}\n`
              }
            ]
          } 
          ,
          '\n',
          {text: 'Cotización ', italics: true,bold: true , fontSize: 15},
          {
            style: 'tableExample',
            table: {
              headerRows: 1,
              body: [
                [{text: 'DESCRIPCIÓN', style: 'tableHeader',fillColor: '#1268b8'},{text: 'MONTO (S/.)', style: 'tableHeader',fillColor: '#1268b8'}],
                [{text: 'Monto Neto', fillColor: '#eeeeff'}, {text: `${this.importe_neto}`, fillColor: '#eeeeff'}],
                ['IGV (18%)', `${this.importe_impuesto}`],
                [{text: 'Monto Total', fillColor: '#eeeeff'}, {text: `${this.importe_total}`, fillColor: '#eeeeff'}]
              ]
            },
            alignment: 'center'
          },
          '\n\n\n\n\n\n\n\n\n\n\n\n\n\n',
          {
            canvas: [
              { type: 'line', x1: 0, y1: 0, x2: 515, y2: 0, lineWidth: 5, margin: [0, 5, 0, 0] }, // Línea horizontal del pie de página
            ],
            margin: [0, 10, 0, 0]
          },
          {text: '\u00A9 2023 CONDOSA. Todos los derechos reservados.', style: 'footer', margin: [0, 5, 0, 0]}
          
        ],
        styles: {
          header: {
            fontSize: 18,
            bold: true,
            margin: [0, 0, 0, 10]
          },
          subheader: {
            fontSize: 16,
            bold: true,
            margin: [0, 10, 0, 5]
          },
          tableExample: {
            margin: [0, 5, 0, 15]
          },
          tableHeader: {
            bold: true,
            fontSize: 13,
            color: 'black'
          }
        },
        defaultStyle: {
          // alignment: 'justify'
        }
      }
      pdfMake.createPdf(docDefinition).open();
    });
  }
}
