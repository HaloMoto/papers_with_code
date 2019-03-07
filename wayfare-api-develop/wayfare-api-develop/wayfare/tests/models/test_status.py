"""Unit tests for Status models."""
import unittest

from wayfare.models import Status

# TODO: Test update, delete methods from AbstractModelBase

class TestStatus(unittest.TestCase):
    """Tests for the Status model."""
    def setUp(self):
        Status.delete_all()

    def test_create(self):
        status = Status(
            description='Pending'
        )
        status.create()
        self.assertEqual(status.description, 'Pending')
        self.assertEqual(status.id, 1)

    def test_find_nonexistent_id(self):
        nonexistent_id = 5
        status_with_id = Status(
            description='Accepted'
        )
        status_with_id.create()
        result = Status.find_by_id(nonexistent_id)
        self.assertEqual(result, None)

    def test_find_existing_id(self):
        existing_id = 1
        status_with_id = Status(
            description='Pending'
        )
        status_with_id.create()
        result = Status.find_by_id(existing_id)
        self.assertEqual(result.id, existing_id)

    def test_find_nonexistent_desc(self):
        nonexistent_description = 'Pending'
        status_with_desc = Status(
            description='Accepted'
        )
        status_with_desc.create()
        result = Status.find_by_description(nonexistent_description)
        self.assertEqual(result, None)

    def test_find_existing_desc(self):
        existing_description = 'Accepted'
        status_with_desc = Status(
            description='Accepted'
        )
        status_with_desc.create()
        result = Status.find_by_description(existing_description)
        self.assertEqual(result.description, existing_description)


if __name__ == '__main__':
    unittest.main()
