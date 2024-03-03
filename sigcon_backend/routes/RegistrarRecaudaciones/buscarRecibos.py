from flask import Blueprint, render_template as request, url_for, redirect,make_response
from flask import flash, request
from models.mant_recibo import MantRecibo
from models.casa import Casa
from models.predio import Predio
from models.persona import Persona
from models.cuenta import Cuenta
from utils.db import db
from models.cuenta_predio import CuentaPredio
from schemas.mant_recibo_schema import mant_recibo_schema,mant_recibos_schema
from schemas.cuenta_schema import cuenta_schema
from schemas.cuenta_predio_schema import cuenta_predio_schema
from flask import jsonify


recibo = Blueprint('recibo', __name__)

##------------BUSCAR POR NUMERO RECIBO---------------
@recibo.route('/buscarRecibo/<string:n_recibo>', methods=['GET'])
def buscar_nroRecibo(n_recibo):


    mantRecibo = MantRecibo.query.filter_by(n_recibo=n_recibo).first()
    if mantRecibo:
        casa = mantRecibo.casa
        predio = casa.predio
        cuenta = Cuenta.query.filter_by(id_persona=predio.id_persona).first()
        cuentaPredio = CuentaPredio.query.filter_by(id_predio=casa.id_predio).first()
        if cuenta:
            response = {
                'success': True,
                'id-recibo': mantRecibo.id_mant_recibo,
                'importe': mantRecibo.importe,
                'estado': mantRecibo.recibo_estado.descripcion,
                'cuenta-id': cuenta.id_cuenta,
                'id_tipo': cuenta.id_tipo_moneda,
                'desc_tipo': cuenta.tipo_moneda.descripcion,
                'cuenta-predio': cuentaPredio.id_cuenta_predio               
            }
        
            return make_response(jsonify(response),200)
    else:
         
            # Si no se encuentra el número de documento, redirigir a la página inicial con un mensaje de error
        data = {
            'message': 'Persona no encontrada',
            'status': 404
        }
        return make_response(jsonify(data), 404)

