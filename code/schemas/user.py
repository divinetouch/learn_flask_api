from ma import ma
from models.user import UserModel


class UserSchema(ma.ModelSchema):
    class Meta:
        model = UserModel

        # password field is only for loading data, not for dumping data
        load_only = ("password", )
        dump_only = ("id", )
