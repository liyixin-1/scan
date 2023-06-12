from marshmallow import post_load,fields
from marshmallow_sqlalchemy import SQLAlchemySchema,auto_field
from app.ipscan.models import IPScan,IPScanResult


class IPScanSchema(SQLAlchemySchema):
  class Meta:
    model = IPScan
    # sqla_session = db.session

  id = auto_field(dump_only=True)
  IPs = auto_field()

  @post_load
  def make_ipscan(self, data, **kwargs):
    return IPScan(**data)


class IPScanResultSchema(SQLAlchemySchema):
  class Meta:
    model = IPScanResult
    # sqla_session = db.session

  result_id = fields.Number(dump_only=True)
  ip=fields.String(required=True)
  mac=fields.String(required=True)
  state = fields.String(required=True)
  task_id = fields.Number(required=True)

  @post_load
  def make_ipscanresult(self, data, **kwargs):
    return IPScanResult(**data)
