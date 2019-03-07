"""Unit tests for User models."""
import unittest

from wayfare.exceptions import DuplicateEmailError
from wayfare.exceptions import InvalidEmailError
from wayfare.exceptions import InvalidFirstNameError
from wayfare.exceptions import InvalidLastNameError
from wayfare.models import User

# TODO: Test update, delete methods from AbstractModelBase

class TestUser(unittest.TestCase):
    """Tests for the User model."""
    def setUp(self):
        User.delete_all()

    def test_create(self):
        user = User(
            first_name='firstname',
            last_name='lastname',
            email='email@example.com',
            password='password'
        )
        user.create()
        self.assertEqual(user.id, 1)
        self.assertEqual(user.first_name, 'firstname')
        self.assertEqual(user.last_name, 'lastname')
        self.assertEqual(user.email, 'email@example.com')
        self.assertEqual(user.password, 'password')

    def test_invalid_email(self):
        invalid_email = 'not_an_email'
        with self.assertRaises(InvalidEmailError):
            User(
                first_name='Tony',
                last_name='Stark',
                email=invalid_email,
                password='password123'
            )
        invalid_email = 'not_an_email@@example.com'
        with self.assertRaises(InvalidEmailError):
            User(
                first_name='Tony',
                last_name='Stark',
                email=invalid_email,
                password='password'
            )
        invalid_email = 'not_an_email@example'
        with self.assertRaises(InvalidEmailError):
            User(
                first_name='Tony',
                last_name='Stark',
                email=invalid_email,
                password='password'
            )

    def test_valid_email(self):
        valid_email = 'example@example.com'
        valid_user = User(
            first_name='test',
            last_name='test',
            email=valid_email,
            password='test'
        )
        valid_user.create()
        self.assertEqual(valid_user.email, valid_email)

    def test_duplicate_email(self):
        duplicate_email = 'email@example.com'
        user_with_email = User(
            first_name='test',
            last_name='test',
            email=duplicate_email,
            password='test'
        )
        user_with_email.create()
        with self.assertRaises(DuplicateEmailError):
            User(
                first_name='Tony',
                last_name='Stark',
                email=duplicate_email,
                password='password123'
            )

    def test_invalid_first_name(self):
        invalid_name = 'kari*'
        with self.assertRaises(InvalidFirstNameError):
            User(
                first_name=invalid_name,
                last_name='Bennett',
                email='email@example.com',
                password='password'
            )

        invalid_name = "a" * 65
        with self.assertRaises(InvalidFirstNameError):
            User(
                first_name=invalid_name,
                last_name='Bennett',
                email='email@example.com',
                password='password'
            )

    def test_valid_first_name(self):
        valid_name = 'Kari'
        valid_user = User(
            first_name=valid_name,
            last_name='Bennett',
            email='email@example.com',
            password='password'
        )
        valid_user.create()
        self.assertEqual(valid_user.first_name, valid_name)

        valid_name = 'Mary-Kate'
        valid_user2 = User(
            first_name=valid_name,
            last_name='Bennett',
            email='eemail@example.com',
            password='password'
        )
        valid_user2.create()
        self.assertEqual(valid_user2.first_name, valid_name)

    def test_invalid_last_name(self):
        invalid_name = '*bennett'
        with self.assertRaises(InvalidLastNameError):
            User(
                first_name='kari',
                last_name=invalid_name,
                email='email@example.com',
                password='password'
            )
        invalid_name = 'b' * 75
        with self.assertRaises(InvalidLastNameError):
            User(
                first_name='kari',
                last_name=invalid_name,
                email='email@example.com',
                password='password'
            )

    def test_valid_last_name(self):
        valid_name = 'Bennett'
        valid_user = User(
            first_name='kari',
            last_name=valid_name,
            email='email@example.com',
            password='password'
        )
        valid_user.create()
        self.assertEqual(valid_user.last_name, valid_name)

        valid_name = 'Bennett-Polansky'
        valid_user2 = User(
            first_name='kari',
            last_name=valid_name,
            email='eemail@example.com',
            password='password'
        )
        valid_user2.create()
        self.assertEqual(valid_user2.last_name, valid_name)

    def test_find_nonexistent_id(self):
        nonexistent_id = 5
        user_with_id = User(
            first_name='test',
            last_name='test',
            email='email@example.com',
            password='password'
        )
        user_with_id.create()
        result = User.find_by_id(nonexistent_id)
        self.assertEqual(result, None)

    def test_find_existing_id(self):
        existing_id = 1
        user_with_id = User(
            first_name='test',
            last_name='test', 
            email='email@example.com',
            password='password'
        )
        user_with_id.create()
        result = User.find_by_id(existing_id)
        self.assertEqual(result.id, existing_id)

    def test_find_nonexistent_email(self):
        nonexistent_email = 'exampleemail@example.com'
        user_with_email = User(
            first_name='test',
            last_name='test',
            email='email@email.com',
            password='password123'
        )
        user_with_email.create()
        result = User.find_by_email(nonexistent_email)
        self.assertEqual(result, None)

    def test_find_existing_email(self):
        valid_email = 'example@email.com'
        user_with_email = User(
            first_name='test',
            last_name='test',
            email=valid_email,
            password='test123'
        )
        user_with_email.create()
        result = User.find_by_email(valid_email)
        self.assertEqual(result.email, valid_email)

if __name__ == '__main__':
    unittest.main()
