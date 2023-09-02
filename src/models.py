from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.db.Integer, primary_key=True)
    email = db.Column(db.db.String(120), unique=True, nullable=False)
    password = db.Column(db.db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }

class People(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    persons_name = db.Column(db.String(50), nullable=False)
    height = db.Column(db.String(50), nullable=True)
    mass = db.Column(db.String(50), nullable=True)
    hair_color = db.Column(db.String(50), nullable=True)
    skin_color = db.Column(db.String(50), nullable=True)
    eye_color = db.Column(db.String(50), nullable=True)
    birth_year = db.Column(db.String(50), nullable=True)
    gender = db.Column(db.String(50), nullable=True)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.persons_name,
            "height": self.height,
            "mass": self.mass,
            "hair_color": self.hair_color,
            "skin_color": self.skin_color,
            "eye_color": self.eye_color,
            "gender": self.gender,
        }

class Planets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    planet_name = db.Column(db.String(30), nullable=False)
    diameter = db.Column(db.String(30), nullable=False)
    rotation_period = db.Column(db.String(30), nullable=False)
    orbital_period = db.Column(db.String(30), nullable=False)
    gravity = db.Column(db.String(30), nullable=False)
    population = db.Column(db.String(30), nullable=False)
    climate = db.Column(db.String(30), nullable=False)
    terrain = db.Column(db.String(30), nullable=False)
    description = db.Column(db.String(30), nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.planet_name,
            "diameter": self.diameter,
            "rotation_period": self.rotation_period,
            "orbital_period":self.orbital_period,
            "gravity": self.gravity,
            "population": self.population,
            "climate": self.climate,
            "terrain": self.terrain,
            "description": self.description
        }

class Vehicles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vehicle_name = db.Column(db.String(50), nullable=False)
    model = db.Column(db.String(50), nullable=False)
    manufacturer = db.Column(db.String(50), nullable=True)
    cost_in_credits = db.Column(db.String(50), nullable=True)
    length = db.Column(db.String(50), nullable=True)
    max_atmosphering_speed = db.Column(db.String(50), nullable=True)
    cargo_capacity = db.Column(db.String(50), nullable=True)
    consumables = db.Column(db.String(50), nullable=True)
    vehicle_class = db.Column(db.String(50), nullable=True)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.vehicle_name,
            "model": self.model,
            "manufacturer": self.manufacturer,
            "cost_in_credits": self.cost_in_credits,
            "length": self.length,
            "max_atmosphering_speed": self.max_atmosphering_speed,
            "cargo_capacity": self.cargo_capacity,
            "consumables": self.consumables,
            "vehicle_class": self.vehicle_class
        }


