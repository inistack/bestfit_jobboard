from marshmallow import Schema, fields, validate

class RegisterSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=validate.Length(min=8))
    role = fields.Str(required=True, validate=validate.OneOf(['employer', 'candidate']))


class LoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True)


class TokenSchema(Schema):
    access_token = fields.Str(required=True)
    refresh_token = fields.Str(required=True)
    

