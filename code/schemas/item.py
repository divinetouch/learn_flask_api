from ma import ma
from models.item import ItemModel
from models.store import StoreModel


class ItemSchema(ma.ModelSchema):
    class Meta:
        model = ItemModel
        # password field is only for loading data, not for dumping data
        load_only = ("store", )
        dump_only = ("id", )
        include_fk = True
