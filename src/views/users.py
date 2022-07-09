from flask import request
from flask.views import MethodView
from marshmallow import fields, Schema, ValidationError
from src.utils.auth import get_user_from_token
from src.utils.validation import not_none
from src.models.user import User


class UserSchema(Schema):
    username = fields.Str()
    email = fields.Str()
    password = fields.Str()

user_schema = UserSchema()


class UsersSelfAPI(MethodView):
    def get(self):
        user = get_user_from_token(request)

        if not user:
            return {"error": "invalid JWT"}, 401

        return user.json()

    def put(self):
        user = get_user_from_token(request)

        if not user:
            return {'error': 'user does not exist'}, 401

        json_data = request.get_json()
        if not json_data:
            return {"error": "no input data provided"}, 400

        try:
            data = user_schema.load(json_data)
        except ValidationError as err:
            return err.messages, 400        

        user.username = not_none(data.get('username'), user.username)
        user.email = not_none(data.get('email'), user.email)
        
        # user.password = not_none(data.get('password'), user.password) # TODO hashing

        user.save()

        return user.json(), 200

    def delete(self):
        user = get_user_from_token(request)

        if not user:
            return {'error' : 'user does not exist'}, 401

        User.delete_one(user.id)
        return {'result' : 'success'}, 204
