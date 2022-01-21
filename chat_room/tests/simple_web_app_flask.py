import json
import unittest

from chat_room.src import simple_web_app_flask as app
from chat_room.src.simple_web_app_flask import db

BASE_URL = 'http://127.0.0.1:5000/'
BAD_ITEM_URL = f'{BASE_URL}/5'
GOOD_ITEM_URL = f'{BASE_URL}/home'


class TestFlaskApi(unittest.TestCase):

    def setUp(self):
        self.app = app.app.test_client()
        self.app.testing = True
        db.create_all()
        db.session.commit()

    def tearDown(self):
        import os
        os.remove('../src/site.db')

    def test_empty_users(self):
        # len of users is 0
        response = self.app.get(BASE_URL + 'users')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data())
        self.assertEqual(0, len(data['users']))

    def test_add_invalid_user(self):
        # missing email field = bad
        item = {"username": "some_item"}
        response = self.app.post(BASE_URL + 'create',
                                 data=json.dumps(item),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 400)

        # len of users is 0
        response = self.app.get(BASE_URL + 'users')
        self.assertEqual(200, response.status_code)
        data = json.loads(response.get_data())
        self.assertEqual(0, len(data['users']))

    def test_add_valid_user(self):
        # valid input
        item = {"username": "user1", "email": 'user1@email.com'}
        response = self.app.post(BASE_URL + 'create',
                                 data=json.dumps(item),
                                 content_type='application/json')
        self.assertEqual(201, response.status_code)

        # len of users is 1
        response = self.app.get(BASE_URL + 'users')
        self.assertEqual(200, response.status_code)
        data = json.loads(response.get_data())
        self.assertEqual(1, len(data['users']))
        expected = ["User('1', 'user1@email.com')"]
        self.assertListEqual(expected, data['users'])

        # second user
        item = {"username": "user2", "email": "user2@email.com"}
        response = self.app.post(BASE_URL + 'create',
                                 data=json.dumps(item),
                                 content_type='application/json')
        self.assertEqual(201, response.status_code)

        # len of users is 2
        response = self.app.get(BASE_URL + 'users')
        self.assertEqual(200, response.status_code)
        data = json.loads(response.get_data())
        self.assertEqual(2, len(data['users']))
        expected = ["User('1', 'user1@email.com')", "User('2', 'user2@email.com')"]
        self.assertListEqual(expected, data['users'])

    def test_update(self):
        # valid input
        item = {"username": "user1", "email": 'user1@email.com'}
        response = self.app.post(BASE_URL + 'create',
                                 data=json.dumps(item),
                                 content_type='application/json')
        self.assertEqual(201, response.status_code)

        # len of users is 1
        response = self.app.get(BASE_URL + 'users')
        self.assertEqual(200, response.status_code)
        data = json.loads(response.get_data())
        self.assertEqual(1, len(data['users']))
        expected = ["User('1', 'user1@email.com')"]
        self.assertListEqual(expected, data['users'])

        # update input
        item = {"username": "user1", "email": 'user11@email.com'}
        response = self.app.put(BASE_URL + 'update',
                                 data=json.dumps(item),
                                 content_type='application/json')
        self.assertEqual(200, response.status_code)

        # len of users is 1
        response = self.app.get(BASE_URL + 'users')
        self.assertEqual(200, response.status_code)
        data = json.loads(response.get_data())
        self.assertEqual(1, len(data['users']))
        expected = ["User('1', 'user11@email.com')"]
        self.assertListEqual(expected, data['users'])

    def test_create_group(self):
        item = {"groupname": "some_item"}
        response = self.app.post(BASE_URL + 'creategroup',
                                 data=json.dumps(item),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertIn('some_item', db.metadata.tables.keys())

    def test_join_group(self):
        # valid input
        item = {"username": "user1", "email": 'user1@email.com'}
        response = self.app.post(BASE_URL + 'create',
                                 data=json.dumps(item),
                                 content_type='application/json')
        self.assertEqual(201, response.status_code)

        item = {"groupname": "some_item", 'username': 'user1'}
        response = self.app.post(BASE_URL + 'joingroup',
                                 data=json.dumps(item),
                                 content_type='application/json')
        # self.assertEqual(200, response.status_code)


if __name__ == "__main__":
    unittest.main()
