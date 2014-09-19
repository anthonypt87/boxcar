import datetime
import unittest

import mock
from dateutil import tz

from batch import load_uber_data
from boxcar.core import domain_objects
from shapely import geometry


class UberDataLoaderTest(unittest.TestCase):

    def test_load_uber_data(self):
        mock_tsv_loader = mock.MagicMock()
        mock_tsv_loader.return_value.__enter__.return_value = [{
            'id': '00001',
            'time': '2007-01-07T10:54:50+00:00',
            'lat': '37.782551',
            'lng': '-122.445368',
            'type': domain_objects.TripEventType.END
        }]
        trip_ingestor = mock.Mock()
        loader = load_uber_data.UberDataLoader(
            trip_ingestor,
            mock_tsv_loader,
        )
        loader.load_uber_data()
        time = datetime.datetime(2007, 1, 7, 10, 54, 50, tzinfo=tz.tzutc())
        point = geometry.Point(37.782551, -122.445368)
        domain_objects.TripEvent(
            id=1,
            time=time,
            point=point,
            fare=load_uber_data.UberDataLoader.DEFAULT_FARE,
            type=domain_objects.TripEventType.END
        )
        trip_ingestor.add_trip_event_to_be_analyzed.assert_has_any_call()


if __name__ == '__main__':
    unittest.main()
