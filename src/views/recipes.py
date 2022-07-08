from flask import abort, jsonify, request, make_response
from flask.views import MethodView
from marshmallow import fields, Schema, ValidationError
from src.models.ingredient import Ingredient
from src.models.recipe_ingredient import RecipeIngredient
from src.models.recipe import Recipe
from src.utils.auth import get_user_from_token
from src.utils.validation import is_valid_uuid


class RecipeIngredientSchema(Schema):
    ingredient = fields.Str(required=True)  # id
    amount = fields.Float(required=True)


class RecipeSchema(Schema):
    id = fields.Str(dump_only=True)
    title = fields.Str(required=True)
    content = fields.Str(required=True)
    cook_minutes = fields.Int(required=True)  # TODO make it nullable
    user = fields.Str(required=True)
    ingredients = fields.List(fields.Nested(RecipeIngredientSchema), required=True)


recipe_schema = RecipeSchema()


def parse_ingredients(ingredient_item, recipe: Recipe):
    ingredient_id = ingredient_item.get("ingredient")
    
    if not is_valid_uuid(ingredient_id):
        response = make_response(
            jsonify({"errors": f"ingredient with id {ingredient_id} does not exist"}), 400
        )
        abort(response)
    
    ingredient = Ingredient.get(ingredient_id)

    if not ingredient:
        response = make_response(
            jsonify({"errors": f"ingredient with id {ingredient} does not exist"}), 400
        )
        abort(response)
    
    # recipe.save()   # save once we are sure there won't be errors
    # print(recipe.id)

    amount = ingredient_item.get("amount")

    recipe_ingredient = RecipeIngredient(
        recipe=recipe.id, ingredient=ingredient.id, amount=amount
    )
    recipe_ingredient.save()

    return recipe_ingredient.json()


class RecipesAPI(MethodView):
    def get(self):
        recipes = Recipe.all()
        return jsonify([recipe.json() for recipe in recipes])

    def post(self):
        json_data = request.get_json()
        if not json_data:
            return {"error": "no input data provided"}, 400

        try:
            data = recipe_schema.load(json_data)
        except ValidationError as err:
            return err.messages, 400

        user = get_user_from_token(request)
        
        if not user:
            return {"error": "unauthorized (JWT error)"}, 401

        recipe = Recipe(
            title=data.get("title"),
            content=data.get("content"),
            cook_minutes=data.get("cook_minutes"),  # TODO make it nullable
            user=user.id,
        )
        recipe.save()

        ingredient_list = [
            parse_ingredients(ingredient, recipe)
            for ingredient in data.get("ingredients")
        ]

        recipe_json = recipe.json()
        recipe_json["ingredients"] = ingredient_list

        return recipe_json