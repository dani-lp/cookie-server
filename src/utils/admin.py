from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from src.db import db_session
from src.models.unit import Unit
from src.models.ingredient import Ingredient
from src.models.recipe import Recipe
from src.models.user import User
from src.models.fridge_entry import FridgeEntry
from src.models.recipe_ingredient import RecipeIngredient

def create_admin(app):
    app.config["FLASK_ADMIN_SWATCH"] = "cosmo"
    admin = Admin(app, name='Cookie', template_mode='bootstrap3')
    
    admin.add_view(ModelView(Unit, db_session))
    admin.add_view(ModelView(Ingredient, db_session))
    admin.add_view(ModelView(Recipe, db_session))
    admin.add_view(ModelView(User, db_session))
    admin.add_view(ModelView(FridgeEntry, db_session))
    admin.add_view(ModelView(RecipeIngredient, db_session))
