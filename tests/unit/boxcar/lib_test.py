import unittest

from shapely import geometry

from boxcar import lib
from tests import util


class GetMergedPathTest(unittest.TestCase):

    def test_get_merged_path(self):
        point = geometry.Point(1, 2)
        path = geometry.LineString([(3, 4), (5, 6)])

        util.assert_shapes_are_equal(
            self,
            geometry.LineString([(3, 4), (5, 6), (1, 2)]),
            lib.get_merged_path(path, point)
        )


if __name__ == '__main__':
    unittest.main()
