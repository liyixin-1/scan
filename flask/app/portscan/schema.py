from marshmallow import post_load,fields
from marshmallow_sqlalchemy import SQLAlchemySchema,auto_field
from app.portscan.models import PortScan,PortScanResult
from app import db

class PortScanSchema(SQLAlchemySchema):
    class Meta:
        model = PortScan
        #sqla_session = db.session

    id = auto_field(dump_only=True)
    IP = auto_field()
    port = auto_field()
    argument = auto_field()

    @post_load
    def make_portscan(self, data, **kwargs):
        return PortScan(**data)


class PortScanResultSchema(SQLAlchemySchema):
  class Meta:
    model = PortScanResult
    # sqla_session = db.session

  result_id = id = fields.Number(dump_only=True)
  host=fields.String(required=True)
  protocol=fields.String(required=True)
  port=fields.String(required=True)
  name=fields.String(required=True)
  state=fields.String(required=True)
  reason=fields.String(required=True)
  task_id = fields.Number(required=True)

  @post_load
  def make_portscanresult(self, data, **kwargs):
    return PortScanResult(**data)
