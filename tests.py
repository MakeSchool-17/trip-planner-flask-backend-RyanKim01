import server
import unittest
import json
import bcrypt
import base64
from pymongo import MongoClient


def make_auth_header(username="ryankim", password="12341234"):
    string = username + ":" + password
    # import pdb; pdb.set_trace()
    encoded_base64 = base64.b64encode(string.encode("utf-8"))
    decoded_base64 = encoded_base64.decode("utf-8")
    auth_header = {"Authorization": "Basic " + decoded_base64}
    return auth_header


def make_headers():
    headers = make_auth_header()
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
    #
    # def test_get_user(self):
    #
    #     response = self.app.post('/users/',
    #                              data=json.dumps(dict(
    #                              name="ryankim", password="12341234")),
    #                              content_type='application/json'
    #                              )
    #
    #     postResponseJSON = json.loads(response.data.decode())
    #     postedObjectID = postResponseJSON["_id"]
    #
    #     response = self.app.get('/users/'+postedObjectID,
    #                             headers=make_headers())
    #     responseJSON = json.loads(response.data.decode())
    #
    #     self.assertEqual(response.status_code, 200)
    #     assert 'ryankim' in responseJSON["name"]
    #     assert 'application/json' in response.content_type
    #
    # def test_get_non_existent_user(self):
    #     response = self.app.get('/users/55f0cbb4236f44b7f0e3cb23',
    #                             headers=make_headers())
    #     self.assertEqual(response.status_code, 404)

# Trip tests
    # def test_post_trip(self):
    #     response = self.app.post('/trips/',
    #                              data=json.dumps(dict(name="New Trip",
    #                              waypoints=["LA", "San Francisco"])),
    #                              headers=make_headers())
    #
    #     responseJSON = json.loads(response.data.decode())
    #
    #     self.assertEqual(response.status_code, 200)
    #     assert 'application/json' in response.content_type
    #     assert 'New Trip' in responseJSON["name"]

    # def test_get_trip(self):
    #     response = self.app.post('/users/', data=json.dumps(dict(
    #                              name="ryankim", password="12341234")),
    #                              content_type='application/json')
    #
    #     response2 = self.app.post('/trips/', data=json.dumps(dict(
    #                               name="Trip to SF",
    #                               waypoints=["Los Angeles, SF"])),
    #                               headers=make_headers())
    #
    #     postResponseJSON = json.loads(response2.data.decode())
    #     postedObjectID = postResponseJSON["_id"]
    #
    #     get_response = self.app.get('/trips/'+postedObjectID,
    #                                 headers=make_headers())
    #     responseJSON = json.loads(response.data.decode())
    #
    #     self.assertEqual(get_response.status_code, 200)
    #     assert 'application/json' in response.content_type
    #     assert 'Trip to SF' in responseJSON["name"]

    # def test_getting_all_trips(self):
    #     response1 = self.app.post('/trips/', data=json.dumps(dict(
    #                               name="Trip to SF",
    #                               waypoints=["Los Angeles, SF"])),
    #                               headers=make_headers())
    #
    #     response2 = self.app.post('/trips/', data=json.dumps(dict(
    #                               name="Trip to SF",
    #                               waypoints=["Los Angeles, SF"])),
    #                               headers=make_headers())
    #
    #

    # [Ben-G] This test is a duplicate of test above
    # def test_getting_non_existent_trip(self):
    #     response = self.app.get('/trips/55f0cbb4236f44b7f0e3cb23')
    #     self.assertEqual(response.status_code, 404)

    # def test_put_trip(self):
    #     response = self.app.post('/trips/', data=json.dumps(dict(
    #                              name="Trip to SF", waypoints=["LA", "SJ"])),
    #                              headers=make_headers())
    #
    #     postResponseJSON = json.loads(response.data.decode())
    #     postedObjectID = postResponseJSON["_id"]
    #
    #     response = self.app.put('/trips/'+postedObjectID, data=json.dumps(dict(
    #                             name="Trip to Seattle",
    #                             waypoints=["San Jose", "Oregon"])),
    #                             headers=make_headers())
    #     responseJSON = json.loads(response.data.decode())
    #
    #     self.assertEqual(response.status_code, 200)
    #     assert 'application/json' in response.content_type
    #     assert 'Trip to Seattle' in responseJSON["name"]
    #
    # def test_delete_trip(self):
    #     response = self.app.post('/trips/', data=json.dumps(dict(
    #                              name="Trip to SF",
    #                              waypoints=["LA", "SJ"])),
    #                              headers=make_headers())
    #
    #     postResponseJSON = json.loads(response.data.decode())
    #     assert "_id" in postResponseJSON
    #     postedObjectID = postResponseJSON["_id"]
    #
    #     delete_response = self.app.delete('/trips/'+postedObjectID,
    #                                       headers=make_headers())
    #
    #     self.assertEqual(delete_response.status_code, 200)
    #     assert 'application/json' in response.content_type

if __name__ == '__main__':
    unittest.main()
