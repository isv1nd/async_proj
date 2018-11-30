from marshmallow import schema
from marshmallow import fields
from marshmallow import validate


class AuthenticationSchema(schema.Schema):
    email = fields.Str(
        required=True, validate=[validate.Length(max=255), validate.Email()])
    password = fields.Str(
        required=True, validate=[validate.Length(min=5, max=20)],
        load_only=True
    )

    class Meta:
        strict = True


class TokenResponseScheme(schema.Schema):
    token = fields.Str(required=True, dump_only=True)
