import os
from flask_jwt_extended import JWTManager
from flask import Flask
from flask_restful import Api
from dotenv import load_dotenv
from security import authenticate, identity
from resources.user import UserRegister, User, UserLogin
from resources.item import Item, ItemList
from resources.store import Store, StoreList
from db import db

# pylint: disable=invalid-name

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['JWT_SECRET_KEY'] = os.getenv('SECRET_KEY')
app.secret_key = os.getenv('SECRET_KEY')
db.init_app(app)
api = Api(app)


@app.before_first_request
def create_tables():
    db.create_all()


jwt = JWTManager(app) # not creating the auth end point

api.add_resource(Item, '/item/<string:name>')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')
api.add_resource(StoreList, '/stores')
api.add_resource(User, '/user/<int:user_id>')
api.add_resource(UserLogin, '/login')

app.run(port=5000)
