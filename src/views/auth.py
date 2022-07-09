from flask import abort, make_response, request
from flask.views import MethodView
from marshmallow import fields, Schema, ValidationError
from src.config import app_secret
from src.models.user import User
import bcrypt
import jwt


# TODO allow login with either email or username
class LoginSchema(Schema):
    email = fields.Str(required=True)
    password = fields.Str(required=True)


class RegisterSchema(Schema):
    username = fields.Str(required=True)
    email = fields.Str(required=True)
    password = fields.Str(required=True)


login_schema = LoginSchema()
register_schema = RegisterSchema()


def valid_login(password_hash: str, password: str):
    try:
        return bcrypt.checkpw(password.encode('utf8'), password_hash.encode('utf8'))
    except ValueError as err:
        response = make_response(str(err), 401)
        abort(response)


class LoginAPI(MethodView):
    def post(self):
        json_data = request.get_json()
        if not json_data:
            return {"error": "no input data provided"}, 400

        try:
            data = login_schema.load(json_data)
        except ValidationError as err:
            return err.messages, 400

        user = User.get_by_email(data.get("email"))

        if not user:
            return {"error": "user does not exist"}, 404

        if not valid_login(user.password, data.get("password")):
            return {"error": "invalid credentials"}, 401

        token = jwt.encode({"user_id": str(user.id)}, app_secret, algorithm="HS256")

        response = make_response(user.json(), 200)
        response.set_cookie("jwt_token", token)

        return response


class RegisterAPI(MethodView):
    def post(self):
        json_data = request.get_json()
        if not json_data:
            return {"error": "no input data provided"}, 400

        try:
            data = register_schema.load(json_data)
        except ValidationError as err:
            return err.messages, 400

        user_email = data.get("email")

        if User.email_exists(user_email):
            return {"error": f'user with email "${user_email}" already exists'}, 409

        new_user = User(
            username=data.get("username"),
            password=data.get("password"),
            email=data.get("email"),
        )
        new_user.save()

        token = jwt.encode(
            {"user_id": str(new_user.id)}, app_secret, algorithm="HS256"
        )

        response = make_response(new_user.json(), 201)
        response.set_cookie(
            "jwt_token", token, samesite="None", secure=True, httponly=True
        )

        return response


class LogoutAPI(MethodView):
    def post(self):
        response = make_response({"result": "logged out"}, 202)
        response.delete_cookie("jwt_token", samesite="None", secure=True, httponly=True)
        return response
