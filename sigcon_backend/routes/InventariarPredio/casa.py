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

casa= Blueprint('casa',__name__)


data_Casa = []

@casa.route('/new/casa', methods=['POST','GET'])
def add_casa():
    id_predio = request.json.get('id_predio')
    id_estado = request.json.get('id_estado')
    id_predio_mdu = request.json.get('id_predio_mdu')
    numero = request.json.get('numero')
    piso = request.json.get('piso')
    area = request.json.get('area')
    participacion = request.json.get('participacion')
    new_contact = Casa( id_predio, id_estado, id_predio_mdu, numero, piso, area, participacion)
    db.session.add(new_contact)
    db.session.commit()

    resultado = casa_schema.dump(new_contact)
    data={
        'message' : 'Nueva casa agregada',
        'status:' : 201,
        'data' : resultado
            }

    return make_response(jsonify(data),201)
    
    
    '''
    # Obtener el último ID de predio registrado
    last_casa = db.session.query(func.max(Casa.id_casa)).scalar()
    # Incrementar el último ID de predio para obtener el siguiente
    new_id_casa = last_casa + 1 if last_casa else 1

    id_predio = int(request.form['id_predio'])
    id_estado = request.form['id_estado']
    id_predio_mdu = id_predio_mdu = db.session.query(func.max(predio_mdu.id_predio_mdu)).scalar()
    numero = request.form['numero']
    piso = request.form['piso']
    area = request.form['area']
    participacion = request.form['participacion']
    new_contact = Casa(new_id_casa, id_predio, id_estado, id_predio_mdu, numero, piso, area, participacion)
    db.session.add(new_contact)
    db.session.commit()

    # Guardar el valor seleccionado en la variable de sesión
    session['selected_id_predio'] = id_predio

    # Verificar si los campos tienen valores
    if id_predio and id_estado and id_predio_mdu and numero and piso and area and participacion:
        # Agregar una nueva fila a la lista de datos
        row = [id_predio, id_estado, id_predio_mdu, numero, piso, area, participacion]
        data_Casa.append(row)

    flash("Casa añadida satisfactoriamente!")
    return redirect(url_for('contacts.index'))
    #return render_template('index.html', data_Casa=data_Casa)'''

@casa.route('/update/casa/<id>', methods = ['POST','GET'])
def update_casa(id):
    #casa
        contact = Casa.query.get(id)
        if not contact:
            data = {
                'message': 'Casa no encontrada',
                'status': 404
            }
            return make_response(jsonify(data), 404) 
  
        id_casa=request.json.get('id_casa')
        id_predio=request.json.get('id_predio')
        id_estado=request.json.get('id_estado')
        id_predio_mdu=request.json.get('id_predio_mdu')
        numero=request.json.get('numero')
        piso=request.json.get('piso')
        area=request.json.get('area')
        participacion=request.json.get('participacion')
        
        contact.id_casa=id_casa
        contact.id_predio=id_predio
        contact.id_estado=id_estado
        contact.id_predio_mdu=id_predio_mdu
        contact.numero=numero
        contact.piso=piso
        contact.area=area
        contact.participacion=participacion
        
        db.session.commit()
        
        result = casa_schema.dump(contact)
        
        data = {
            'message': 'Casa actualizada',
            'status': 200,
            'data': result
        }
        
        return make_response(jsonify(data), 200)
'''
    casa
    contact = Casa.query.get(id)
    if request.method == 'POST':
        contact.id_casa=request.form['id_casa']
        contact.id_predio=request.form['id_predio']
        contact.id_estado=request.form['id_estado']
        contact.id_predio_mdu=request.form['id_predio_mdu']
        contact.numero=request.form['numero']
        contact.piso=request.form['piso']
        contact.area=request.form['area']
        contact.participacion=request.form['participacion']
        db.session.commit()
        return redirect(url_for("contacts.about"))
    flash("Casa actualizada satisfactoriamente!")
    return render_template('InventariarPredio/update.html', contact=contact, contact_type='casa')'''

@casa.route('/delete/casa/<int:id>')
def delete_casa(id):
    #casa
    casa = Casa.query.get(id)

    if not casa:
        data = {
            'message': 'Casa no encontrado',
            'status': 404
        }
        return make_response(jsonify(data), 404)

    db.session.delete(casa)
    db.session.commit()

    data = {
        'message': 'Casa eliminada satisfactoriamente',
        'status': 200
    }

    return make_response(jsonify(data), 200)

    '''casa_delete  = Casa.query.get_or_404(id)
    #casa
    db.session.delete(casa_delete )
    db.session.commit()
    flash("Casa eliminada satisfactoriamente!")
    return redirect(url_for('contacts.about'))'''