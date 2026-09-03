from marshmallow import Schema, fields, validate

class JobSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True, validate=validate.Length(min=1, max=255))
    description = fields.Str(required=True, validate=validate.Length(min=1))
    location = fields.Str(required=True, validate=validate.Length(min=1, max=255))
    tags = fields.Str(allow_none=True)
    employer_id = fields.Int(dump_only=True)
    created_at = fields.DateTime(dump_only=True)


class JobQueryArgsSchema(Schema):
    title = fields.Str(required=False)
    location = fields.Str(required=False)
    tags = fields.Str(required=False)