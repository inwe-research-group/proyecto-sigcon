import { Component, OnChanges, OnDestroy, OnInit,Pipe, SimpleChanges } from '@angular/core';
import { NgForm } from '@angular/forms';
import { Subscription } from 'rxjs';
import { ConexionService } from 'src/app/services/conexion.service';
import Swal from 'sweetalert2';
 
@Component({
  selector: 'app-recaudacion',
  templateUrl: './recaudacion.component.html',
  styleUrls: ['./recaudacion.component.css']
})
export class RecaudacionComponent implements OnChanges, OnDestroy{
  
  //Variables que usa Recibo
  numRecibo: any;
  id_mantRecibo: any;
  importe_mantRecibo:any;
  estado: any;

  //Variables que usa Recaudacion
  importeRec:any;
  cuenta_id: any;
  n_operacion: any;
  fecha_operacion: any;
  recaudacion_estado: any;
  observacion: any;
  id_moneda: any;
  desc_moneda: any;
  cuentaPredio: any; 

  recaudaciones: any;
  registro_id_recaudacion:any;
  registro_nro_operacion: any;
  registro_fecha: any;
  registro_importe: any;
  registro_estado: any;
  registro_observacion: any;

  Recaudacion = {
    id_cuenta:0,
    id_mant_recibo: 0,
    n_operacion: 0,
    fecha_operacion: '',
    id_tipo_moneda: 0,
    importe: 0,
    id_recaudacion_estado: 0,
    id_cuenta_predio: 0,
    observacion: ''
  };

  edicionRecaudacion = {
    fecha_operacion: '',
    id_recaudacion_estado: 0,
    observacion:''
  }


  //Otras Variables
  filterPost = '';
  a: any;
  b:any;
  filtro="";


  public page!: number;

  suscription: Subscription;



  constructor(private conexion: ConexionService){
    conexion.getRecaudaciones().subscribe((res:any)=>{
      this.recaudaciones = res['data'];
      this.recaudaciones= this.recaudaciones.sort((a:any,b:any)=>a.fecha_operacion.localeCompare(b.fecha_operacion));
      console.log(this.recaudaciones);
    })
    this.suscription = conexion.refresh$.subscribe(()=>{
      conexion.getRecaudaciones().subscribe((res:any)=>{
        this.recaudaciones = res['data'];
        this.recaudaciones= this.recaudaciones.sort((a:any,b:any)=>a.fecha_operacion.localeCompare(b.fecha_operacion));
        console.log(this.recaudaciones);
      })      
    })
  }
  // ngOnInit(): void {}
  ngOnDestroy(): void {
    this.suscription.unsubscribe();
    console.log('Obervable cerrado');
  }
  ngOnChanges(changes: SimpleChanges): void {
    console.log(changes);
  }
  buscarRecibo(){
    this.conexion.getBuscarRecibo(this.numRecibo).subscribe((res: any) => {
      this.id_mantRecibo = res['id-recibo'];
      this.importe_mantRecibo = res['importe'];
      this.importeRec = this.importe_mantRecibo; //Importe para Recaudacion
      this.estado = res['estado'];
      this.cuenta_id = res['cuenta-id'];
      this.id_moneda = res['id_tipo'];
      this.desc_moneda = res['desc_tipo'];
      this.cuentaPredio = res['cuenta-predio'];
      
    },
    (error: any) => {
      // Manejo de errores
      console.error('Error al obtener el recibo:', error);
      Swal.fire({
        icon: "error",
        title: "Error..",
        text: "Recibo no encontrado!"
      });
      this.limpiarForms();
    });
    Swal.fire({
      icon: "info",
      title: "En Proceso..!",
      showConfirmButton: false,
      timer: 1500
    }).then((result) => {
      if (result.dismiss === Swal.DismissReason.timer) {
        // Este código se ejecuta cuando el temporizador se completa
        Swal.fire({
          icon: "success",
          title: "¡Búsqueda Encontrada!",
          showConfirmButton: true
        });
      }
    });
  }


  RegistrarRecaudacion(){
    this.Recaudacion.id_cuenta = this.cuenta_id;
    this.Recaudacion.id_mant_recibo = this.id_mantRecibo;
    this.Recaudacion.id_cuenta_predio = this.cuentaPredio;
    this.Recaudacion.n_operacion = this.n_operacion;
    this.Recaudacion.fecha_operacion = this.fecha_operacion;
    this.Recaudacion.observacion = this.observacion;
    this.Recaudacion.id_tipo_moneda = this.id_moneda;
    this.Recaudacion.importe = this.importeRec;


    if(this.recaudacion_estado == "Validado"){
      this.Recaudacion.id_recaudacion_estado = 1;
    }else if(this.recaudacion_estado == "Rechazado"){
      this.Recaudacion.id_recaudacion_estado = 2;
    }else if(this.recaudacion_estado == "Anulado"){
      this.Recaudacion.id_recaudacion_estado = 3;
    }else{
      this.Recaudacion.id_recaudacion_estado = 4;
    }

    this.conexion.addRecaudacion(this.Recaudacion).subscribe((res: any) => {
      console.log("Recaudacion añadida correctamente: ",res);
      this.limpiarForms();
    },
    (error: any) => {
      // Manejo de errores
      console.error('Error al obtener el recibo:', error);
      Swal.fire({
        icon: "error",
        title: "Error..",
        text: "Recaudacion No Registrada!!"
      });
    });
    Swal.fire({
      icon: "info",
      title: "En Proceso..!",
      showConfirmButton: false,
      timer: 5200
    }).then((result) => {
      if (result.dismiss === Swal.DismissReason.timer) {
        // Este código se ejecuta cuando el temporizador se completa
        Swal.fire({
          icon: "success",
          title: "¡Registro Completado!",
          showConfirmButton: true
        });
      }
    });

  }

