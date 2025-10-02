#!/usr/bin/env python3

from flask import Flask, request
from flask_migrate import Migrate
from flask_restful import Api, Resource
from models import db, Plant

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)


# ---- Helpers ----
def plant_to_dict(plant):
    return {
        "id": plant.id,
        "name": plant.name,
        "image": plant.image,
        "price": float(plant.price) if plant.price is not None else None,
    }


# ---- Resources ----
class Plants(Resource):
    def get(self):
        """GET /plants -> return all plants"""
        plants = Plant.query.all()
        return [plant_to_dict(p) for p in plants], 200

    def post(self):
        """POST /plants -> create a new plant"""
        data = request.get_json() or {}
        name = data.get("name")
        image = data.get("image")
        price = data.get("price")

        if not name:
            return {"error": "Name is required"}, 400
        if price is not None:
            try:
                price = float(price)
            except ValueError:
                return {"error": "Price must be a number"}, 400

        plant = Plant(name=name, image=image, price=price)
        db.session.add(plant)
        db.session.commit()

        return plant_to_dict(plant), 201


class PlantByID(Resource):
    def get(self, id):
        """GET /plants/:id -> return a single plant"""
        plant = db.session.get(Plant, id)
        if not plant:
            return {"error": "Plant not found"}, 404
        return plant_to_dict(plant), 200


# ---- Route registration ----
api.add_resource(Plants, "/plants")
api.add_resource(PlantByID, "/plants/<int:id>")


if __name__ == '__main__':
    app.run(port=5555, debug=True)
