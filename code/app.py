import os
from flask_jwt import JWT
from flask import Flask
from flask_restful import Api
from dotenv import load_dotenv
from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList
from db import db

# pylint: disable=invalid-name

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = os.getenv('SECRET_KEY')
db.init_app(app)
api = Api(app)

_jwt = JWT(app, authenticate, identity)  # /auth


api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')

app.run(host="192.168.1.39", port=5000)
