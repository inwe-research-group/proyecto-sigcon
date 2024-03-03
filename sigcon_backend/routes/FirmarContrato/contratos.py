from flask import Blueprint,render_template, request, redirect, url_for, flash, session, make_response, jsonify

from models.tipo_predio import TipoPredio
from models.ubigeo import Ubigeo
from models.predio import Predio
from models.area_comun import AreaComun
from models.predio_area_comun import PredioAreaComun
from models.servicio import Servicio
from models.solicitud_cotizacion import SolicitudCotizacion
from models.solicitud import Solicitud
from models.rol import Rol
from models.tipo_documento import TipoDocumento
from models.persona import Persona
from models.personal import Personal
from models.solicitante import Solicitante
from models.contrato import Contrato
from datetime import datetime
from schemas.contrato_schema import contrato_schema
from flask_cors import cross_origin

from jinja2 import Environment, FileSystemLoader
import pdfkit
import webbrowser

from utils.clean_cache import borrar_cache
from utils.gen_route import route

import os
from datetime import datetime,timedelta

from routes.FirmarContrato.Google.ObtenerTokens import obtener_token
from routes.FirmarContrato.Google.Carpetas import crear_carpeta
from routes.FirmarContrato.Google.DescargarArchivos import descargar_archivo
from routes.FirmarContrato.Google.SubirArchivo import subir_archivo, reemplazar_archivo

from utils.db import db
ROOT_PATH = os.environ.get('ROOT_PATH')

routes = Blueprint("routes", __name__, url_prefix="/contratos")

@routes.route('/<string:tipo>/<int:id>', methods=['POST', 'GET'])
@cross_origin(origin='http://localhost:4200', headers=['Content-Type', 'Authorization'])
def contratos(tipo, id):
    
    id_solicitud_cotizacion =int(id)
    id_personal = int(id)
    id_solicitante = int(id)
    cotizaciones = []
    
    if tipo == "personal" :
    
        cotizaciones = SolicitudCotizacion.query.filter(
            SolicitudCotizacion.id_personal == id_personal,
            ~SolicitudCotizacion.id_solicitud_cotizacion.in_(
                db.session.query(Contrato.id_solicitud_cotizacion)
            ),
            (SolicitudCotizacion.id_estado == 1) | 
            (SolicitudCotizacion.id_estado == None)
        ).all()
        
    if tipo == "solicitante":
        contratos_pendientes = Contrato.query.filter(
            Contrato.id_solicitante == id_solicitante,
            Contrato.fecha_contrato != None,
            Contrato.fecha_firma_solicitante == None,
            Contrato.fecha_firma_personal == None,
        ).all()
        contratos_registrados = Contrato.query.filter(
            Contrato.id_solicitante == id_solicitante,
            Contrato.fecha_contrato != None,
            Contrato.fecha_firma_solicitante != None,
            Contrato.fecha_firma_personal != None,
            Contrato.fecha_registro != None,
        ).all()
    else:
        contratos_pendientes = Contrato.query.filter(
            Contrato.id_personal == id_personal,
            Contrato.fecha_contrato != None,
            Contrato.fecha_firma_solicitante != None,
            Contrato.fecha_firma_personal == None,
        ).all()
        contratos_registrados = Contrato.query.filter(
            Contrato.id_personal == id_personal,
            Contrato.fecha_contrato != None,
            Contrato.fecha_firma_solicitante != None,
            Contrato.fecha_firma_personal != None,
            Contrato.fecha_registro != None,
        ).all()

    return jsonify({
        'idSolicitudCotizacion': id_solicitud_cotizacion,
        'tipo': tipo,
        'id': id,
        'cotizaciones': [cotizacion.serialize() for cotizacion in cotizaciones],
        'contratos_pendientes': [contrato.serialize() for contrato in contratos_pendientes],
        'contratos_registrados': [contrato.serialize() for contrato in contratos_registrados]
    })
        
        
