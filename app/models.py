from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from .extensions import db

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    adoptions = db.relationship("AdoptionRequest", backref="requester", lazy=True)
    volunteer_apps = db.relationship("VolunteerApplication", backref="applicant", lazy=True)

    def set_password(self, password:str):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password:str) -> bool:
        return check_password_hash(self.password_hash, password)

class Animal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    species = db.Column(db.String(50), nullable=False)   # cão, gato, etc.
    breed = db.Column(db.String(120))
    age = db.Column(db.String(50))                       # ex: "2 anos", "6 meses"
    size = db.Column(db.String(30))                      # porte: pequeno/médio/grande
    sex = db.Column(db.String(10))                       # macho/fêmea
    city = db.Column(db.String(120))
    description = db.Column(db.Text)
    photo_url = db.Column(db.String(300))
    available = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    requests = db.relationship("AdoptionRequest", backref="animal", lazy=True)

class AdoptionRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    animal_id = db.Column(db.Integer, db.ForeignKey("animal.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    message = db.Column(db.Text)
    status = db.Column(db.String(20), default="Pendente")  # Pendente/Aprovado/Recusado
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class VolunteerApplication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    skills = db.Column(db.Text)
    availability = db.Column(db.String(120))  # fins de semana, noites, etc.
    status = db.Column(db.String(20), default="Pendente")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(180), nullable=False)
    date = db.Column(db.String(40), nullable=False)  # simples para demo
    city = db.Column(db.String(120))
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Campaign(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(180), nullable=False)
    description = db.Column(db.Text)
    link = db.Column(db.String(300))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)