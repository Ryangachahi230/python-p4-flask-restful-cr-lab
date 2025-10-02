#!/usr/bin/env python3

from app import app
from models import db, Plant

with app.app_context():
    print("🌱 Seeding plants...")

    # Drop old data
    db.session.query(Plant).delete()

    plants = [
        Plant(
            name="Aloe",
            image="https://upload.wikimedia.org/wikipedia/commons/thumb/3/36/Aloe_vera_flower_02_ies.jpg/320px-Aloe_vera_flower_02_ies.jpg",
            price=11.50,
        ),
        Plant(
            name="ZZ Plant",
            image="https://upload.wikimedia.org/wikipedia/commons/thumb/6/67/Zamioculcas_zamiifolia_002.jpg/320px-Zamioculcas_zamiifolia_002.jpg",
            price=25.98,
        ),
    ]

    db.session.add_all(plants)
    db.session.commit()

    print("✅ Done seeding!")
