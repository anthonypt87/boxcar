import datetime
from dateutil import tz
import mock
import unittest

from batch import load_uber_data
from boxcar.core import domain_objects


class LoadUberDataTest(unittest.TestCase):

    def test_load_uber_data(self):
        mock_tsv_loader = mock.MagicMock()
        mock_tsv_loader.return_value.__enter__.return_value = [{
            'id': '00001',
            'time': '2007-01-07T10:54:50+00:00',
            'lat': '37.782551',
            'lng': '-122.445368'
        }]
        trip_analyzer = mock.Mock()
        loader = load_uber_data.UberDataLoader(
            trip_analyzer,
            mock_tsv_loader,
        )
        loader.load_uber_data()
        trip_event = domain_objects.TripEvent(
            id=1,
            time=datetime.datetime(2007, 1, 7, 10, 54, 50, tzinfo=tz.tzutc()),
            location=domain_objects.Coordinate(
                37.782551,
                -122.445368
            ),
            # TODO: figure out later
            type=1
        )
        trip_analyzer.add_trip_event.assert_called_once_with(
            trip_event
        )


if __name__ == '__main__':
    unittest.main()
