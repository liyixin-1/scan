from marshmallow import post_load
from marshmallow_sqlalchemy import SQLAlchemySchema,auto_field
from app.users.models import User
from app import db

class UserSchema(SQLAlchemySchema):
    class Meta:
        model = User
        #sqla_session = db.session

    id = auto_field(dump_only=True)
    username = auto_field(required=True)
    password=auto_field()
    phonenumber=auto_field()
    email=auto_field()
    role=auto_field()

    @post_load
    def make_user(self, data, **kwargs):
        return User(**data)
