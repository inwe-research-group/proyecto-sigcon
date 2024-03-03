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

inventario = Blueprint('inventario',__name__)



@inventario.route('/inventario')
def about():
    contacts_predio = Predio.query.all()
    contacts_predio_area_comun = PredioAreaComun.query.all()
    contacts_predio_mdu = predio_mdu.query.all()
    contacts_casa = Casa.query.all()
    tipos_predio = TipoPredio.query.all()
    areas_comunes = AreaComun.query.all()
    contacts_mdu = mdu.query.all()

    contacts_predio_serializado = predios_schema.dump(contacts_predio)
    contacts_predio_area_comun_serializado = prediosAreaComun_schema.dump(contacts_predio_area_comun)
    contacts_predio_mdu_serializado = prediosMdu_schema.dump(contacts_predio_mdu)
    contacts_casa_serializado = casas_schema.dump(contacts_casa)
    tipos_predio_serializado = tiposPredio_schema.dump(tipos_predio)
    areas_comunes_serializado = areasComunes_schema.dump(areas_comunes)
    contacts_mdu_serializado = mdus_schema.dump(contacts_mdu)

    data = {
            'success': True,
            'contact_predio': contacts_predio_serializado,
            'contacts_predio_area_comun': contacts_predio_area_comun_serializado,
            'contacts_predio_mdu': contacts_predio_mdu_serializado,
            'contacts_casa': contacts_casa_serializado,
            'tipos_predio': tipos_predio_serializado,
            'areas_comunes': areas_comunes_serializado,
            'contacts_mdu': contacts_mdu_serializado
    }
    return make_response(jsonify(data), 200) 
    '''contacts_predio = Predio.query.all()
    contacts_predio_area_comun = PredioAreaComun.query.all()
    contacts_predio_mdu = predio_mdu.query.all()
    contacts_casa = Casa.query.all()
    tipos_predio = TipoPredio.query.all()
    areas_comunes = AreaComun.query.all()
    contacts_mdu = mdu.query.all()

    # Obtén el recuento de casas para cada id_predio
    cantidad_casas = {}
    for contact in contacts_casa:
        id_predio = contact.id_predio
        if id_predio in cantidad_casas:
            cantidad_casas[id_predio] += 1
        else:
            cantidad_casas[id_predio] = 1

    return render_template(
        'InventariarPredio/inventario.html',
        areas_comunes=areas_comunes,
        tipos_predio=tipos_predio,
        contacts_predio=contacts_predio,
        contacts_predio_area_comun=contacts_predio_area_comun,
        contacts_predio_mdu=contacts_predio_mdu,
        contacts_casa=contacts_casa,
        cantidad_casas=cantidad_casas,
        contacts_mdu=contacts_mdu
    )'''
@inventario.route('/mostrar_casas/<int:id_predio>', methods=['GET', 'POST'])
def mostrar_casas(id_predio):
    val = None
    if request.method == 'GET':
        val = request.args.get('val')
    casas_predio = Casa.query.filter_by(id_predio=id_predio).all()
    predios_mdu = predio_mdu.query.all()
    mdus = mdu.query.all()
    casas_predio_serializado = casas_schema.dump(casas_predio)
    predios_mdu_serializado = prediosMdu_schema.dump(predios_mdu)
    mdus_serializado = mdus_schema.dump(mdus)
    data = {
            'success': True,
            'casas_predio': casas_predio_serializado,
            'predios_mdu': predios_mdu_serializado,
            'mdus': mdus_serializado,
    }
    return make_response(jsonify(data), 200) 
    '''val = None
    if request.method == 'GET':
        val = request.args.get('val')
    casas_predio = Casa.query.filter_by(id_predio=id_predio).all()
    predios_mdu = predio_mdu.query.all()
    mdus = mdu.query.all()
    return render_template('InventariarPredio/mostrar_casas.html', casas_predio=casas_predio, predios_mdu=predios_mdu, mdus=mdus, val=val)'''

@inventario.route('/contacts/filter_predios', methods=['GET', 'POST'])
def filter_predios():
    tipo_predio = request.form.get('tipo_predio')
    descripcion_predio = request.form.get('descripcion_predio')
    ruc_predio = request.form.get('ruc_predio')

    engine = create_engine('postgresql://modulo4:modulo4@137.184.120.127:5432/sigcon')
    connection = engine.connect()

    # Obtén el recuento de casas para cada id_predio
    contacts_casa = Casa.query.all()
    cantidad_casas = {}
    for contact in contacts_casa:
        id_predio = contact.id_predio
        if id_predio in cantidad_casas:
            cantidad_casas[id_predio] += 1
        else:
            cantidad_casas[id_predio] = 1

    query = '''
    SELECT p.id_predio, tp.nomre_predio,
       (
           SELECT STRING_AGG(DISTINCT ac.descripcion, ', ')
           FROM predio_area_comun pac
           JOIN area_comun ac ON pac.id_area_comun = ac.id_area_comun
           WHERE pac.id_predio = p.id_predio
       ) AS area_comun_descripcion,
       (
           SELECT STRING_AGG(CASE WHEN m.descripcion IS NOT NULL THEN CONCAT(m.descripcion, ': ', pm.descripcion) ELSE pm.descripcion END, ', ')
           FROM predio_mdu pm
           JOIN mdu m ON pm.id_mdu = m.id_mdu
           WHERE pm.id_predio = p.id_predio
       ) AS mdu_descripcion,
       p.descripcion, p.ruc, p.telefono, p.correo, p.direccion, p.idubigeo
    FROM predio p
    JOIN tipo_predio tp ON p.id_tipo_predio = tp.id_tipo_predio
    LEFT JOIN predio_area_comun pac ON p.id_predio = pac.id_predio
    LEFT JOIN area_comun ac ON pac.id_area_comun = ac.id_area_comun
    LEFT JOIN predio_mdu pm ON p.id_predio = pm.id_predio
    LEFT JOIN mdu m ON pm.id_mdu = m.id_mdu
    WHERE (tp.nomre_predio = :tipo_predio OR :tipo_predio IS NULL OR :tipo_predio = '') -- Filtro por tipo_predio
    AND (p.descripcion ILIKE :descripcion_predio OR :descripcion_predio IS NULL OR :descripcion_predio = '')
    AND (p.ruc ILIKE :ruc_predio OR :ruc_predio IS NULL OR :ruc_predio = '')
    GROUP BY p.id_predio, tp.nomre_predio, p.descripcion, p.ruc, p.telefono, p.correo, p.direccion, p.idubigeo
    ORDER BY p.id_predio
    '''

    result = connection.execute(text(query).bindparams(tipo_predio=tipo_predio, descripcion_predio=f'%{descripcion_predio}%', ruc_predio=f'%{ruc_predio}%'))
    contacts = result.fetchall()

    connection.close()
    engine.dispose()

    return render_template('InventariarPredio/inventario.html', contacts=contacts, cantidad_casas=cantidad_casas)
