import unittest

from boxcar.core import domain_objects


class GeoRectTest(unittest.TestCase):

    def test_create_from_lat_lngs(self):
        self.assertEqual(
            domain_objects.GeoRect.create_from_lat_lngs(1, 2, 3, 4),
            domain_objects.GeoRect(
                domain_objects.Coordinate(1, 2),
                domain_objects.Coordinate(3, 4)
            )
        )

    def test_get_all_points(self):
        geo_rect = domain_objects.GeoRect(
            domain_objects.Coordinate(1, 2),
            domain_objects.Coordinate(3, 4)
        )
        expected_points = [
            domain_objects.Coordinate(1, 2),
            domain_objects.Coordinate(1, 4),
            domain_objects.Coordinate(3, 2),
            domain_objects.Coordinate(3, 4),
        ]
        self.assertSetEqual(
            set(geo_rect.get_all_points()),
            set(expected_points)
        )


if __name__ == '__main__':
    unittest.main()
