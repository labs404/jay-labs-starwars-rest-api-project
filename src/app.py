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
from models import db, User, People, Vehicles, Planets, Favorites
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

###################################################################
# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

###################################################################
# added routes below
###################################################################

@app.route('/people', methods=['GET'])
def handle_people():
    return "<a href='/..'>Return home from Hello People.</a><br /><br /><br /><a href='/people/1'>click for person id #1</a>"

@app.route('/people/<int:person_id>', methods=['PUT','GET'])
def get_single_person(person_id):
    if request.method == 'GET':
        user1 = People.query.get(person_id)
        return jsonify(user1.serialize()), 200
    else:
        return "Person not found",404

@app.route('/planets', methods=['GET'])
def handle_planets():
    return "<a href='/..'>Return home from Hello Planets.</a><br /><br /><br /><a href='/planets/1'>click for planet id #1</a>"

@app.route('/planets/<int:planet_id>', methods=['PUT','GET'])
def get_single_planet(planet_id):
    if request.method == 'GET':
        planet1 = Planets.query.get(planet_id)
        return jsonify(planet1.serialize()), 200
    else:
        return "Planet not found",404

@app.route('/vehicles', methods=['GET'])
def handle_vehicles():
    return "<a href='/..'>Return home from Hello Vehicles.</a><br /><br /><br /><a href='/vehicles/4'>click for vehicle id #4</a>"

@app.route('/vehicles/<int:vehicle_id>', methods=['PUT','GET'])
def get_single_vehicle(vehicle_id):
    if request.method == 'GET':
        vehicle1 = Vehicles.query.get(vehicle_id)
        return jsonify(vehicle1.serialize()), 200
    else:
        return "Person not found",404
    
@app.route('/user', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200

@app.route('/user/favorites', methods=['GET'])
def get_user_favorites():
    user_favorites = Favorites.query.all()
    if request.method == 'GET':
        if user_favorites is None:
            return jsonify({'message': 'No favorites found'}), 404
        else:
            return jsonify(data=[user_favorites.serialize() for user_favorites in user_favorites]), 200


@app.route('/favorite/planet/', methods=['POST'])
def add_favorite_planet():

    data = request.get_json()
    new_favorite_planet = Favorites(user_id=data.user_id, planet_id=data["planet_id"])
    if request.method == 'POST':
        db.session.add(new_favorite_planet)
        db.session.commit()

    return jsonify(new_favorite_planet.serialize()), 200


@app.route('/favorite/people/', methods=['POST'])
def add_favorite_people():
    data = request.get_json()
    new_favorite_person = Favorites(user_id=data.user_id, person_id=data["person_id"])
    db.session.add(new_favorite_person)
    db.session.commit()

    return jsonify(data), 200


@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(planet_id):
    favorite_planet_to_delete = Favorites.query.get(planet_id)
    db.session.delete(favorite_planet_to_delete)
    db.session.commit()

    return jsonify({'message': 'Favorite successfully deleted.'}), 200


@app.route('/favorite/people/<int:person_id>', methods=['DELETE'])
def delete_favorite_people(person_id):
    favorite_person_to_delete = Favorites.query.get(person_id)
    db.session.delete(favorite_person_to_delete)
    db.session.commit()

    return jsonify({'message': 'Favorite successfully deleted.'}), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)

