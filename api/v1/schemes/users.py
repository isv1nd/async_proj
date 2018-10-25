from marshmallow import schema
from marshmallow import fields
from marshmallow import validate


class UserSchema(schema.Schema):
    id = fields.Int(required=False, dump_only=True)
    name = fields.Str(required=True, validate=[validate.Length(min=1, max=255)])
    birthday = fields.Date(required=True)

    class Meta:
        strict = True
