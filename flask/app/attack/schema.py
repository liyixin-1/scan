from marshmallow import post_load,fields
from marshmallow_sqlalchemy import SQLAlchemySchema,auto_field
from app.attack.models import Attack,AttackResult

class AttackSchema(SQLAlchemySchema):
    class Meta:
        model = Attack
        #sqla_session = db.session

    id = auto_field(dump_only=True)
    destination = auto_field()
    attacktype=auto_field()
    attacknum= auto_field()

    @post_load
    def make_attack(self, data, **kwargs):
        return Attack(**data)


class AttackResultSchema(SQLAlchemySchema):
  class Meta:
    model = AttackResult
    # sqla_session = db.session

  result_id = fields.Number(dump_only=True)
  destination =fields.String(required=True)
  attacknum= fields.Number(required=True)
  attacktype=fields.String(required=True)
  result=fields.String(required=True)
  task_id = fields.Number(required=True)

  @post_load
  def make_attackresult(self, data, **kwargs):
    return AttackResult(**data)
