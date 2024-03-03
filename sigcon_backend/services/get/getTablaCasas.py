from utils.config import getURI
import psycopg2
from models.casas import Casas

def getTablaCasas(id):
    try:
        url = getURI()
        conn = psycopg2.connect(url)

        casas = []
        inst = "UPDATE casa AS CA SET participacion = ((CA.area + COALESCE((SELECT E.area FROM estacionamiento E WHERE E.id_casa = CA.id_casa), 0)) / COALESCE((SELECT SUM(COALESCE(CA1.area, 0) + COALESCE(E1.area, 0)) FROM casa CA1 LEFT JOIN estacionamiento E1 ON E1.id_casa = CA1.id_casa WHERE CA1.id_predio = %s), 1)) * 100 WHERE CA.id_predio = %s;"
        inst1 = "select row_number() over (order by CA.id_casa) as indice, CA.id_predio, CA.id_casa, PMD.descripcion as MDU, CA.numero, CA.piso, CES.descripcion as estado, CONCAT(PE.apellido_paterno, ' ', PE.nombres) as responsable, CA.area as area_casa,E.area as area_cochera, sum(COALESCE(CA.area, 0) + COALESCE(E.area, 0)) as area_total, CA.participacion from casa CA INNER JOIN predio_mdu PMD ON (PMD.id_predio_mdu = CA.id_predio_mdu) INNER JOIN casa_estado CES ON (CES.id_estado = CA.id_estado) LEFT JOIN estacionamiento E ON (E.id_casa = CA.id_casa) INNER JOIN predio PR ON (PR.id_predio = CA.id_predio) INNER JOIN persona PE ON (PE.id_persona = PR.id_persona) where CA.id_predio = %s Group by CA.id_predio, CA.id_casa, PMD.descripcion,CA.numero,CA.piso,CES.descripcion,PE.apellido_paterno,PE.nombres, CA.area, E.area,CA.participacion;"
        with conn.cursor() as cursor:
            cursor.execute(inst, (id,id))
            cursor.execute(inst1, (id,))
            for row in cursor.fetchall():
                casa = Casas(row[0], row[1], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11])
                casa.id_casa = row[2]
                casas.append(casa.to_json())
        conn.close()
        return casas
    except Exception as error:
        print(error)

