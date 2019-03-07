"""Unit tests for TimeRange models."""
import unittest

from wayfare.models import TimeRange

# TODO: Test update, delete methods from AbstractModelBase

class TestTimeRange(unittest.TestCase):
    """Tests for the TimeRange model."""
    def setUp(self):
        TimeRange.delete_all()

    def test_create(self):
        timerange = TimeRange(
            description='Morning',
            start_time=12,
            end_time=11
        )
        timerange.create()
        self.assertEqual(timerange.id, 1)
        self.assertEqual(timerange.description, 'Morning')
        self.assertEqual(timerange.start_time, 12)
        self.assertEqual(timerange.end_time, 11)

    def test_find_nonexistent_id(self):
        nonexistent_id = 5
        timerange = TimeRange(
            description='Morning',
            start_time=12,
            end_time=11
        )
        timerange.create()
        result = TimeRange.find_by_id(nonexistent_id)
        self.assertEqual(result, None)

    def test_find_existing_id(self):
        existing_id = 1
        timerange = TimeRange(
            description='Morning',
            start_time=12,
            end_time=11
        )
        timerange.create()
        result = TimeRange.find_by_id(existing_id)
        self.assertEqual(result.id, existing_id)

    def test_find_nonexistent_start_time(self):
        nonexistent_start = 0
        timerange = TimeRange(
            description='Morning',
            start_time=12,
            end_time=11
        )
        timerange.create()
        result = TimeRange.find_by_start_time(nonexistent_start)
        self.assertEqual(result, None)

    def test_find_existing_start_time(self):
        existing_start = 12
        timerange = TimeRange(
            description='Morning',
            start_time=12,
            end_time=11
        )
        timerange.create()
        result = TimeRange.find_by_start_time(existing_start)
        self.assertEqual(result.start_time, existing_start)

    def test_find_nonexistent_end_time(self):
        nonexistent_end = 111
        timerange = TimeRange(
            description='Morning',
            start_time=12,
            end_time=11
        )
        timerange.create()
        result = TimeRange.find_by_end_time(nonexistent_end)
        self.assertEqual(result, None)

    def test_find_existing_end_time(self):
        existing_end = 11
        timerange = TimeRange(
            description='Morning',
            start_time=12,
            end_time=11
        )
        timerange.create()
        result = TimeRange.find_by_end_time(existing_end)
        self.assertEqual(result.end_time, existing_end)

if __name__ == '__main__':
    unittest.main()