@routes.route('/crear_contrato/<string:tipo>/<string:id>/<string:id_solicitud_cotizacion>', methods=['POST','GET'])
@cross_origin(origin='http://localhost:4200', headers=['Content-Type', 'Authorization'])
def crear_contrato(tipo,id,id_solicitud_cotizacion):
    cotizacion = SolicitudCotizacion.query.filter(
        SolicitudCotizacion.id_solicitud_cotizacion == id_solicitud_cotizacion
    ).all()
    
    solicitud = Solicitud.query.filter(
        Solicitud.id_solicitud == cotizacion[0].id_solicitud    
    ).all()
    
    id_personal = id
    id_solicitante = solicitud[0].id_solicitante
    
    fecha_actual = datetime.now().date()
    fecha_actual_str = fecha_actual.strftime("%Y-%m-%d")
    
    print("FECHAAAAAAAAAAA: ",fecha_actual)
    
    contrato = Contrato(id_solicitud_cotizacion,
                        id_personal,
                        id_solicitante,
                        fecha_actual_str, 
                        None,
                        None,
                        None,
                        None)
    db.session.add(contrato)
    db.session.commit()
    
    
    resultado = contrato_schema.dump(contrato)
    data = {
        'message': 'Nuevo contrato agregado',
        'status:': 201,
        'data': resultado
    }

    # Devuelve la respuesta JSON
    response = jsonify(data)

    # Realiza la redirección solo si la solicitud es de tipo 'GET'
    if request.method == 'GET':
        contrato_final = Contrato.query.filter(
            Contrato.id_solicitud_cotizacion == id_solicitud_cotizacion,
            Contrato.id_personal == id_personal,
            Contrato.id_solicitante == id_solicitante
        ).all()

        id_contrato = contrato_final[0].id_contrato

        crear_carpeta_contratos(id_contrato, id_solicitud_cotizacion, id_personal, id_solicitante)

    return response

def crear_carpeta_contratos(id_contrato,id_solicitud_cotizacion,id_personal,id_solicitante):
    nombre_carpeta = "contrato-"+str(id_contrato)+"-"+str(id_solicitud_cotizacion)+"-"+str(id_personal)+"-"+str(id_solicitante)    
    nombre_parent = "contratos"
     
    crear_carpeta(nombre_parent,nombre_carpeta)
    
    carpeta_datos_solicitante = ("datos_solicitante_"+nombre_carpeta)
    crear_carpeta(nombre_carpeta,carpeta_datos_solicitante)
    
    carpeta_datos_personal = ("datos_personal_"+nombre_carpeta)
    crear_carpeta(nombre_carpeta,carpeta_datos_personal)
    
    return 


@routes.route('/contrato/<accion>/<tipo>/<id>/<id_contrato>', methods=['POST','GET'])
def mostrar_contrato(accion,tipo,id,id_contrato):
    borrar_cache(["Vacio.png"])
    
    print("---------------------------------------------"+tipo,id,id_contrato)
    
    data = obtener_datos_contrato(id_contrato)
    
    data.update({
        'accion': accion,
        'tipo': tipo,
        'id': id,
        'id_contrato': id_contrato
    })

    
    return render_template('contrato.html', **data)
    
@routes.route('/firmar/<string:tipo>/<string:id>/<string:id_contrato>', methods=['POST','GET'])
def firmar_contrato(tipo,id,id_contrato):
    
    contrato = Contrato.query.get(id_contrato)
    
    fecha_actual = datetime.now().date()

    if tipo == "solicitante":
        contrato.fecha_firma_solicitante = fecha_actual
    else:
        contrato.fecha_firma_personal = fecha_actual  
        contrato.fecha_registro = fecha_actual 
        # generar_pdf (id_contrato,tipo,referencia) 

    db.session.commit()
    
    flash("CONTRADO FIRMADO CORRECTAMENTE!!!")
    
    return redirect(url_for('routes.contratos', tipo = tipo, id = id)) 


