from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(
    db.String(100), nullable=False
    )
    email = db.Column(
    db.String(100),
    unique=True,
    nullable=False,
    )
    reviews = db.relationship(
    "Review", backref="user", lazy=True
    )


class Movie(db.Model):
    __tablename__ = "movies"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(
    db.String(200), nullable=False
    )
    year = db.Column(db.Integer, nullable=False)
    genres = db.relationship(
    "Genre",
    secondary="movie_genre",
    backref="movies",
    )
    reviews = db.relationship(
    "Review", backref="movie", lazy=True
    )


class Genre(db.Model):
    __tablename__ = "genres"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(
    db.String(50), nullable=False
    )


class MovieGenre(db.Model):
    __tablename__ = "movie_genre"
    movie_id = db.Column(
    db.Integer,
    db.ForeignKey("movies.id"),
    primary_key=True,
    )
    genre_id = db.Column(
    db.Integer,
    db.ForeignKey("genres.id"),
    primary_key=True,
    )
    

class Review(db.Model):
    __tablename__ = "reviews"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
    db.Integer,
    db.ForeignKey("users.id"),
    nullable=False,
    )
    movie_id = db.Column(
    db.Integer,
    db.ForeignKey("movies.id"),
    nullable=False,
    )
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text)
    date = db.Column(db.Date)