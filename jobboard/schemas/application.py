from marshmallow import fields, validate, Schema

class ApplicationSchema(Schema):
    id = fields.Int(dump_only=True)
    job_id = fields.Int(required=True)
    candidate_id = fields.Int(dump_only=True)
    cover_letter = fields.Str(required=True, validate=validate.Length(min=1))
    status = fields.Str(dump_only=True)
    pdf_url = fields.Str(dump_only=True)
    created_at = fields.DateTime(dump_only=True)