from flask_restful import Resource, request
from models.user import UserModel
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_refresh_token_required,
    get_jwt_identity,
    get_raw_jwt,
    jwt_required
)
from marshmallow import ValidationError
from schemas.user import UserSchema
from werkzeug.security import safe_str_cmp
from resources.blacklist import BLACKLIST

USER_ALREADY_EXISTS = "A user with that username already exists."
CREATED_SUCCESSFULLY = "User created successfully."
USER_NOT_FOUND = "User not found."
USER_DELETED = "User deleted."
INVALID_CREDENTIALS = "Invalid credentials!"
USER_LOGGED_OUT = "User <id={}> successfully logged out."

user_schema = UserSchema()


class UserRegister(Resource):
    def post(self):
        try:
            user_json = request.get_json()
            user_data = user_schema.load(user_json)
        except ValidationError as err:
            return err.messages, 400

        if UserModel.find_by_username(user_data['username']):
            return {'message': USER_ALREADY_EXISTS}, 400

        user = UserModel(**user_data)
        user.save_to_db()

        return {'message': CREATED_SUCCESSFULLY}, 201


class User(Resource):
    @classmethod
    def get(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': USER_NOT_FOUND}, 404

        return user_schema.dump(user)

    @classmethod
    def delete(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': USER_NOT_FOUND}, 404

        user.delete_from_db()
        return {'message': USER_DELETED}, 200


class UserLogin(Resource):

    @classmethod
    def post(cls):
        # get data from parser
        try:
            user_data = user_schema.load(request.get_json())
        except ValidationError as err:
            return err.messages, 400

        # find user in database
        user = UserModel.find_by_username(user_data['username'])

        # check password
        if user_data and safe_str_cmp(user.password, user_data['password']):
            # create access token
            access_token = create_access_token(identity=user.id, fresh=True)

            # create refresh token
            refresh_token = create_refresh_token(user.id)

            return {
                'access_token': access_token,
                'refresh_token': refresh_token
            }, 200

        # return them
        return {'message': INVALID_CREDENTIALS}, 401


class TokenRefresh(Resource):

    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {'access_token': new_token}, 200


class UserLogout(Resource):

    @jwt_required
    def post(self):
        # jwt id
        jti = get_raw_jwt()['jti']
        user_id = get_jwt_identity()
        BLACKLIST.add(jti)
        print(BLACKLIST)
        return {'message': USER_LOGGED_OUT.format(user_id)}, 200
