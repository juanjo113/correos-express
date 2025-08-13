from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Vehicle(db.Model):
    __tablename__ = 'vehicles'
    id = db.Column(db.Integer, primary_key=True)
    make = db.Column(db.String(120), nullable=False)
    model = db.Column(db.String(120), nullable=False)
    plate = db.Column(db.String(20), unique=True, nullable=False)
    owner_email = db.Column(db.String(255), nullable=False)
    oil_date = db.Column(db.Date, nullable=True)
    itv_date = db.Column(db.Date, nullable=True)
    oil_notified_on = db.Column(db.Date, nullable=True)
    itv_notified_on = db.Column(db.Date, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<Vehicle {self.plate}>"

def get_all_vehicles(query=None):
    if query:
        vehicles = Vehicle.query.filter(
            (Vehicle.make.ilike(f'%{query}%')) |
            (Vehicle.model.ilike(f'%{query}%')) |
            (Vehicle.plate.ilike(f'%{query}%'))
        ).all()
    else:
        vehicles = Vehicle.query.all()
    return vehicles

def get_vehicles_due_today():
    today = datetime.utcnow().date()
    vehicles_due_today = Vehicle.query.filter(
        (Vehicle.oil_date == today) | (Vehicle.itv_date == today)
    ).all()
    return vehicles_due_today
