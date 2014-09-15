import unittest

from boxcar.core.adapters import WKTAdapter
from boxcar.core import data_models


class WKTAdapterTest(unittest.TestCase):

    def test_convert_coordinate_to_wkt(self):
        lat = 37.782551
        lng = -122.445368
        coordinate = data_models.Coordinate(lat, lng)
        self.assertEqual(
            WKTAdapter.convert_coordinate_to_wkt(coordinate),
            'POINT(%s %s)' % (lat, lng)
        )

    def test_convert_geo_rect_to_wkt(self):
        rect = data_models.GeoRect.create_from_lat_lngs(
            1.01, 2.02, -3.03, -4.04
        )
        self.assertEqual(
            WKTAdapter.convert_geo_rect_to_wkt(rect),
            'POLYGON((1.01 2.02, 1.01 -4.04, -3.03 '
            '2.02, -3.03 -4.04, 1.01 2.02))'
        )

    def test_convert_coordinates_to_linestring(self):
        coordinates = [
            data_models.Coordinate(1, 2),
            data_models.Coordinate(3, 4)
        ]
        self.assertEqual(
            WKTAdapter.convert_coordinates_to_linestring(
                coordinates
            ),
            'LINESTRING(1 2, 3 4)'
        )


if __name__ == '__main__':
    unittest.main()
