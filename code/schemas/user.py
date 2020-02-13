from marshmallow import Schema, fields


class UserSchema(Schema):
    class Meta:
        # password field is only for loading data, not for dumping data
        load_only = ("password", )
    id = fields.Int()
    username = fields.Str(required=True)
    password = fields.Str(required=True)
