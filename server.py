from flask import Flask, request, make_response, jsonify
from flask_restful import Resource, Api
from pymongo import MongoClient
import bcrypt
import base64
from bson.objectid import ObjectId
from utils.mongo_json_encoder import JSONEncoder


# Basic Setup
app = Flask(__name__)
mongo = MongoClient('localhost', 27017)
app.db = mongo.develop_database
api = Api(app)
app.bcrypt_rounds = 12


def check_auth(username, password):
    user_collection = app.db.myobjects
    user = user_collection.find_one({"username": username})
    if user is None:
        return False
    stored_pw = user["password"]
    encoded_pw = password.encode("utf-8")
    hashed_pw = bcrypt.hashpw(encoded_pw, stored_pw)
    return stored_pw == hashed_pw


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            message = {'error': 'Basic Auth Required.'}
            resp = jsonify(message)
            resp.status_code = 401
            return resp

        return f(*args, **kwargs)
    return decorated


# User architecture
class User(Resource):

    def post(self):
        new_user = request.json
        user_collection = app.db.users
        # user = user_collection.find_one({"name": new_user["name"]})
        # if user is None:
        encoded_pw = new_user["password"].encode('utf-8')
        hashed_pw = bcrypt.hashpw(encoded_pw,
                                  bcrypt.gensalt(app.bcrypt_rounds))
        new_user["password"] = hashed_pw
        result = user_collection.insert_one(new_user)
        user = user_collection.find_one({"_id":
                                        ObjectId(result.inserted_id)})

        del user["password"]
        return user

    def get(self, user_id):
        user_collection = app.db.myobjects
        user = user_collection.find_one({"_id": ObjectId(user_id)})
        if user is None:
            response = jsonify(data=user)
            response.status_code = 404
            return response
        else:
            return user


# Trip architecture
class Trip(Resource):
    # @requires_auth
    def post(self):
        new_trip = request.json
        trip_collection = app.db.trips
        result = trip_collection.insert_one(new_trip)
        posted_trip = trip_collection.find_one({"_id":
                                                ObjectId(result.inserted_id)})
        return posted_trip

<<<<<<< HEAD
    # @requires_auth
=======
    # [Ben-G] You still need to implement the "get all trips" functionality.
    # All trips should be returned when /trips/ is called
    @requires_auth
>>>>>>> 8bce11cb116352c1cfe02dadd593591b6f470567
    def get(self, trip_id):
        trip_collection = app.db.trips
        trip = trip_collection.find_one({"_id": ObjectId(trip_id)})
        if trip is None:
            response = jsonify(data=trip)
            response.status_code = 404
            return response
        else:
            return trip

    # [Ben-G] Instead of refetching the trip, you can use the
    # result from `delete_one` to verify that the deletion was
    # successful
    def delete(self, trip_id):
        trip_collection = app.db.trips
        trip_collection.delete_one({"_id": ObjectId(trip_id)})
        deleted_trip = trip_collection.find_one({"_id": ObjectId(trip_id)})
        if deleted_trip is not None:
            response = jsonify(data=deleted_trip)
            response.status_code = 404
            return response
        else:
            return deleted_trip

    def put(self, trip_id):
        updated_trip = request.json
        trip_collection = app.db.trips
        # which function should I use to set/update the trip

        result = trip_collection.update_one({"_id": ObjectId(trip_id)},
                                            {'$set': updated_trip})
        check_trip = trip_collection.find_one({"_id": ObjectId(trip_id)})
        return check_trip

<<<<<<< HEAD
=======

# User architecture
class User(Resource):

    def post(self):
        new_user = request.json
        user_collection = app.db.users
        hashed_pw = bcrypt.hashpw(new_user["password"], bcrypt.gensalt())
        result = user_collection.insert_one(new_user)
        user = user_collection.find_one({"_id": ObjectId(result.inserted_id)})
        if bcrypt.hashpw(responseJSON["password"], hashed_pw) == hashed_pw:
            return true

        return user

    # [Ben-G] This endpoint should require authentication
    def get(self, myobject_id):
        user_collection = app.db.myobjects
        myobject = user_collection.find_one({"_id": ObjectId(myobject_id)})
        if myobject is None:
            response = jsonify(data=myobject)
            response.status_code = 404
            return response
        else:
            return myobject


>>>>>>> 8bce11cb116352c1cfe02dadd593591b6f470567
# Add REST resource to API
api.add_resource(User, '/users/', '/users/<string:user_id>')
api.add_resource(Trip, '/trips/', '/trips/<string:trip_id>')


# provide a custom JSON serializer for flaks_restful
@api.representation('application/json')
def output_json(data, code, headers=None):
    resp = make_response(JSONEncoder().encode(data), code)
    resp.headers.extend(headers or {})
    return resp


if __name__ == '__main__':
    # Turn this on in debug mode to get detailled information about
    # request related exceptions: http://flask.pocoo.org/docs/0.10/config/
    app.config['TRAP_BAD_REQUEST_ERRORS'] = True
    app.run(debug=True)
