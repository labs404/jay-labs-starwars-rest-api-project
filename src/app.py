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

@app.route('/user', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200


######################################
# START get all people/planet/vehicles
@app.route('/people', methods=['GET'])
def return_all_people():
    all_people = People.query.all()
    all_people = list(map(lambda index: index.serialize(), all_people))
    response_body = all_people
    return jsonify(response_body), 200

@app.route('/planets', methods=['GET'])
def return_all_planets():
    all_planets = Planets.query.all()
    all_planets = list(map(lambda index: index.serialize(), all_planets))
    response_body = all_planets
    return jsonify(response_body), 200

@app.route('/vehicles', methods=['GET'])
def return_all_vehicles():
    all_vehicles = Vehicles.query.all()
    all_vehicles = list(map(lambda index: index.serialize(), all_vehicles))
    response_body = all_vehicles
    return jsonify(response_body), 200
# END get all people/planet/vehicles
####################################



############################################
# START get individual people/planet/vehicle
@app.route('/people/<int:person_id>', methods=['GET'])
def return_single_person(person_id):
    single_person = People.query.get(person_id)
    return jsonify(single_person.serialize()), 200

@app.route('/planets/<int:planet_id>', methods=['GET'])
def return_single_planet(planet_id):
    single_planet = Planets.query.get(planet_id)
    return jsonify(single_planet.serialize()), 200

@app.route('/vehicles/<int:vehicle_id>', methods=['GET'])
def return_single_vehicle(vehicle_id):
    single_vehicle = Vehicles.query.get(vehicle_id)
    return jsonify(single_vehicle.serialize()), 200
# END get individual people/planet/vehicle
##########################################



##############################
# START get all user favorites
@app.route('/user/favorites', methods=['GET'])
def get_user_favorites():
    user_favorites = Favorites.query.all()
    if request.method == 'GET':
        if user_favorites is None:
            return jsonify({'message': 'No favorites found'}), 404
        else:
            return jsonify(data=[user_favorites.serialize() for user_favorites in user_favorites]), 200
# START get all user favorites
##############################



#####################################
# START get individual user favorites
@app.route('/user/<int:user_id>/favorites/', methods=['GET'])
def return_individual_user_favorites(user_id):
    individual_user_favorites = Favorites.query.all()[user_id - 1]
    returnable_favorites = {
        "favorite_person": individual_user_favorites.person_id,
        "favorite_planet": individual_user_favorites.planet_id,
        "favorite_vehicle": individual_user_favorites.vehicle_id
    }
    return jsonify(data=[returnable_favorites])
# END get individual user favorites
###################################


##############################################################
# START add and delete favorite person for one individual user
@app.route('/user/<int:user_id>/favorites/people/<int:person_id>', methods=['POST', 'DELETE'])
def add_or_delete_favorite_person(user_id, person_id):
    body = request.get_json()
    if request.method == 'POST':
        individual_user_favorites = Favorites.query.filter_by(user_id=user_id).first()
        individual_user_favorites.person_id = person_id
        db.session.commit()
        return jsonify("Person added to favorites",individual_user_favorites.serialize())
    
    if request.method == 'DELETE':
        individual_user_favorites = Favorites.query.filter_by(user_id=user_id).first()
        individual_user_favorites.person_id = None
        db.session.commit()
        return jsonify("Person deleted from favorites", individual_user_favorites.serialize())
    
    return "POST or DELETE requests were invalid", 404
# END add and delete favorite person for one individual user
# ##########################################################



##############################################################
# START add and delete favorite planet for one individual user
@app.route('/user/<int:user_id>/favorites/planets/<int:planet_id>', methods=['POST', 'DELETE'])
def add_or_delete_favorite_planet(user_id, planet_id):
    body = request.get_json()
    if request.method == 'POST':
        individual_user_favorites = Favorites.query.filter_by(user_id=user_id).first()
        individual_user_favorites.planet_id = planet_id
        db.session.commit()
        return jsonify("Planet added to favorites",individual_user_favorites.serialize())
    
    if request.method == 'DELETE':
        individual_user_favorites = Favorites.query.filter_by(user_id=user_id).first()
        individual_user_favorites.planet_id = None
        db.session.commit()
        return jsonify("Planet deleted from favorites", individual_user_favorites.serialize())
    
    return "POST or DELETE requests were invalid", 404
# END add and delete favorite planet for one individual user
# ##########################################################



##############################################################
# START add and delete vehicle person for one individual user
@app.route('/user/<int:user_id>/favorites/vehicles/<int:vehicle_id>', methods=['POST', 'DELETE'])
def add_or_delete_favorite_vehicle(user_id, vehicle_id):
    body = request.get_json()
    if request.method == 'POST':
        individual_user_favorites = Favorites.query.filter_by(user_id=user_id).first()
        individual_user_favorites.vehicle_id = vehicle_id
        db.session.commit()
        return jsonify("Vehicle added to favorites",individual_user_favorites.serialize())
    
    if request.method == 'DELETE':
        individual_user_favorites = Favorites.query.filter_by(user_id=user_id).first()
        individual_user_favorites.vehicle_id = None
        db.session.commit()
        return jsonify("Vehicle deleted from favorites", individual_user_favorites.serialize())
    
    return "POST or DELETE requests were invalid", 404
# END add and delete vehicle person for one individual user
# ##########################################################



# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)