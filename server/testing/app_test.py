import pytest
import json

from app import app
from models import db, Plant


@pytest.fixture(autouse=True)
def run_around_tests():
    """Reset the DB before each test"""
    with app.app_context():
        db.drop_all()
        db.create_all()
    yield
    with app.app_context():
        db.session.remove()


class TestPlant:
    '''Flask application in app.py'''

    def test_plants_get_route(self):
        '''has a resource available at "/plants".'''
        response = app.test_client().get('/plants')
        assert response.status_code == 200

    def test_plants_get_route_returns_list_of_plant_objects(self):
        '''returns JSON representing Plant objects at "/plants".'''
        with app.app_context():
            p = Plant(name="Douglas Fir")
            db.session.add(p)
            db.session.commit()

        response = app.test_client().get('/plants')
        data = json.loads(response.data.decode())

        assert isinstance(data, list)
        assert len(data) > 0
        assert isinstance(data[0], dict)
        assert "id" in data[0]
        assert "name" in data[0]

    def test_plants_post_route_creates_plant_record_in_db(self):
        '''allows users to create Plant records through the "/plants" POST route.'''
        response = app.test_client().post(
            '/plants',
            json={
                "name": "Live Oak",
                "image": "https://www.nwf.org/-/media/NEW-WEBSITE/Shared-Folder/Wildlife/Plants-and-Fungi/plant_southern-live-oak_600x300.ashx",
                "price": 250.00,
            }
        )
        assert response.status_code == 201

        with app.app_context():
            lo = Plant.query.filter_by(name="Live Oak").first()
            assert lo is not None
            assert lo.id
            assert lo.name == "Live Oak"
            assert lo.image == "https://www.nwf.org/-/media/NEW-WEBSITE/Shared-Folder/Wildlife/Plants-and-Fungi/plant_southern-live-oak_600x300.ashx"
            assert float(lo.price) == 250.00

    def test_plant_by_id_get_route(self):
        '''has a resource available at "/plants/<int:id>".'''
        with app.app_context():
            p = Plant(name="Maple")
            db.session.add(p)
            db.session.commit()

            plant_id = p.id

        response = app.test_client().get(f'/plants/{plant_id}')
        assert response.status_code == 200

    def test_plant_by_id_get_route_returns_one_plant(self):
        '''returns JSON representing one Plant object at "/plants/<int:id>".'''
        with app.app_context():
            p = Plant(name="Birch")
            db.session.add(p)
            db.session.commit()

            plant_id = p.id

        response = app.test_client().get(f'/plants/{plant_id}')
        data = json.loads(response.data.decode())

        assert isinstance(data, dict)
        assert data["id"] == plant_id
        assert data["name"] == "Birch"
