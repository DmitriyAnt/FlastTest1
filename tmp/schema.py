from marshmallow import Schema, fields


class AuthorSchema(Schema):
    id = fields.Int()
    name = fields.Str(required=True)
    email = fields.Email()

