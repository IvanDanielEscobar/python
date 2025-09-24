from flask_sqlalchemy import SQLAlchemy()

db = SQLAlchemy

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable= False, unique=True)

class Reviews(db.Model):
    __tablename__ = 'reviews'
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.String(200), nullable=False)
    date = db.Column(db.DateTime, defult=db.func.now())
    #autor de la review
    user = db.relationship('User', backref='autor', lazy=True)
    
class Movies(db.Model):
    __tablename__ = 'movies'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False, unique=True)
    year = db.Column(db.DateTime)

class MovieGen(db.Model):
    