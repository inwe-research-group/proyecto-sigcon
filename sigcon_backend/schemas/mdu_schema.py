from utils.ma import ma
from marshmallow import fields
from models.mdu import mdu

class mduSchema(ma.SQLAlchemySchema):
    class Meta:
        model = mdu
        fields = ('id_mdu', 'descripcion')

mdu_schema = mduSchema()
mdus_schema = mduSchema(many=True)

#areaComun_schema = mduSchema()
#areasComunes_schema = mduSchema(many=True)