import datetime
from dateutil import tz
import mock
import unittest

from batch import load_uber_data
from boxcar.core import domain_objects


class UberDataLoaderTest(unittest.TestCase):

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
        time = datetime.datetime(2007, 1, 7, 10, 54, 50, tzinfo=tz.tzutc())
        coordinate = domain_objects.Coordinate(37.782551, -122.445368)
        trip = domain_objects.Trip(
            id=1,
            start_time=time,
            end_time=time,
            path=[coordinate],
            fare=load_uber_data.UberDataLoader.DEFAULT_FARE,
            start_point=coordinate,
            end_point=coordinate
        )
        trip_analyzer.add_trip.assert_called_once_with(trip)

    def test_load_two_datas(self):
        pass


if __name__ == '__main__':
    unittest.main()
