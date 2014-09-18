from shapely import geometry


def get_merged_path(path, point):
    return geometry.LineString(path.coords[:] + point.coords[:])
