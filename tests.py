import server
import unittest
import json
import base64
from pymongo import MongoClient


def make_auth_header(username, password):
    string = username + ":" + password
    encoded_base64 = base64.b64encode(string.encode("utf-8"))
    decoded_base64 = encoded_base64.decode("utf-8").strip('\n')
    auth_header = {"Authorization": "Basic " + decoded_base64}
    return auth_header


def make_headers():
    headers = make_auth_header("ryankim", "12341234")
    headers["Content-Type"] = "application/json"
    return headers


class FlaskrTestCase(unittest.TestCase):

    def setUp(self):
        self.app = server.app.test_client()
        # Run app in testing mode to retrieve exceptions and stack traces
        server.app.config['TESTING'] = True

        # Inject test database into application
        mongo = MongoClient('localhost', 27017)
        db = mongo.test_database
        server.app.db = db

        # Drop collection (significantly faster than dropping entire db)
        db.drop_collection('trips')
        db.drop_collection('users')

    # User tests
    def test_post_user(self):
        response = self.app.post('/users/', data=json.dumps(dict(
                                 name="ryankim", password="12341234")),
                                 content_type='application/json')
        responseJSON = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 200)
        assert 'application/json' in response.content_type
        assert 'ryankim' in responseJSON["name"]

    def test_get_user(self):
        response = self.app.post('/users/',
                                 data=json.dumps(dict(
                                 name="ryankim", password="12341234")),
                                 content_type='application/json'
                                 )
        postResponseJSON = json.loads(response.data.decode())
        postedObjectID = postResponseJSON["_id"]

        response2 = self.app.get('/users/'+postedObjectID,
                                 headers=make_headers())
        responseJSON = json.loads(response2.data.decode())

        self.assertEqual(response2.status_code, 200)
        assert 'ryankim' in responseJSON["name"]
        assert 'application/json' in response2.content_type

    def test_get_non_existent_user(self):
        response = self.app.get('/users/55f0cbb4236f44b7f0e3cb23',
                                headers=make_headers())
        self.assertEqual(response.status_code, 404)

# Trip tests
    def test_post_trip(self):
        response = self.app.post('/users/', data=json.dumps(dict(
                                 name="ryankim", password="12341234")),
                                 content_type='application/json')

        response = self.app.post('/trips/',
                                 data=json.dumps(dict(name="New Trip",
                                 waypoints=["LA", "San Francisco"])),
                                 headers=make_headers())

        responseJSON = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 200)
        assert 'application/json' in response.content_type
        assert 'New Trip' in responseJSON["name"]

    def test_get_trip(self):
        response = self.app.post('/users/', data=json.dumps(dict(
                                 name="ryankim", password="12341234")),
                                 content_type='application/json')

        response = self.app.post('/trips/', data=json.dumps(dict(
                                 name="Trip to SF",
                                 waypoints=["Los Angeles, SF"])),
                                 headers=make_headers())

        postResponseJSON = json.loads(response.data.decode())
        postedObjectID = postResponseJSON["_id"]

        get_response = self.app.get('/trips/'+postedObjectID,
                                    headers=make_headers())
        responseJSON = json.loads(response.data.decode())

        self.assertEqual(get_response.status_code, 200)
        assert 'application/json' in response.content_type
        assert 'Trip to SF' in responseJSON["name"]

    def test_getting_all_trips(self):
        response = self.app.post('/users/', data=json.dumps(dict(
                                 name="ryankim", password="12341234")),
                                 content_type='application/json')

        self.app.post('/trips/', data=json.dumps(dict(
                      name="Trip to SF",
                      waypoints=["Los Angeles, SF"])),
                      headers=make_headers())

        self.app.post('/trips/', data=json.dumps(dict(
                      name="Trip to OR",
                      waypoints=["Utah, Sacremento"])),
                      headers=make_headers())

        response = self.app.get('/trips/', headers=make_headers())
        responseJSON = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(responseJSON), 2)

    def test_put_trip(self):
        response = self.app.post('/users/', data=json.dumps(dict(
                                 name="ryankim", password="12341234")),
                                 content_type='application/json')

        response = self.app.post('/trips/', data=json.dumps(dict(
                                 name="Trip to SF", waypoints=["LA", "SJ"])),
                                 headers=make_headers())

        postResponseJSON = json.loads(response.data.decode())
        postedObjectID = postResponseJSON["_id"]

        response_put = self.app.put('/trips/'+postedObjectID, data=json.dumps(dict(
                                    name="Trip to Seattle",
                                    _id=postedObjectID,
                                    waypoints=["San Jose", "Oregon"])),
                                    headers=make_headers())
        responseJSON = json.loads(response_put.data.decode())

        self.assertEqual(response_put.status_code, 200)
        assert 'application/json' in response.content_type
        assert 'Trip to Seattle' in responseJSON["name"]

    def test_delete_trip(self):
        response = self.app.post('/users/', data=json.dumps(dict(
                                 name="ryankim", password="12341234")),
                                 content_type='application/json')

        response = self.app.post('/trips/', data=json.dumps(dict(
                                 name="Trip to SF",
                                 waypoints=["LA", "SJ"])),
                                 headers=make_headers())

        postResponseJSON = json.loads(response.data.decode())
        postedObjectID = postResponseJSON["_id"]

        delete_response = self.app.delete('/trips/'+postedObjectID,
                                          headers=make_headers())
        get_response = self.app.get('/trips/'+postedObjectID, headers=make_headers())

        self.assertEqual(delete_response.status_code, 200)
        self.assertEqual(get_response.status_code, 404)
        assert 'application/json' in delete_response.content_type


if __name__ == '__main__':
    unittest.main()
