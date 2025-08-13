python
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
