
    id = Column(Integer, primary_key=True)
    event_id = Column(Integer)
    path = Column(
        Geometry(geometry_type='LINESTRING', srid=4326, spatial_index=True)
    )
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    start_point = Column(
        Geometry(geometry_type='POINT', srid=4326, spatial_index=True)
    )
    end_point = Column(
        Geometry(geometry_type='POINT', srid=4326, spatial_index=True)
    )
    fare = Column(Integer)

trip:event_id:trip_data - {'start_time': .., 'end_time': ..., 'start_point': ..., 'end_point': ..., 'fare': ...}
trip:event_id:path
trip:event_id:



class TripAnalyzer(object):

    def add_trip_event(self, trip_event):
        pass

    def get_trips_that_passed_through_geo_rect(self, geo_rect):
        pass

    def get_trips_started_or_stopped_in_geo_rect(self, geo_rect):
        pass

    def get_fares_in_started_or_stopped_in_geo_rect(self, geo_rect):
        pass

    def get_trips_during_time(self, time):
        pass


class TripAnalyzer(object):

    def add_trip_event_to_be_analyzed(self, trip_event):
        start_transaction
        # NOTE: ... Possible off by one. when ending trips and asking. can be
        # fixed by using transactions. Also since we don't have transactions
        # actually becomes a problem.
        if event is done:
            event_info = get_trip_info()
            try:
                add trip row
                delete info row
            except:
                pass

        if event is begin:
            ongoing.add
        elif event is update:
            ongoing.append

    def get_trips_that_passed_through_geo_rect(self, geo_rect):
        sum

    def get_trips_started_or_stopped_in_geo_rect(self, geo_rect):
        sum

    def get_fares_in_started_or_stopped_in_geo_rect(self, geo_rect):
        sum

    def get_trips_during_time(self, time):
        sum


def for all active trips:





Display
    MAP
        restart <wipe everything>
        dump uber TSV <> - test query performance
            get_trips_that_passed_through_geo_rect
            get_trips_started_or_stopped_in_geo_rect
            get_fares_in_started_or_stopped_in_geo_rect
            get_trips_during_time

            TIME_TO_INSERT x trip events and X trips
            TRIP_TIME_RANGE
            how many trips at time

        replay - test insertion speed and live updates with incoming data
            uber_dump live
                start pause
                highlight box
            how many trips at time
            how many trips currently

MEGALOAD TESTING
    DUMPS TON OF DATA (months amount)
    test query performance - 5 queries



