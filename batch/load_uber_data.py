import csv
import contextlib
import argparse
import dateutil.parser
from boxcar import core
from boxcar import trip_analyzer
import itertools


def grouper(iterable, n, fillvalue=None):
    args = [iter(iterable)] * n
    return itertools.izip_longest(*args, fillvalue=fillvalue)


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

    def __init__(self, trip_analyzer, tsv_loader):
        self._trip_analyzer = trip_analyzer
        self._tsv_loader = tsv_loader

    def load_uber_data_3(self):
        with self._tsv_loader() as loader:
            for i, group in enumerate(grouper(loader, 10000)):
                trip_events = [
                    self._create_trip_event_from_row(row)
                    for row in group
                ]
                self._trip_analyzer.add_trip_events(trip_events)

    def load_uber_data_2(self):
        with self._tsv_loader() as loader:
            for row in loader:
                trip_event = self._create_trip_event_from_row(row)
                self._trip_analyzer.add_trip_event(trip_event)

    def load_uber_data(self):
        with self._tsv_loader() as loader:
            previous_row_id = None
            rows = []
            for i, row in enumerate(loader):
                if previous_row_id is None:
                    previous_row_id = row['id']
                if row['id'] != previous_row_id:
                    trip_events = [
                        self._create_trip_event_from_row(row_to_add)
                        for row_to_add in rows
                    ]
                    self._trip_analyzer.add_trip_events(trip_events)
                    print i
                    rows = []
                    previous_row_id = None
                else:
                    rows.append(row)

    def _create_trip_event_from_row(self, row):
        return core.TripEvent(
            id=int(row['id']),
            location=core.Coordinate(
                float(row['lat']),
                float(row['lng'])
            ),
            time=dateutil.parser.parse(row['time']),
            type=1,
        )


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Dump uber tsv file to trip analyzer.'
    )
    parser.add_argument('uber_path')
    args = parser.parse_args()

    analyzer = trip_analyzer.InnoDBTripAnalyzer()
    tsv_loader = get_tsv_loader(args.uber_path)

    UberDataLoader(analyzer, tsv_loader).load_uber_data()