def obtener_datos_contrato(id_contrato):
    contrato = Contrato.query.get(id_contrato)
    personal = Personal.query.get(contrato.id_personal)
    solicitante = Solicitante.query.get(contrato.id_solicitante)
    cotizacion = SolicitudCotizacion.query.get(contrato.id_solicitud_cotizacion)
    solicitud = Solicitud.query.get(cotizacion.id_solicitud)
    servicio = Servicio.query.get(solicitud.id_servicio)
    predio = Predio.query.get(solicitud.id_predio)
    ubigeo_predio = Ubigeo.query.get(predio.idubigeo)
    tipo_predio = TipoPredio.query.get(predio.id_tipo_predio)
    
    consulta_area_comun = db.session.query(PredioAreaComun, AreaComun).join(AreaComun, PredioAreaComun.id_area_comun == AreaComun.id_area_comun)
    consulta_area_comun = consulta_area_comun.filter(PredioAreaComun.id_predio == predio.id_predio).all()

    predio_area_comun = []
    area_comun = []
    if len(consulta_area_comun) > 0:
        consulta = consulta_area_comun[0]
        predio_area_comun.append(consulta[0])
        area_comun.append(consulta[1])
        
    persona_personal = Persona.query.get(personal.id_persona)
    rol_personal = Rol.query.get(personal.id_rol)
    tipo_documento_personal = TipoDocumento.query.get(persona_personal.id_tipo_documento)
    
    persona_solicitante = Persona.query.get(solicitante.id_persona)
    rol_solicitante = Rol.query.get(solicitante.id_rol)
    tipo_documento_solicitante = TipoDocumento.query.get(persona_solicitante.id_tipo_documento)
    
    referencia = str(id_contrato)+"-"+str(cotizacion.id_solicitud_cotizacion)+"-"+str(personal.id_personal)+"-"+str(solicitante.id_solicitante)  
    
    firma_solicitante_link, huella_solicitante_link, firma_personal_link, huella_personal_link = cargar_documentos(referencia)
    
    data = {
        'referencia': referencia,
        'contrato': contrato,
        'personal': personal,
        'solicitante': solicitante,
        'cotizacion': cotizacion,
        'solicitud': solicitud,
        'servicio': servicio,
        'predio': predio,
        'ubigeo_predio': ubigeo_predio,
        'tipo_predio': tipo_predio,
        'predio_area_comun': predio_area_comun,
        'area_comun': area_comun,
        'persona_personal': persona_personal,
        'rol_personal': rol_personal,
        'tipo_documento_personal': tipo_documento_personal,
        'persona_solicitante': persona_solicitante,
        'rol_solicitante': rol_solicitante,
        'tipo_documento_solicitante': tipo_documento_solicitante,
        'firma_solicitante_link': firma_solicitante_link,
        'huella_solicitante_link': huella_solicitante_link,
        'firma_personal_link': firma_personal_link,
        'huella_personal_link': huella_personal_link
    }
    
    return data

def generar_pdf (id_contrato,tipo,referencia):
    borrar_cache(["Vacio.png"])
    
    accion = "ver_contrato"
    
    data = obtener_datos_contrato(id_contrato)
    
    data.update({
        'accion': accion,
        'tipo': tipo,
        'id': id,
        'id_contrato': id_contrato
    })
    
    nombre_template = "partials/_contrato_partial.html"
    html = render_template(nombre_template, **data)
    
    
    print(html)
    
    opciones = {
        'enable-local-file-access': '',
        'page-size': 'A4',
        'margin-top': '10mm',
        'margin-right': '10mm',
        'margin-bottom': '10mm',
        'margin-left': '10mm',
    }
    
    nombre_contrato = "contrato-"+referencia+".pdf"
    ruta_destino = route("Desktop","")
    ruta_destino = ruta_destino + "\\"+nombre_contrato
    ruta_destino = ruta_destino.replace("\\", "/")
    
    ruta_wkhtmltopdf = route("DSW-ProyectoCondosa-main","\\wkhtmltox\\bin\\wkhtmltopdf.exe")
    
    #ruta_wkhtmltopdf = ruta_wkhtmltopdf.replace("\\", "/")
    
    config = pdfkit.configuration(wkhtmltopdf=ruta_wkhtmltopdf)
    
    print(ruta_destino)
    
    pdfkit.from_string(html, ruta_destino, options=opciones, configuration=config) 
    
    #response = make_response(pdf)
    #response.headers["Content-Type"] = "application/pdf"
    
    #response.headers["Content-Disposition"] = "inline; filename={{nombre_contrato}}"
    #return response





