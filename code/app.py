import os
from flask_jwt_extended import JWTManager
from flask import Flask, jsonify
from flask_restful import Api
from dotenv import load_dotenv
from security import authenticate, identity
from resources.user import UserRegister, User, UserLogin, TokenRefresh, UserLogout
from resources.item import Item, ItemList
from resources.store import Store, StoreList
from resources.blacklist import BLACKLIST
from db import db

# pylint: disable=invalid-name

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
app.config['JWT_SECRET_KEY'] = os.getenv('SECRET_KEY')
app.secret_key = os.getenv('SECRET_KEY')
db.init_app(app)
api = Api(app)


@app.before_first_request
def create_tables():
    db.create_all()


jwt = JWTManager(app) # not creating the auth end point

@jwt.user_claims_loader
def add_claims_to_jwt(identity):
    # the value should be getting from the config file or db
    # identiy is the user_id
    if identity == 1:
        return {'is_admin': True}
    return {'is_admin': False}

# after the token has expired, this method will be triggered
@jwt.expired_token_loader
def expired_token_callback():
    return {
        'description': 'The token has expired.',
        'error': 'token_expired'
    }, 401

@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({
        'description': 'Signature verification failed',
        'error': 'invalid_token'
    }), 401

@jwt.revoked_token_loader
def reovked_token_callback():
    return jsonify({
        'description': 'The token has been revoked',
        'error': 'token_revoked'
    }), 401

@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    print(decrypted_token)
    return decrypted_token['jti'] in BLACKLIST

api.add_resource(Item, '/item/<string:name>')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')
api.add_resource(StoreList, '/stores')
api.add_resource(User, '/user/<int:user_id>')
api.add_resource(UserLogin, '/login')
api.add_resource(UserLogout, '/logout')
api.add_resource(TokenRefresh, '/refresh')

app.run(port=5000)
