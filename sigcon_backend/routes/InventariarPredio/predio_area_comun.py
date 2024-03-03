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


predio_area_comun= Blueprint('predio_area_comun',__name__)




data_ArCm = []

@predio_area_comun.route('/new/predio_area_comun', methods=['POST','GET'])
def add_predio_area_comun():
  
    id_predio = request.json.get('id_predio')
    id_area_comun=request.json.get('id_area_comun')
    codigo=request.json.get('codigo')
    area = request.json.get('area')
    # Si no existe, agregar los datos a la base de datos
    new_contact = PredioAreaComun(id_predio, id_area_comun, codigo, area)
    db.session.add(new_contact)
    db.session.commit()
    resultado = predioAreaComun_schema.dump(new_contact)
    data={
        'message' : 'Nueva Area Común agregada',
        'status:' : 201,
        'data' : resultado
            }

    return make_response(jsonify(data),201)
    
    '''
    # Obtener el último ID de predio registrado
    id_predio = int(request.form['id_predio']) if request.form['id_predio'] else None
    id_area_comun = request.form['id_area_comun']
    codigo = request.form['codigo']
    area = request.form['area']

     # Verificar si ya existe una fila con la misma combinación de id_predio e id_area_comun
    existing_area = predio_area_comun.query.filter_by(id_predio=id_predio, id_area_comun=id_area_comun).first()
    if existing_area:
        # Si existe, mostrar un mensaje indicando que ya existe
        flash('Este tipo de área común ya existe', 'error')
    else:
        # Si no existe, agregar los datos a la base de datos
        new_contact = predio_area_comun(id_predio, id_area_comun, codigo, area)
        db.session.add(new_contact)
        db.session.commit()
        
        # Verificar si los campos tienen valores
        if id_predio and id_area_comun and codigo and area:
            # Agregar una nueva fila a la lista de datos
            row = [id_predio, id_area_comun, codigo, area]
            data_ArCm.append(row)
    
        flash("Predio de Area Comun añadido satisfactoriamente!")

    # Guardar el valor seleccionado en la variable de sesión
        session['selected_id_predio'] = id_predio
    return redirect(url_for('contacts.index'))
    #return render_template('index.html', data_ArCm=data_ArCm)
    '''

@predio_area_comun.route('/update/predio_area_comun/<id>', methods = ['POST','GET'])
def update_predio_area_comun(id):
    #predio_area_comun
        contact = PredioAreaComun.query.get(id)
        if not contact:
            data = {
                'message': 'Predio Area Comun no encontrado',
                'status': 404
            }
            return make_response(jsonify(data), 404)
  
        id_predio=request.json.get('id_predio')
        id_area_comun=request.json.get('id_area_comun')
        codigo=request.json.get('codigo')
        area=request.json.get('area')
        
        contact.id_predio=id_predio
        contact.id_area_comun=id_area_comun
        contact.codigo=codigo
        contact.area=area
        db.session.commit()
    
        result = predioAreaComun_schema.dump(contact)

        data = {
            'message': 'Predio Area Comun actualizado',
            'status': 200,
            'data': result
        }

        return make_response(jsonify(data), 200)
'''#predio_area_comun
    contact = PredioAreaComun.query.get(id)
    if request.method == 'POST':
        contact.id_predio=request.form["id_predio"]
        contact.id_area_comun=request.form["id_area_comun"]
        contact.codigo=request.form["codigo"]
        contact.area=request.form["area"]
        db.session.commit()
        return redirect(url_for("contacts.index"))
    contact = PredioAreaComun.query.get(id)
    flash("Predio Area Comun actualizado satisfactoriamente!")
    return render_template('InventariarPredio/update.html', contact=contact, contact_type='predio_area_comun')
'''
@predio_area_comun.route('/delete/predio_area_comun/<id>')
def delete_predio_area_comun(id_predio, id_area_comun):
    #predio_area_comun
    predio_area_comun = PredioAreaComun.query.filter_by(id_predio=id_predio, id_area_comun=id_area_comun).first()

    if not predio_area_comun:
        data = {
            'message': 'Predio-AreaComun no encontrado',
            'status': 404
        }
        return make_response(jsonify(data), 404)

    db.session.delete(predio_area_comun)
    db.session.commit()

    data = {
        'message': 'Predio-AreaComun eliminado',
        'status': 200
    }

    return make_response(jsonify(data), 200)

    '''#predio_area_comun
    contact = PredioAreaComun.query.get(id)
    db.session.delete(contact)
    db.session.commit()
    flash("Predio Area Comun eliminado satisfactoriamente!")
    return redirect(url_for('contacts.index'))'''