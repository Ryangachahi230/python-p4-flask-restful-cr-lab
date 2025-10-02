import pytest
from app import app
from models import db, Plant

# Autouse fixture = runs before every test automatically
@pytest.fixture(autouse=True)
def clean_db():
    with app.app_context():
        db.session.rollback()
        db.drop_all()
        db.create_all()
    yield

def test_can_create_plant():
    with app.app_context():
        p = Plant(name="Douglas Fir")
        db.session.add(p)
        db.session.commit()
        assert p.id is not None

def test_to_dict():
    with app.app_context():
        p = Plant(name="Maple Tree", image="maple.png", price=19.99)
        db.session.add(p)
        db.session.commit()
        data = p.to_dict()
        assert data["name"] == "Maple Tree"
        assert data["price"] == 19.99
