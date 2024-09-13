from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    planets_favorites = db.relationship('FavoritePlanets', back_populates='user')
    following = db.relationship('Follow', foreign_keys='Follow.follower_id', back_populates='follower', cascade="all, delete-orphan")
    followers = db.relationship('Follow', foreign_keys='Follow.followed_id', back_populates='followed', cascade="all, delete-orphan")

    def __repr__(self):
        return '<User %r>' % self.email

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }

class Follow(db.Model):
    __tablename__ = 'follow'
    id = db.Column(db.Integer, primary_key=True)
    
    # Llave foránea al usuario que sigue
    follower_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # Llave foránea al usuario seguido
    followed_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    # Relaciones bidireccionales con la tabla 'User'
    follower = db.relationship('User', foreign_keys=[follower_id], back_populates='following')
    followed = db.relationship('User', foreign_keys=[followed_id], back_populates='followers')

class Planet(db.Model):
    __tablename__ = 'planet'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    population = db.Column(db.Integer, nullable=False)
    favorite_by = db.relationship("FavoritePlanets", back_populates='planet')

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "population": self.population
        }
    
class FavoritePlanets(db.Model):
    __tablename__ = 'favorite_planets'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    user = db.relationship("User", back_populates="planets_favorites")
    planet_id = db.Column(db.Integer, db.ForeignKey("planet.id"))
    planet = db.relationship("Planet", back_populates="favorite_by") 

    def serialize(self):
        return {
            'id': self.id,
            'user': self.user.serialize(),
            'planet': self.planet.serialize()
        }


class Parent(db.Model):
    __tablename__ = 'parent_table'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    children = db.relationship("Child", back_populates="parent")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "children": [child.serialize() for child in self.children]
        }

class Child(db.Model):
    __tablename__ = 'child_table'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey("parent_table.id"))
    parent = db.relationship("Parent", back_populates="children")  

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "parent_id": self.parent_id
        }

