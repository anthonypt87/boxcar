from geoalchemy2 import WKTElement
from shapely import geometry


def get_merged_path(path, point):
    return geometry.LineString(path.coords[:] + point.coords[:])


def convert_shape_to_wkt_element(shape):
    return WKTElement(shape.wkt, srid=4326)
