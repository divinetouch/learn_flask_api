from flask_jwt import JWT
from flask import Flask
from flask_restful import Api
from dotenv import load_dotenv
from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList

import os
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')
api = Api(app)

jwt = JWT(app, authenticate, identity)  # /auth


api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')

app.run(port=5000)
