"""Unit tests for users endpoints and resources."""
import unittest

import requests

from wayfare.routes.users import BASE_URL

_TEST_USERS = [
    {  # id: 1
        'first_name': 'Oliver',
        'last_name': 'Wang',
        'email': 'owang02@calpoly.edu',
        'password': 'password123'
    },
    {  # id: 2
        'first_name': 'Karissa',
        'last_name': 'Bennett',
        'email': 'kbenne09@calpoly.edu',
        'password': 'deadlifts'
    },
    {  # id: 3
        'first_name': 'Barack',
        'last_name': 'Obama',
        'email': 'email@example.com',
        'password': 'america'
    },
    {  # id: 4
        'first_name': 'Minh-Quan',
        'last_name': 'Tran',
        'email': 'mtran22@calpoly.edu',
        'password': 'Yeah, my password is really long.'
    }
]


class TestUserBase(unittest.TestCase):
    """Base class for user route tests. Provides a common test setUp method."""
    def setUp(self):
        """Replace all source data with test user data."""
        self.scheme = 'http://'
        self.base_url = 'localhost'
        self.port = 5000
        self.route = BASE_URL
        self.endpoint = f'{self.scheme}{self.base_url}:{self.port}{self.route}'
        # Clear source and load all test data.
        requests.delete(self.endpoint)
        for user in _TEST_USERS:
            requests.post(self.endpoint, user)


class TestUsers(TestUserBase):
    """Tests for the Users resource."""
    def test_get_and_id_generation(self):
        response = requests.get(self.endpoint).json()
        self.assertEqual(len(response), 4)
        for index, user in enumerate(response):
            self.assertEqual(user['id'], index + 1)
            self.assertEqual(user['email'], _TEST_USERS[index]['email'])

    def test_post_missing_first_name(self):
        response = requests.post(self.endpoint, {
            'last_name': 'test',
            'email': 'email@example.com',
            'password': 'test'
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn('first_name', response.json()['message'])

    def test_post_missing_last_name(self):
        response = requests.post(self.endpoint, {
            'first_name': 'test',
            'email': 'email@example.com',
            'password': 'test'
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn('last_name', response.json()['message'])

    def test_post_missing_email(self):
        response = requests.post(self.endpoint, {
            'first_name': 'test',
            'last_name': 'test',
            'password': 'test'
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn('email', response.json()['message'])

    def test_post_missing_password(self):
        response = requests.post(self.endpoint, {
            'first_name': 'test',
            'last_name': 'test',
            'email': 'email@example.com'
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn('password', response.json()['message'])

    def test_post_duplicate_email(self):
        duplicate_email = _TEST_USERS[0]['email']
        response = requests.post(self.endpoint, {
            'first_name': 'test',
            'last_name': 'test',
            'email': duplicate_email,
            'password': 'test'
        })
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['message'], "Duplicate email: '{}'".format(duplicate_email))

    def test_successful_post(self):
        new_user = {
            'first_name': 'test',
            'last_name': 'test',
            'email': 'unique_email@example.com',
            'password': 'test'
        }
        post_response = requests.post(self.endpoint, new_user)
        self.assertEqual(post_response.status_code, 201)
        self.assertEqual(post_response.json(), '')  # Expect an empty body.
        new_user_id = len(_TEST_USERS) + 1
        expected_location = f'{self.endpoint}/{new_user_id}'
        self.assertEqual(post_response.headers['Location'], expected_location)
        new_user.update({
            'id': new_user_id
        })
        new_user.pop('password')
        get_response = requests.get(self.endpoint)
        self.assertEqual(get_response.status_code, 200)
        expected_location = '{}/{}'.format(self.endpoint, new_user['id'])
        self.assertEqual(get_response.json()[-1], new_user)

    def test_put_not_allowed(self):
        response = requests.put(self.endpoint)
        self.assertEqual(response.status_code, 405)


class TestUserById(TestUserBase):
    """Tests for the UserById resource."""
    def test_get_first_user(self):
        first_user_id = 1
        first_user = {
            'id': first_user_id,
            **_TEST_USERS[0]
        }
        response = requests.get(f'{self.endpoint}/{first_user_id}')
        self.assertEqual(response.status_code, 200)
        first_user.pop('password')
        self.assertEqual(response.json(), first_user)

    def test_get_nonexistent_id(self):
        nonexistent_id = 9001
        response = requests.get(f'{self.endpoint}/{nonexistent_id}')
        self.assertEqual(response.status_code, 404)

    def test_update_first_user(self):
        first_user_id = 1
        updated_first_user = dict(_TEST_USERS[0])
        updated_first_user.update({
            'first_name': 'newname',
        })
        put_response = requests.put(f'{self.endpoint}/{first_user_id}', updated_first_user)
        self.assertEqual(put_response.status_code, 200)
        get_response = requests.get(f'{self.endpoint}/{first_user_id}')
        self.assertEqual(get_response.status_code, 200)
        self.assertEqual(get_response.json()['first_name'], updated_first_user['first_name'])

    # Rethinking how PUT on a nonexistent id should work.
    # def test_update_nonexistent_user(self):
    #     nonexistent_id = 9001
    #     response = requests.put('{}/{}'.format(self.endpoint, nonexistent_id))
    #     self.assertEqual(response.status_code, 404)

    def test_delete_first_user(self):
        first_user_id = 1
        response = requests.delete(f'{self.endpoint}/{first_user_id}')
        self.assertEqual(response.status_code, 200)
        for user in requests.get(self.endpoint).json():
            self.assertNotEqual(user['id'], first_user_id)

    def test_delete_nonexistent_user(self):
        nonexistent_id = 9001
        delete_response = requests.delete(f'{self.endpoint}/{nonexistent_id}')
        self.assertEqual(delete_response.status_code, 404)
        get_response = requests.get(self.endpoint)
        self.assertEqual(len(get_response.json()), len(_TEST_USERS))




if __name__ == '__main__':
    unittest.main()
