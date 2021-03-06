class WKTAdapter(object):

    @classmethod
    def convert_coordinate_to_wkt(cls, coordinate):
        return 'POINT(%s %s)' % (coordinate.lat, coordinate.lng)

    @classmethod
    def convert_geo_rect_to_wkt(cls, geo_rect):
        points = geo_rect.get_all_points()
        points.append(points[0])
        points_string = ''
        for point in points:
            points_string += '%s %s, ' % (point.lat, point.lng)
        points_string = points_string[:-2]
        return 'POLYGON((%s))' % points_string

    @classmethod
    def convert_coordinates_to_linestring(cls, coordinates):
        points_string = ''
        for coordinate in coordinates:
            points_string += '%s %s, ' % (
                coordinate.lat,
                coordinate.lng
            )
        points_string = points_string[:-2]
        return 'LINESTRING(%s)' % points_string
