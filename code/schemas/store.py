from ma import ma
from models.store import StoreModel
from models.item import ItemModel
from schemas.item import ItemSchema


class StoreSchema(ma.ModelSchema):
    items = ma.Nested(ItemSchema, many=True)

    class Meta:
        model = StoreModel
        # password field is only for loading data, not for dumping data
        dump_only = ("id", )
        include_fk = True
