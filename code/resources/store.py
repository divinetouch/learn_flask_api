from flask_restful import Resource
from models.store import StoreModel

NAME_ALREADY_EXISTS = "A store with name '{}' already exists."
ERROR_INSERTING = "An error occured while creating the store."
STORE_NOT_FOUND = "Store not found."
STORE_DELETED = "Store deleted."


class Store(Resource):
    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()

        return {'message': STORE_NOT_FOUND}, 404

    def post(self, name):
        if StoreModel.find_by_name(name):
            return {'message': ''.format(name)}, 400

        store = StoreModel(name)
        try:
            store.save_to_db()
        except:
            return {'message': ERROR_INSERTING}, 500

        return store.json(), 201

    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()

        return {'message': STORE_DELETED}


class StoreList(Resource):
    def get(self):
        return {'stores': [x.json() for x in StoreModel.find_all()]}
        # return {'stores': list(map(lambda x: x.json(), StoreModel.query.all()))}
