import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from sqlalchemy.sql import exists
import dateutil.parser

database_path = os.environ['DATABASE_URL']

db = SQLAlchemy()


'''
setup_db(app) binds a flask application and a SQLAlchemy service.
'''


def setup_db(app, db_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = db_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


'''
date_valid(date_str) ensures that a valid date string has been entered so that it may be stored in the database.
'''


def date_valid(date_str):
    try:
        is_valid = dateutil.parser.parse(date_str)
        return True
    except ValueError:
        return False


'''
Movie is a persistent movie entity that extends the base SQLAlchemy Model.
'''


class Movie(db.Model):
    __tablename__ = 'Movie'

    movie_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False, unique=True)
    release_date = db.Column(db.Date, nullable=False)

    def __init__(self, title, release_date):
        self.title = title
        self.release_date = release_date

    # Inserts a new movie into a database. It must have a unique name and id. It must have a release date.
    def insert(self):
        db.session.add(self)
        db.session.commit()

    # Updates a movie in the database. The movie_id must already exist.
    def update(self):
        db.session.commit()

    # Deletes a movie in the database. The movie_id must already exist.
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {'movie_id': self.movie_id,
                'title': self.title,
                'release_date': self.release_date.strftime('%Y-%m-%d')}

    def __repr__(self):
        return '<Movie %r>' % self

    # Determines if the movie to be added is already in the database.
    def is_duplicate(self):
        return db.session.query(exists().where(func.lower(Movie.title) == func.lower(
            self.title))).scalar()


'''
Actor is a persistent actor entity that extends the base SQLAlchemy Model.
'''


class Actor(db.Model):
    __tablename__ = 'Actor'

    actor_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    birth_date = db.Column(db.Date, nullable=False)
    gender = db.Column(db.String, nullable=False)

    def __init__(self, name, birth_date, gender):
        self.name = name
        self.birth_date = birth_date
        self.gender = gender

    # Inserts a new actor into a database. It must have a unique name and id. It must have a birth_date and gender.
    def insert(self):
        db.session.add(self)
        db.session.commit()

    # Updates an actor in the database. The actor_id must already exist.
    def update(self):
        db.session.commit()

    # Deletes an actor in the database. The actor_id must already exist.
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {'actor_id': self.actor_id,
                'name': self.name,
                'birth_date': self.birth_date.strftime('%Y-%m-%d'),
                'gender': self.gender}

    def __repr__(self):
        return '<Actor %r>' % self

    # Determines if the actor to be added is already in the database.
    def is_duplicate(self):
        return db.session.query(exists().where(func.lower(Actor.name) == func.lower(
            self.name))).scalar()
