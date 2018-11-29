from marshmallow import schema
from marshmallow import fields
from marshmallow import validate


class UserSchema(schema.Schema):
    id = fields.Int(required=False, dump_only=True)
    email = fields.Str(
        required=True, validate=[validate.Length(max=255), validate.Email()])
    password = fields.Str(
        required=True, validate=[validate.Length(min=6, max=20)],
        load_only=True
    )
    full_name = fields.Str(required=False, validate=[validate.Length(min=1, max=255)])
    is_active = fields.Boolean(dump_only=True)

    class Meta:
        strict = True
