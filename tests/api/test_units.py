import pytest
import json
from src.models.unit import Unit


@pytest.fixture()
def base_data():
    Unit.query.delete()
    unit1 = Unit(name="grams")
    unit2 = Unit(name="dozen")

    unit1.save()
    unit2.save()

    yield [unit1, unit2]


def test_get_units(client, base_data):
    unit1, unit2 = base_data

    response = client.get("/units")

    assert len(response.json) == len(base_data)
    assert unit1.name in json.dumps(response.json)
