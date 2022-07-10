from flask import Flask
from flask_cors import CORS
from src.config import app_secret
from src.db import init_db, db_session
from src.utils.admin import create_admin
from src.views.auth import LoginAPI, LogoutAPI, RegisterAPI
from src.views.ingredients import IngredientsAPI
from src.views.recipes import RecipesAPI
from src.views.units import UnitsAPI
from src.views.users import UsersSelfAPI

app = Flask(__name__)
app.secret_key = app_secret
CORS(app, supports_credentials=True)

init_db()
create_admin(app)

app.config['DEBUG'] = True

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

app.add_url_rule('/units', view_func=UnitsAPI.as_view('units'))
app.add_url_rule('/ingredients', view_func=IngredientsAPI.as_view('ingredients'))
app.add_url_rule('/recipes', view_func=RecipesAPI.as_view('recipes'))
app.add_url_rule('/auth/login', view_func=LoginAPI.as_view('login'))
app.add_url_rule('/auth/logout', view_func=LogoutAPI.as_view('logout'))
app.add_url_rule('/auth/register', view_func=RegisterAPI.as_view('register'))
app.add_url_rule('/auth/self', view_func=UsersSelfAPI.as_view('self'))


if __name__ == '__main__':
    app.run()
