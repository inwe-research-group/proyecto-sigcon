import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, Subject } from 'rxjs';
import { tap } from 'rxjs/operators';

@Injectable({
  providedIn: 'root',
})
export class ConexionService {
  private BASE_URL = 'http://137.184.120.127:5000';
  private _refresh$ = new Subject<void>();

  constructor(private http: HttpClient) {}

  get refresh$() {
    return this._refresh$;
  }
  getBuscarRecibo(n_recibo: any) {
    const url = `${this.BASE_URL}/buscarRecibo/${n_recibo}`;
    return this.http.get(url);
  }
  getRecaudaciones() {
    const url = `${this.BASE_URL}/BuscarRecaudacion`;
    return this.http.get(url);
  }
  addRecaudacion(recaudacion: any) {
    const url = `${this.BASE_URL}/agregar`;
    return this.http.post<any>(url, recaudacion).pipe(
      tap(() => {
        this.refresh$.next();
      })
    );
  }
  updateRecaudacion(id_recaudacion: any, recaudacion: any) {
    const url = `${this.BASE_URL}/editar/${id_recaudacion}`;
    return this.http.put<any>(url, recaudacion).pipe(
      tap(() => {
        this.refresh$.next();
      })
    );
  }
  deleteRecaudacion(id_recaudacion: any) {
    const url = `${this.BASE_URL}/eliminar/${id_recaudacion}`;
    return this.http.delete<any>(url, id_recaudacion).pipe(
      tap(() => {
        this.refresh$.next();
      })
    );
  }

  getPersona() {
    const url = `${this.BASE_URL}/persona`;
    return this.http.get(url);
  }

  addPersona(persona: any) {
    const url = `${this.BASE_URL}/persona`;
    return this.http.post<number>(url, persona);
  }

  getRol() {
    const url = `${this.BASE_URL}/rol`;
    return this.http.get(url);
  }

  addRol(rol: any) {
    const url = `${this.BASE_URL}/rol`;
    return this.http.post<number>(url, rol);
  }

  getSolicitante() {
    const url = `${this.BASE_URL}/solicitante`;
    return this.http.get(url);
  }

  addSolicitante(solicitante: any) {
    const url = `${this.BASE_URL}/solicitante`;
    return this.http.post<number>(url, solicitante);
  }

  getSolicitud() {
    const url = `${this.BASE_URL}/solicitud`;
    return this.http.get(url);
  }

  addSolicitud(solicitud: any) {
    const url = `${this.BASE_URL}/solicitud`;
    return this.http.post<number>(url, solicitud);
  }

  getTipoDocumento() {
    const url = `${this.BASE_URL}tipo_documento`;
    return this.http.get(url);
  }

  addTipoDocumento(tipoDocumento: any) {
    const url = `${this.BASE_URL}/tipo_documento`;
    return this.http.post<number>(url, tipoDocumento);
  }

  getPredio() {
    const url = `${this.BASE_URL}/predio`;
    return this.http.get(url);
  }

  addPredio(predio: any): Observable<any> {
    const url = `${this.BASE_URL}/predio`;
    return this.http.post<number>(url, predio);
  }

  getServicio() {
    const url = `${this.BASE_URL}/servicio`;
    return this.http.get(url);
  }

  addServicio(servicio: any) {
    const url = `${this.BASE_URL}/servicio`;
    return this.http.post<number>(url, servicio);
  }

  getTipoPredio() {
    const url = `${this.BASE_URL}/tipo_predio`;
    return this.http.get(url);
  }

  addTipoPredio(tipoPredio: any) {
    const url = `${this.BASE_URL}/tipo_predio`;
    return this.http.post<number>(url, tipoPredio);
  }

  getUbigeo() {
    const url = `${this.BASE_URL}/ubigeo`;
    return this.http.get(url);
  }

  addUbigeo(ubigeo: any) {
    const url = `${this.BASE_URL}/ubigeo`;
    return this.http.post<number>(url, ubigeo);
  }

  getAreaComun() {
    const url = `${this.BASE_URL}/areaComun`;
    return this.http.get(url);
  }

  addAreaComun(areaComun: any) {
    const url = `${this.BASE_URL}/areaComun`;
    return this.http.post<number>(url, areaComun);
  }

