import unittest
from boxcar import core


class GeoRectTest(unittest.TestCase):

    def test_create_from_lat_lngs(self):
        self.assertEqual(
            core.GeoRect.create_from_lat_lngs(1, 2, 3, 4),
            core.GeoRect(
                core.Coordinate(1, 2),
                core.Coordinate(3, 4)
            )
        )

    def test_get_all_points(self):
        geo_rect = core.GeoRect(
            core.Coordinate(1, 2),
            core.Coordinate(3, 4)
        )
        expected_points = [
            core.Coordinate(1, 2),
            core.Coordinate(1, 4),
            core.Coordinate(3, 2),
            core.Coordinate(3, 4),
        ]
        self.assertSetEqual(
            set(geo_rect.get_all_points()),
            set(expected_points)
        )


if __name__ == '__main__':
    unittest.main()