@routes.route('/subir/<accion>/<tipo>/<id>/<id_contrato>/<referencia>', methods=['POST','GET'])
def subir_datos(accion,tipo,id,id_contrato,referencia):
    
    print(accion, tipo, id, id_contrato, referencia)
    
    firma = request.files['firma']
    huella = request.files['huella']
    
    tipos = ["image/png","image/jpeg"]
    
    carpeta_solicitante= "datos_solicitante_contrato-"+referencia
    carpeta_personal = "datos_personal_contrato-"+referencia
    
    carpeta_cache = route("DSW-ProyectoCondosa-main","\\static\\img\\cache")

    carpeta_cache = carpeta_cache.replace("\\", "/")
    
    if tipo == "solicitante":
        nombre_firma = ("firma_solicitante_"+referencia+".png")
        nombre_huella = ("huella_solicitante_"+referencia+".png")
        
        firma.save(os.path.join(carpeta_cache, nombre_firma))
        huella.save(os.path.join(carpeta_cache, nombre_huella))
        
        ruta_firma = carpeta_cache+"/"+nombre_firma
        ruta_huella = carpeta_cache+"/"+nombre_huella
    
        if verificar_existencia(nombre_firma,tipos) and verificar_existencia(nombre_huella,tipos):
            reemplazar_archivo(nombre_firma,ruta_firma,tipos)
            reemplazar_archivo(nombre_huella,ruta_huella,tipos)
        else:
            subir_archivo(nombre_firma,ruta_firma,tipos,carpeta_solicitante)
            subir_archivo(nombre_huella,ruta_huella,tipos,carpeta_solicitante)
    else:
        nombre_firma = ("firma_personal_"+referencia+".png")
        nombre_huella = ("huella_personal_"+referencia+".png")
        
        firma.save(os.path.join(carpeta_cache, nombre_firma))
        huella.save(os.path.join(carpeta_cache, nombre_huella))
    
        ruta_firma = carpeta_cache+"/"+nombre_firma
        ruta_huella = carpeta_cache+"/"+nombre_huella
    
        if verificar_existencia(nombre_firma,tipos) and verificar_existencia(nombre_huella,tipos):
            reemplazar_archivo(nombre_firma,ruta_firma,tipos)
            reemplazar_archivo(nombre_huella,ruta_huella,tipos)
        else:
            subir_archivo(nombre_firma,ruta_firma,tipos,carpeta_personal)
            subir_archivo(nombre_huella,ruta_huella,tipos,carpeta_personal)
        
    borrar_cache(["Vacio.png"])
    
    return redirect(url_for('routes.mostrar_contrato',accion=accion, tipo = tipo, id=id, id_contrato = id_contrato))


def verificar_existencia(nom_archivo,tipos):
    token_resultado,nom_resultado =  obtener_token(nom_archivo,tipos)
    
    if token_resultado and nom_resultado:
        return True
    else:
        return False
    
    
def cargar_documentos(referencia):
    tipos = ["image/png","image/jpeg"]
         
    nombre_firma_solicitante = "firma_solicitante_"+referencia+".png"
    nombre_huella_solicitante = "huella_solicitante_"+referencia+".png"
    nombre_firma_personal = "firma_personal_"+referencia+".png"
    nombre_huella_personal = "huella_personal_"+referencia+".png"
    
    rutas = []
    
    carpeta_cache = route("DSW-ProyectoCondosa-main","\\static\\img\\cache")

    carpeta_cache = carpeta_cache.replace("\\", "/")
    
    
    nombres_archivos = [nombre_firma_solicitante, nombre_huella_solicitante, nombre_firma_personal, nombre_huella_personal]

    for archivo in nombres_archivos:
        if verificar_existencia(archivo,tipos):
            print(archivo)
            nombre_final = descargar_archivo([archivo], tipos)
            print("NOMBREEE FINALLLLL- ",nombre_final)
            
            ruta_final = "img/cache/"+nombre_final
            
            print(ruta_final)
            
            rutas.append(ruta_final)
        else:
            rutas.append("img/cache/Vacio.png")
        
    return rutas[0],rutas[1],rutas[2],rutas[3]

        
    
    
    