from src.config import app_secret
from src.models.user import User
import jwt

def get_user_from_token(request) -> User or None:
    cookie_token: str = request.cookies.get('jwt_token')
    header_token: str = request.headers.get('Authorization')

    if cookie_token:
        token = cookie_token
    elif header_token and header_token.lower().startswith('bearer'):
        token = header_token[7:]
    else:
        return None

    try:
        decoded_user_id = jwt.decode(token, app_secret, algorithms=["HS256"]).get('user_id')
        user = User.get(decoded_user_id)
        return user
    except jwt.InvalidSignatureError as err:
        print(err)
        return None
