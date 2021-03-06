from flask_jwt_extended import jwt_required, jwt_optional, get_jwt_identity, fresh_jwt_required
from flask_restful import Resource
from flask import request
from models.item import ItemModel
from schemas.item import ItemSchema

BLANK_ERROR = "'{}' cannot be left blank!"
NAME_ALREADY_EXISTS = "An item with '{}' already exists."
ITEM_NOT_FOUND = "Item not found."
ERROR_INSERTING = "An error occurred inserting the item."
ITEM_DELETED = 'Item deleted.'

item_schema = ItemSchema()
item_list_schema = ItemSchema(many=True)


class Item(Resource):

    @classmethod
    @jwt_required
    def get(cls, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item_schema.dump(item), 200

        return {'message': ITEM_NOT_FOUND}, 404

    @classmethod
    @jwt_required
    def post(cls, name: str):

        if ItemModel.find_by_name(name):
            # not found
            return {'message': NAME_ALREADY_EXISTS.format(name)}, 400

        item_json = request.get_json()
        item_json['name'] = name
        print(item_json)

        # force=True mean no need to set the header --> get_json(force=True)
        # data = request.get_json()

        item = item_schema.load(item_json)

        try:
            item.save_to_db()
        except:
            # Internal server error
            return {'message': ERROR_INSERTING}, 500

        return item_schema.dump(item), 201

    @classmethod
    @jwt_required
    def delete(cls, name):
        # claims = get_jwt_claims()
        # if not claims['is_admin']:
        #     return {'message': 'Admin privilege required.'}, 401
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()

        return {'message': ITEM_DELETED}

    @classmethod
    @jwt_required
    def put(cls, name):
        item_json = request.get_json()
        item = ItemModel.find_by_name(name)

        if item:
            item.price = item_json['price']
        else:
            item_json['name'] = name
            item = item_schema.load(item_json)

        item.save_to_db()
        return item.json()


class ItemList(Resource):
    # @jwt_optional
    def get(self):
        # user_id = get_jwt_identity()
        items = item_list_schema.dump(ItemModel.find_all())
        return {'items': items}, 200

        # if user_id:
        # return {'items': items}, 200
        # return {
        #     'items': [item['name'] for item in items],
        #     'message': 'More data available if you log in'
        # }, 200
        # return {'items': list(map(lambda x: x.json(), ItemModel.query.all()))}
