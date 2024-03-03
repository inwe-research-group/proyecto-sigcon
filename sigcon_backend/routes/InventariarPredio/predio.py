from flask import Blueprint, render_template, request, redirect, url_for, flash, session, make_response, jsonify
from models.predio import Predio
from models.predio_area_comun import PredioAreaComun
from models.predio_mdu import predio_mdu
from models.casa import Casa
from models.tipo_predio import TipoPredio
from models.area_comun import AreaComun
from models.mdu import mdu
from schemas.predio_area_comun_schema import predioAreaComun_schema, prediosAreaComun_schema
from schemas.predio_mdu_schema import predioMdu_schema, prediosMdu_schema
from schemas.casa_schema import casa_schema, casas_schema
from schemas.predio_schema import predio_schema, predios_schema
from schemas.tipo_predio_schema import tipoPredio_schema, tiposPredio_schema
from schemas.area_comun_schema import areaComun_schema, areasComunes_schema
from schemas.mdu_schema import mdu_schema, mdus_schema
from utils.db import db
from sqlalchemy import func
from sqlalchemy import func, text, create_engine


predio_ip = Blueprint('predio',__name__)

@predio_ip.route('/contacts')#Cambio de endpoints
def index():
    contacts_predio = Predio.query.all()
    contacts_predio_area_comun = PredioAreaComun.query.all()
    contacts_predio_mdu = predio_mdu.query.all()
    contacts_casa = Casa.query.all()

    # Obtener los valores de id_predio y descripcion de la tabla predio ordenados por id_predio
    id_predios = [{'id_predio': item.id_predio, 'descripcion': item.descripcion} for item in Predio.query.order_by(Predio.id_predio).all()]

    # Obtener el valor seleccionado de id_predio de la variable de sesión
    selected_id_predio = session.get('selected_id_predio')

    return render_template('InventariarPredio/index.html', contacts_predio=contacts_predio, contacts_predio_area_comun=contacts_predio_area_comun,
                           contacts_predio_mdu=contacts_predio_mdu, contacts_casa=contacts_casa, id_predios=id_predios,
                           selected_id_predio=selected_id_predio)

'''   return render_template('InventariarPredio/index.html', contacts_predio=contacts_predio, contacts_predio_area_comun=contacts_predio_area_comun,
                           contacts_predio_mdu=contacts_predio_mdu, contacts_casa=contacts_casa, id_predios=id_predios,
                           selected_id_predio=selected_id_predio, data_Mdu=data_Mdu, data_Casa=data_Casa, data_ArCm=data_ArCm)'''
@predio_ip.route('/update/predio/<id>', methods = ['POST','GET'])
def update_predio(id):
    #predio
        contact = Predio.query.get(id)
        if not contact:
            data = {
                'message': 'Predio no encontrado',
                'status': 404
            }
            return make_response(jsonify(data), 404)
    
    
        id_predio=request.json.get('id_predio')
        id_tipo_predio=request.json.get('id_tipo_predio')
        descripcion=request.json.get('descripcion')
        ruc=request.json.get('ruc')
        telefono=request.json.get('telefono')
        correo=request.json.get('correo')
        direccion=request.json.get('direccion')
        idubigeo=request.json.get('idubigeo')
        
        contact.id_predio=id_predio
        contact.id_tipo_predio=id_tipo_predio
        contact.descripcion=descripcion
        contact.ruc=ruc
        contact.telefono=telefono
        contact.correo=correo
        contact.direccion=direccion
        contact.idubigeo=idubigeo
        db.session.commit()
        
        result = predio_schema.dump(contact)

        data = {
            'message': 'Predio actualizado',
            'status': 200,
            'data': result
        }
    
        return make_response(jsonify(data), 200)
'''
    #predio
    contact = Predio.query.get(id)
    if request.method == 'POST':
        contact.id_predio=request.form['id_predio']
        contact.id_tipo_predio=request.form['id_tipo_predio']
        contact.descripcion=request.form['descripcion']
        contact.ruc=request.form['ruc']
        contact.telefono=request.form['telefono']
        contact.correo=request.form['correo']
        contact.direccion=request.form['direccion']
        contact.idubigeo=request.form['idubigeo']
        db.session.commit()
        return redirect(url_for("contacts.about"))
    contact = Predio.query.get(id)
    flash("Predio actualizado satisfactoriamente!")
    return render_template('InventariarPredio/update.html', contact=contact, contact_type='predio')
'''
@predio_ip.route('/delete/predio/<id>')
def delete_predio(id):
    predio = Predio.query.get(id)

    if not predio:
        data = {
            'message': 'Predio no encontrado',
            'status': 404
        }
        return make_response(jsonify(data), 404)

    db.session.delete(predio)
    db.session.commit()

    data = {
        'message': 'Predio eliminado',
        'status': 200
    }

    return make_response(jsonify(data), 200)
    '''# Eliminar Casas
    casas_delete = Casa.query.filter_by(id_predio=id).all()
    for casa_delete in casas_delete:
        db.session.delete(casa_delete)

    # Eliminar Predio Área Común
    predio_area_comun_delete = PredioAreaComun.query.filter_by(id_predio=id).all()
    for pac_delete in predio_area_comun_delete:
        db.session.delete(pac_delete)

    # Eliminar Predio MDU
    predio_mdu_delete = predio_mdu.query.filter_by(id_predio=id).all()
    for pm_delete in predio_mdu_delete:
        db.session.delete(pm_delete)

    # Eliminar Predio
    predio_delete = Predio.query.get(id)
    db.session.delete(predio_delete)

    db.session.commit()
    flash("Predio y entidades relacionadas eliminadas satisfactoriamente!")
    return redirect(url_for('contacts.about'))'''

