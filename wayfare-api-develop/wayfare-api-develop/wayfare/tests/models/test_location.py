"""Unit tests for Location models."""
import unittest

from wayfare.models import Location

# TODO: Test update, delete methods from AbstractModelBase

class TestLocation(unittest.TestCase):
    """Tests for the Location model."""
    def setUp(self):
        Location.delete_all()

    def test_create(self):
        location = Location(
            name='San Francisco'
        )
        location.create()
        self.assertEqual(location.name, 'San Francisco')
        self.assertEqual(location.id, 1)

    def test_find_nonexistent_id(self):
        nonexistent_id = 5
        location_with_id = Location(
            name='San Francisco'
        )
        location_with_id.create()
        result = Location.find_by_id(nonexistent_id)
        self.assertEqual(result, None)

    def test_find_existing_id(self):
        existing_id = 1
        location_with_id = Location(
            name='San Francisco'
        )
        location_with_id.create()
        result = Location.find_by_id(existing_id)
        self.assertEqual(result.id, existing_id)

    def test_find_nonexistent_name(self):
        nonexistent_name = 'Los Angeles'
        location_with_name = Location(
            name='San Francisco'
        )
        location_with_name.create()
        result = Location.find_by_name(nonexistent_name)
        self.assertEqual(result, None)

    def test_find_existing_id(self):
        existing_name = 'San Francisco'
        location_with_name = Location(
            name='San Francisco'
        )
        location_with_name.create()
        result = Location.find_by_name(existing_name)
        self.assertEqual(result.name, existing_name)


if __name__ == '__main__':
    unittest.main()
