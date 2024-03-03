from utils.ma import ma
from marshmallow import fields
from models.predio_mdu import predio_mdu

class predio_mduSchema(ma.SQLAlchemySchema):
    class Meta:
        model = predio_mdu
        fields = ('id_predio_mdu', 'id_predio', 'id_mdu', 'descripcion', 'direccion', 'numero')

predioMdu_schema = predio_mduSchema()
prediosMdu_schema = predio_mduSchema(many=True)