  getPredioAreaComun() {
    const url = `${this.BASE_URL}/predio_area_comun`;
    return this.http.get(url);
  }

  addPredioAreaComun(predioAreaComun: any) {
    const url = `${this.BASE_URL}/predio_area_comun`;
    return this.http.post<number>(url, predioAreaComun);
  }

  getSolicitudes() {
    const url = `${this.BASE_URL}/cotizaciones/cotizacionesp`;
    return this.http.get(url);
  }
  getCotizaciones() {
    const url = `${this.BASE_URL}/cotizaciones/cotizacionesc`;
    return this.http.get(url);
  }
  getCotizar(id_solicitud: any) {
    const url = `${this.BASE_URL}/solicitud/${id_solicitud}`;
    return this.http.get(url);
  }

  getCotizacion(id_solicitud: any) {
    const url = `${this.BASE_URL}/solicitud/cot/${id_solicitud}`;
    return this.http.get(url);
  }

  aceptarCotizacion(idSolicitud: number): Observable<any> {
    const url = `${this.BASE_URL}/cotizaciones/aceptarCotizacion`; // Ajusta la URL según tu backend
    const payload = { id_solicitud: idSolicitud };
    return this.http.post<any>(url, payload);
  }

  getPDF(idsolicitud: any) {
    const url = `${this.BASE_URL}boleta/boleta`;
    const payload = { id_solicitud: idsolicitud };
    return this.http.post<any>(url, payload);
  }

  verCotizar(id_solicitud: any) {
    const url = `${this.BASE_URL}/solicitud/${id_solicitud}`;
    return this.http.get(url);
  }

  getPredios(): Observable<any> {
    return this.http.get(`${this.BASE_URL}/getPredios`);
  }

  getPredioId(id: string): Observable<any> {
    return this.http.get(`${this.BASE_URL}/getPredio/${id}`);
  }

  getGastos(id: string): Observable<any> {
    return this.http.get(`${this.BASE_URL}/getPredios/${id}`);
  }

  getCasas(id: string): Observable<any> {
    return this.http.get(`${this.BASE_URL}/getPredios/${id}/getCasas`);
  }

  getTipoGastos(): Observable<any> {
    return this.http.get(`${this.BASE_URL}/getTipoGastosComunes`);
  }

  getDescripGastos(id: string): Observable<any> {
    return this.http.get(`${this.BASE_URL}/getTipoGastosComunes/${id}`);
  }

  getGastosPredios(id: string): Observable<any> {
    return this.http.get(`${this.BASE_URL}/getGastosPredios/${id}`);
  }

  getGastosPrediosI(id: string, idgasto: string): Observable<any> {
    return this.http.get(`${this.BASE_URL}/getGastosPredios/21/1`);
  }

  postGastosPredios(
    id_pre_ga: string,
    id_ga: string,
    imp: string
  ): Observable<any> {
    const data = {
      id_predio_gastos: id_pre_ga,
      id_gasto: id_ga,
      importe: imp,
    };
    return this.http.post(`${this.BASE_URL}/insertarGastoPredio`, data);
  }

  putGastosPredios(id_pre_ga_det: string, imp: string) {
    const data = {
      id_predio_gastos_det: id_pre_ga_det,
      importe: imp,
    };
    return this.http.put(`${this.BASE_URL}/actualizarGastoPredio`, data);
  }

  getRegistroPredioEstadoI(): Observable<any> {
    return this.http.get(`${this.BASE_URL}/getRegistroPredioEstado`);
  }

  postRegistroPredioEstado(
    id_pred: string,
    id_pers: string,
    id_est: string,
    peri: string
  ): Observable<any> {
    const data = {
      id_predio: id_pred,
      id_personal: id_pers,
      id_estado: id_est,
      periodo: peri,
    };
    return this.http.post(
      `${this.BASE_URL}/insertarRegistroPredioEstado`,
      data
    );
  }

  putRegistroPredioEstado(id_est: string, id_pred: string, peri: string) {
    const data = {
      id_estado: id_est,
      id_predio: id_pred,
      periodo: peri,
    };
    return this.http.put(
      `${this.BASE_URL}/actualizarRegistroPredioEstado`,
      data
    );
  }
}
