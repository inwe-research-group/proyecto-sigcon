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

predio_mdu_ip = Blueprint('predio_mdu',__name__)


data_Mdu = []

@predio_mdu_ip.route('/new/predio_mdu', methods=['POST', 'GET'])
def add_predio_mdu():

    id_predio = request.json.get('id_predio')
    id_mdu=request.json.get('id_mdu')
    descripcion=request.json.get('descripcion')
    direccion = request.json.get('direccion')
    numero = request.json.get('numero')
    new_contact = predio_mdu(id_predio, id_mdu, descripcion, direccion, numero)
    db.session.add(new_contact)
    db.session.commit()

    resultado = predioMdu_schema.dump(new_contact)
    data={
        'message' : 'Nueva MDU agregado',
        'status:' : 201,
        'data' : resultado
            }

    return make_response(jsonify(data),201)
   
  
''' 
   # Obtener el último ID de predio registrado
    last_mdu = db.session.query(func.max(predio_mdu.id_predio_mdu)).scalar()
    # Incrementar el último ID de predio para obtener el siguiente
    new_id_mdu = last_mdu + 1 if last_mdu else 1

    id_predio = int(request.form['id_predio'])
    id_mdu = request.form['id_mdu']
    descripcion = request.form['descripcion']
    direccion = request.form['direccion']
    numero = request.form['numero']
    new_contact = predio_mdu(new_id_mdu, id_predio, id_mdu, descripcion, direccion, numero)
    db.session.add(new_contact)
    db.session.commit()

    # Guardar el valor seleccionado en la variable de sesión
    session['selected_id_predio'] = id_predio

    # Verificar si los campos tienen valores
    if id_predio and id_mdu and descripcion and direccion and numero:
        # Agregar una nueva fila a la lista de datos
        row = [id_predio, id_mdu, descripcion, direccion, numero]
        data_Mdu.append(row)

    flash("Predio MDU añadido satisfactoriamente!")
    return redirect(url_for('contacts.index'))
    #return render_template('index.html', data_Mdu=data_Mdu)
    '''
    
@predio_mdu_ip.route('/update/predio_mdu/<id>', methods = ['POST','GET'])
def update_predio_mdu(id):
    #predio_mdu
        contact = predio_mdu.query.get(id)
        if not contact:
            data = {
                'message': 'Predio MDU no encontrado',
                'status': 404
            }
            return make_response(jsonify(data), 404)
        
        id_predio_mdu=request.json.get('id_predio_mdu')
        id_predio=request.json.get('id_predio')
        id_mdu=request.json.get('id_mdu')
        descripcion=request.json.get('descripcion')
        direccion=request.json.get('direccion')
        numero=request.json.get('numero')
        
        contact.id_predio_mdu=id_predio_mdu
        contact.id_predio=id_predio
        contact.id_mdu=id_mdu
        contact.descripcion=descripcion
        contact. direccion=direccion
        contact.numero=numero
        db.session.commit()

        result = predioMdu_schema.dump(contact)

        data = {
        'message': 'Predio MDU actualizado',
        'status': 200,
        'data': result
         }

        return make_response(jsonify(data), 200)
'''#predio_mdu
    contact = predio_mdu.query.get(id)
    if request.method == 'POST':
        contact.id_predio_mdu=request.form['id_predio_mdu']
        contact.id_predio=request.form['id_predio']
        contact.id_mdu=request.form['id_mdu']
        contact.descripcion=request.form['descripcion']
        contact. direccion=request.form['direccion']
        contact.numero=request.form['numero']
        db.session.commit()
        return redirect(url_for("contacts.index"))
    contact = predio_mdu.query.get(id)
    flash("Predio MDU actualizado satisfactoriamente!")
    return render_template('InventariarPredio/update.html', contact=contact, contact_type='predio_mdu')'''

@predio_mdu_ip.route('/delete/predio_mdu/<id>')
def delete_predio_mdu(id_predio_mdu, id_predio):
     #predio_mdu
    predio_mdu = predio_mdu.query.filter_by(id_predio_mdu=id_predio_mdu,id_predio=id_predio).first()
    if not predio_mdu:   
        data = {
            'message': 'Predio MDU no encontrado',
            'status': 404
        }
        return make_response(jsonify(data), 404)

    db.session.delete(predio_mdu)
    db.session.commit()

    data = {
        'message': 'Predio MDU eliminado satisfactoriamente',
        'status': 200
    }

    return make_response(jsonify(data), 200)
     
'''
    #predio_mdu
    contact = predio_mdu.query.get(id)
    db.session.delete(contact)
    db.session.commit()
    flash("Predio MDU eliminado satisfactoriamente!")
    return redirect(url_for('contacts.index'))'''