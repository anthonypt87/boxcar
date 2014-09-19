from shapely import geometry

from boxcar.core import redis_client


class OngoingTripAnalyzer(object):

    def __init__(self, ongoing_trip_event_store):
        self._ongoing_trip_event_store = ongoing_trip_event_store

    def add_trip_event_to_be_analyzed(self, trip_event):
        self._ongoing_trip_event_store.append_to_path(
            trip_event.id,
            trip_event.point
        )

    def get_trips_that_passed_through_box(self, box):
        trip_id_path_map = \
            self._ongoing_trip_event_store.get_trip_id_to_paths()

        number_of_intersecting_paths = 0
        for path in trip_id_path_map.values():
            if box.intersects(path):
                number_of_intersecting_paths += 1

        return number_of_intersecting_paths

    def get_trips_started_or_stopped_in_box(self, box):
        id_to_trip_info_map = self._ongoing_trip_event_store.get_all_trip_info(
            box
        )
        # We only handle trips that started in box because ongoing trips by
        # definition don't have an end point.
        num_trips_that_started_in_box = 0
        for trip_info in id_to_trip_info_map.values():
            if box.intersects(trip_info['start_point']):
                num_trips_that_started_in_box += 1

        return num_trips_that_started_in_box

    def get_fares_in_started_or_stopped_in_box(self, box):
        return 0

    def get_get_trips_at_time(self, time):
        return


class OngoingTripEventStore(object):

    def add_trip_info(self, trip_id, start_point, start_time):
        trip_info_key = 'trip:%s' % trip_id
        redis_client.client.hset(
            trip_info_key,
            {
                'start_point': self._serialize_point(start_point)
                'start_time': start_point
            }
        )
        self._add_trip_id(trip_id)

    def _serialize_point(self, point):
        return '%s %s' % (point.x, point.y)

    def _serialize_datetime(self, unserialized):
        return '%s'

    def _add_trip_id(self, trip_id):
        redis_client.client.sadd(self.TRIP_KEY, trip_id)

    def append_to_path(self, trip_id, point):
        path_name = self._get_path_key(trip_id)
        redis_client.client.append(
            path_name,
            '%s ' % (self._serialize_point(point))
        )
        self._add_trip_id(trip_id)

    def _get_path_key(self, trip_id):
        return 'trip:%s:path' % trip_id

    def get_trip_id_to_paths(self):
        trip_ids = self._get_all_trip_ids()

        path_names = [
            self._get_path_key(trip_id) for trip_id in trip_ids
        ]
        raw_path_strings = redis_client.client.mget(path_names)

        trip_id_to_paths = {}
        for trip_id, raw_path_strings in zip(trip_ids, raw_path_strings):
            trip_id_to_paths[trip_id] = self._adapt_raw_points_to_shapes(
                raw_path_strings
            )
        return trip_id_to_paths

    def _get_all_trip_ids(self):
        raw_trip_ids = redis_client.client.smembers('trip')
        return [int(raw_trip_id) for raw_trip_id in raw_trip_ids]

    def _adapt_raw_points_to_shapes(self, raw_points):
        raw_points = raw_points.split(' ')[:-1]
        unpaired_points = [float(raw_point) for raw_point in raw_points]
        paired_points = self._get_chunks(unpaired_points, 2)
        if len(paired_points) == 1:
            return geometry.Point(paired_points[0])
        else:
            return geometry.LineString(paired_points)

    def _get_chunks(self, items, chunk_size):
        if chunk_size < 1:
            chunk_size = 1
        return [
            items[i:i + chunk_size] for i in xrange(0, len(items), chunk_size)
        ]
