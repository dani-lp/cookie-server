from flask import jsonify, request
from flask.views import MethodView
from marshmallow import fields, Schema, ValidationError
from src.models.unit import Unit


class UnitSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)


unit_schema = UnitSchema()


class UnitsAPI(MethodView):
    def get(self):
        units = Unit.all()
        return jsonify([unit.json() for unit in units])

    def post(self):
        json_data = request.get_json()
        if not json_data:
            return {"error": "no input data provided"}, 400

        try:
            data = unit_schema.load(json_data)
        except ValidationError as err:
            return err.messages, 400

        unit = Unit(name=data.get("name"))
        unit.save()
        
        print(unit.json())
        
        return unit.json(), 201