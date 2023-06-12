from marshmallow import post_load,fields
from marshmallow_sqlalchemy import SQLAlchemySchema,auto_field
from app.blowup.models import BlowUp,BlowUpResult


class BlowUpSchema(SQLAlchemySchema):
  class Meta:
    model = BlowUp
  id = auto_field(dump_only=True)
  url = auto_field()
  dictionary = auto_field()

  @post_load
  def make_blowup(self, data, **kwargs):
    return BlowUp(**data)


class BlowUpResultSchema(SQLAlchemySchema):
  class Meta:
    model = BlowUpResult

  result_id = fields.Number(dump_only=True)
  url = fields.String(required=True)
  subdomain = fields.String(required=True)
  task_id = fields.Number(required=True)

  @post_load
  def make_blowupresult(self, data, **kwargs):
    return BlowUpResult(**data)