  editarRecaudacion(idRecaudacion: number){
    this.edicionRecaudacion.fecha_operacion = this.registro_fecha;
    if(this.registro_estado == "Validado"){
      this.edicionRecaudacion.id_recaudacion_estado = 1;
    }else if(this.registro_estado == "Rechazado"){
      this.edicionRecaudacion.id_recaudacion_estado = 2;
    }else if(this.registro_estado == "Anulado"){
      this.edicionRecaudacion.id_recaudacion_estado = 3;
    }else{
      this.edicionRecaudacion.id_recaudacion_estado = 4;
    }
    this.edicionRecaudacion.observacion = this.registro_observacion;
    this.conexion.updateRecaudacion(idRecaudacion,this.edicionRecaudacion).subscribe((res: any)=>{
      console.log("Recaudacion ha sido actualizado correctametne: ",res);
    },
    (error: any) => {
      // Manejo de errores
      console.error('Error al obtener el recibo:', error);
      Swal.fire({
        icon: "error",
        title: "Error..",
        text: "Recaudación No Actualizada!!"
      });
    });
    Swal.fire({
      icon: "info",
      title: "En Proceso..!",
      showConfirmButton: false,
      timer: 5200
    }).then((result) => {
      if (result.dismiss === Swal.DismissReason.timer) {
        // Este código se ejecuta cuando el temporizador se completa
        Swal.fire({
          icon: "success",
          title: "¡Actualizacion Completada!",
          showConfirmButton: true
        });
      }
    });
  }
  eliminarRecaudacion(idRecaudacion: any){
    console.log(idRecaudacion);
    Swal.fire({
      title: "Está Seguro de Eliminar?",
      icon: "warning",
      showCancelButton: true,
      confirmButtonColor: "#d33",
      confirmButtonText: "Si, Eliminar!"
    }).then((result) => {
      if (result.isConfirmed) {
        this.conexion.deleteRecaudacion(idRecaudacion).subscribe((res:any) =>{
          console.log("Recaudacion ha sido eliminada correctamente: ",res);
        },
        (error: any) => {
          // Manejo de errores
          console.error('Error al obtener el recibo:', error);
          Swal.fire({
            icon: "error",
            title: "Error..",
            text: "Recaudación No Eliminada!!"
          });
        });
        Swal.fire({
          icon: "info",
          title: "En Proceso..!",
          showConfirmButton: false,
          timer: 5200
        }).then((result) => {
          if (result.dismiss === Swal.DismissReason.timer) {
            // Este código se ejecuta cuando el temporizador se completa
            Swal.fire({
              icon: "success",
              title: "¡Eliminacion Completada!",
              showConfirmButton: true
            });
          }
        });
      }
    });

    
  }
  //Función para el Modal (Editar)
  Registros(recaudacion_:any){

    console.log(recaudacion_);
    this.registro_id_recaudacion=recaudacion_.id_recaudacion;
    this.registro_nro_operacion = recaudacion_.n_operacion;
    this.registro_fecha = recaudacion_.fecha_operacion;
    this.registro_importe= parseFloat(recaudacion_.importe);
    this.registro_estado = recaudacion_.recaudacion_estado.descripcion;
    this.registro_observacion = recaudacion_.observacion;
  }
  //Función de Ordenar
  OrdenarRecibo(){

    this.recaudaciones= this.recaudaciones.sort((a:any,b:any)=>a.mant_recibo.n_recibo.localeCompare(b.mant_recibo.n_recibo));
  }
  OrdenarFecha(){

    this.recaudaciones= this.recaudaciones.sort((a:any,b:any)=>a.fecha_operacion.localeCompare(b.fecha_operacion));
  }

  OrdenarNombre(){
    this.recaudaciones= this.recaudaciones.sort((a:any,b:any)=>a.cuenta.persona.nombre_completo.localeCompare(b.cuenta.persona.nombre_completo));
  }
  OrdenarPredio(){
    this.recaudaciones= this.recaudaciones.sort((a:any,b:any)=>a.mant_recibo.casa.predio.descripcion.localeCompare(b.mant_recibo.casa.predio.descripcion));
  }
  OrdenarMoneda(){
    this.recaudaciones= this.recaudaciones.sort((a:any,b:any)=>a.cuenta.tipo_moneda.descripcion.localeCompare(b.cuenta.tipo_moneda.descripcion));
  }
  OrdenarEstado(){
    this.recaudaciones= this.recaudaciones.sort((a:any,b:any)=>a.recaudacion_estado.descripcion.localeCompare(b.recaudacion_estado.descripcion));
  }

  //Función de limpiar los formularios
  limpiarForms(){
    this.numRecibo = "";
    this.estado = "";
    this.importe_mantRecibo= "";
    this.n_operacion="";
    this.fecha_operacion="";
    this.desc_moneda="";
    this.importeRec="";
    this.recaudacion_estado="";
    this.observacion = "";
  }

}
