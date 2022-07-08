import pytest
import jwt

from src.app import app
from src.config import app_secret
from src.models.user import User

# @pytest.fixture(scope='session', autouse=True)
# def load_env():
#     load_dotenv(dotenv_path='../')


@pytest.fixture()
def app_fixture():
    app_obj = app
    yield app_obj


@pytest.fixture()
def client(app_fixture):
    return app_fixture.test_client()


@pytest.fixture()
def runner(app_fixture):
    return app_fixture.text_cli_runner()


@pytest.fixture()
def test_user(client):
    User.query.delete()
    user = User(
        username="testuser",
        email="email@test.com",
        password="1234",
    )
    user.save()

    jwt_token = jwt.encode({"user_id": str(user.id)}, app_secret, algorithm="HS256")

    if type(jwt_token) == bytes:
        jwt_token = jwt_token.decode("utf-8")

    yield [user, jwt_token]
