"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Parent, Child, Planet, FavoritePlanets
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200

@app.route('/get-data', methods=['GET'])
def get_data():
    parent = Parent.query.get(1)
    user = User.query.get(1)
    print(user.planets_favorites)
    favorite_planets_serialized = []
    for fav in user.planets_favorites:
        print(f'({fav.user.serialize()} {fav.planet.serialize()})')
        favorite_planets_serialized.append(fav.planet.serialize())
    children_serialized = []
    for child in parent.children:
        children_serialized.append(child.serialize())
    favorite_planets_by_user = FavoritePlanets.query.filter_by(user_id=1).all()
    for fav_planet in favorite_planets_by_user: 
        print(fav_planet.planet.serialize())
    return jsonify({'msg': 'ok',
                    'parent': parent.serialize(),
                    'children': children_serialized,
                    "favorite_planets": favorite_planets_serialized})

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
