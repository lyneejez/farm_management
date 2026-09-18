from datetime import date
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Animal(db.Model):
    __tablename__ = "animals"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    species = db.Column(db.String(50), nullable=False)   # e.g. Cow, Goat, Chicken
    breed = db.Column(db.String(80))
    gender = db.Column(db.String(10))
    birth_date = db.Column(db.Date)
    weight_kg = db.Column(db.Float)
    health_status = db.Column(db.String(30), default="Healthy")
    notes = db.Column(db.Text)

    def age_display(self):
        if not self.birth_date:
            return "Unknown"
        days = (date.today() - self.birth_date).days
        years = days // 365
        months = (days % 365) // 30
        if years > 0:
            return f"{years}y {months}m"
        return f"{months}m"
    
class Crop(db.Model):
    __tablename__ = "crops"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    field_location = db.Column(db.String(80))
    area_acres = db.Column(db.Float)
    planting_date = db.Column(db.Date)
    expected_harvest_date = db.Column(db.Date)
    status = db.Column(db.String(30), default="Planted")  # Planted/Growing/Harvested
    yield_amount_kg = db.Column(db.Float)
    notes = db.Column(db.Text)