import datetime
import argparse
import contextlib
import csv

import dateutil.parser

from boxcar.core import domain_objects
#from boxcar.trip_analyzers.postgis_trip_analyzer import PostGISTripAnalyzer
#from boxcar.ongoing_trip_analyzer import OngoingTripAnalyzer
from boxcar.everything_in_memory_analyzer import OngoingTripAnalyzer


def get_tsv_loader(filename):
    @contextlib.contextmanager
    def _inner():
        with open(filename) as csv_file:
            yield csv.DictReader(
                csv_file,
                fieldnames=['id', 'time', 'lat', 'lng'],
                delimiter='\t'
            )
    return _inner


class UberDataLoader(object):

    DEFAULT_FARE = 10

    def __init__(self, trip_analyzer, tsv_loader):
        self._trip_analyzer = trip_analyzer
        self._tsv_loader = tsv_loader

    def load_uber_data(self):
        trip_analyzer = OngoingTripAnalyzer()
        with self._tsv_loader() as loader:
            import cProfile
            cProfile.runctx('self._do_things(trip_analyzer, loader)', globals(), locals())
        georect = domain_objects.GeoRect.create_from_lat_lngs(37.782551 - 1, -122.445368 - 1, 37.782551 + 1, -122.445368 + 1)
        f = lambda: trip_analyzer.get_trips_that_passed_through_geo_rect(georect)
        cProfile.runctx('f()', globals(), locals())
        print 2

    def _do_things(self, trip_analyzer, loader):
        for i, row in enumerate(loader):
            if i == 20000:
                return
            trip_event = self._create_trip_event(row)
            trip_analyzer.add_trip_event_to_be_analyzed(trip_event)

    def load_uber_data_test(self):
        trip_analyzer = OngoingTripAnalyzer()
        with self._tsv_loader() as loader:
            previous_row_id = None
            rows = []
            for i, row in enumerate(loader):
                if i % 500 == 499:
                    return
                trip_event = self._create_trip_event(row)
                trip_analyzer.add_trip_event_to_be_analyzed(trip_event)

        #        if previous_row_id is None:
        #            previous_row_id = row['id']
        #        if row['id'] == previous_row_id:
        #            rows.append(row)
        #        else:
        #            self._add_trip_rows(rows)
        #            rows = []
        #            previous_row_id = row['id']
        #    if rows:
        #        self._add_trip_rows(rows)

    def _create_trip_event(self, row):
        return domain_objects.TripEvent(
            id=row['id'],
            location=domain_objects.Coordinate(float(row['lat']), float(row['lng'])),
            time=datetime.datetime.now(),
            type=None
        )

    def _add_trip_rows(self, rows):
        trip = self._create_trip_from_rows(rows)
        self._trip_analyzer.add_trip(trip)

    def _create_trip_from_rows(self, rows):
        path = [
            domain_objects.Coordinate(
                float(row['lat']),
                float(row['lng'])
            ) for row in rows
        ]
        row_id = rows[0]['id']
        return domain_objects.Trip(
            id=int(row_id),
            path=path,
            start_time=dateutil.parser.parse(rows[0]['time']),
            end_time=dateutil.parser.parse(rows[-1]['time']),
            fare=self.DEFAULT_FARE,
            start_point=path[0],
            end_point=path[-1]
        )


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Dump uber tsv file to trip analyzer.'
    )
    parser.add_argument('uber_path')
    args = parser.parse_args()

    tsv_loader = get_tsv_loader(args.uber_path)

    analyzer = None
    UberDataLoader(analyzer, tsv_loader).load_uber_data()
    import cProfile
#    cProfile.runctx(
#        'UberDataLoader(analyzer, tsv_loader).load_uber_data()',
#        globals(),
#        locals(),
#
#    )
