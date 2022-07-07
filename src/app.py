from flask import Flask
from src.db import init_db
from src.views.units import UnitsAPI

app = Flask(__name__)
init_db()

app.config['DEBUG'] = True

app.add_url_rule('/units/', view_func=UnitsAPI.as_view('units'))


if __name__ == '__main__':
    app.run()