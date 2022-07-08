from flask import jsonify, request
from flask.views import MethodView
from marshmallow import fields, Schema, ValidationError
from src.models.ingredient import Ingredient
from src.models.unit import Unit


class IngredientSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)
    unit = fields.Str(required=True)


ingredient_schema = IngredientSchema()


class IngredientsAPI(MethodView):
    def get(self):
        ingredients = Ingredient.all()
        return jsonify([ingredient.json() for ingredient in ingredients])

    def post(self):
        json_data = request.get_json()
        if not json_data:
            return {"error": "no input data provided"}, 400

        try:
            data = ingredient_schema.load(json_data)
        except ValidationError as err:
            return err.messages, 400

        unit = Unit.get(data.get("unit"))

        ingredient = Ingredient(name=data.get("name"), unit=unit)
        ingredient.save()

        return ingredient.json(), 201
