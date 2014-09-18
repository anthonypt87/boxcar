from pymongo import MongoClient, GEO2D, GEOSPHERE
db = MongoClient().trip


class OngoingTripAnalyzer(object):

    def add_trip_event_to_be_analyzed(self, trip_event):
        db.trip.ensure_index([("id", 1)], unique=True)
        db.trip.ensure_index([("path", GEOSPHERE)])
        db.trip.ensure_index([("start_time", 1)])
        ##db.trip.ensure_index([("end_time", 1)])
        db.trip.ensure_index([("start_point", GEOSPHERE)])
        update_status = db.trip.update(
            {'id': trip_event.id},
            {
                '$push': {
                    'path.coordinates': [
                        trip_event.location.lng, trip_event.location.lat
                    ]
                }
            }
        )
        if update_status['updatedExisting']:
            return
        db.trip.insert({
            'id': trip_event.id,
            'path': {
                'type': 'LineString',
                'coordinates': [
                    [trip_event.location.lng, trip_event.location.lat],
                    [trip_event.location.lng, trip_event.location.lat + .00001]
                ]
            },
            'start_time': trip_event.time,
            'end_time': None,
            'fare': 0,
        })

    def get_trips_that_passed_through_geo_rect(self, geo_rect):
        geo_rect_points = [
            (point.lng, point.lat) for point in geo_rect.get_all_points()
        ]

        geo_rect_points.append(geo_rect_points[0])

        k = db.trip.find(
            {
                'path': {
                    '$geoIntersects': {
                        '$geometry': {
                            'type': 'Polygon',
                            'coordinates': [geo_rect_points]
                        }
                    }
                }
            }
        )
        return k.count()
