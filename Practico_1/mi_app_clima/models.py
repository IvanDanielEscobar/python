from app import db

class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    lat = db.Column(db.Float, nullable=False)
    lon = db.Column(db.Float, nullable=False)

#1- obtener todas las ciudades
City.query.all()

#2- obtener una ciudad por id
City.query.get(1)

#3- filtrar por nombre (exacto)
City.query.filter_by(nombre = "cordoba").first()

#4- filtrar condiciones avanzadas (OR, AND)
from sqlalchemy import or_, and_
City.query.filter(or_(City.lat < 0, City.lon > 100)).all()

#5- Buscar por nombre parcial (como un LIKE)
