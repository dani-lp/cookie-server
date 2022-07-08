from flask import request
from flask.views import MethodView
from src.utils.auth import get_user_from_token
from src.utils.validation import not_none
from src.models.user import User


class UsersSelfAPI(MethodView):
    def get(self):
        user = get_user_from_token(request)

        if not user:
            return {"error": "invalid JWT"}, 401

        return user.json()

    # def put(self):
    #     user_id = decode_request_jwt(request)

    #     if not user_id:
    #         return {'error': 'invalid JWT'}, 401

    #     user = User.get(user_id)

    #     if not user:
    #         return {'error': 'user does not exist'}, 404

    #     data = UsersSelf.edit_parser.parse_args()

    #     user.username = not_none(data.get('username'), user.username)
    #     user.name = not_none(data.get('name'), user.name)
    #     user.email = not_none(data.get('email'), user.email)
    #     user.password = not_none(data.get('password'), user.password)
    #     user.birth_date = not_none(data.get('birthDate'), user.birth_date)

    #     user.save()

    #     return user.json(), 200

    # def delete(self):
    #     user_id = decode_request_jwt(request)

    #     if not user_id:
    #         return {'error': 'invalid JWT'}, 401

    #     user = User.get(user_id)

    #     if not user:
    #         return {'error' : 'user does not exist'}, 404

    #     User.delete_one(user_id)
    #     return {'result' : 'success'}, 204
