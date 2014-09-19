class OngoingTripAnalyzer(object):

    def __init__(self, ongoing_trip_store):
        self._ongoing_trip_store = ongoing_trip_store

    def get_trips_that_passed_through_box(self, box):
        trip_id_path_map = \
            self._ongoing_trip_store.get_trip_id_to_paths()

        number_of_intersecting_paths = 0
        for path in trip_id_path_map.values():
            if box.intersects(path):
                number_of_intersecting_paths += 1

        return number_of_intersecting_paths

    def get_trips_started_or_stopped_in_box(self, box):
        id_to_trip_info_map = \
            self._ongoing_trip_store.get_all_trip_info()
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
