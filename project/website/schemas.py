from marshmallow import fields, Schema

class UserSchema(Schema):
    id = fields.Int()
    username = fields.String()
    password = fields.String()