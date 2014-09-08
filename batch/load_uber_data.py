import argparse
import contextlib
import csv

import dateutil.parser

from boxcar.core import domain_objects
from boxcar.trip_analyzers import linestring_mysql_trip_analyzer


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
        with self._tsv_loader() as loader:
            previous_row_id = None
            rows = []
            for row in loader:
                if previous_row_id is None:
                    previous_row_id = row['id']
                if row['id'] != previous_row_id:
                    self._add_trip_rows(rows)
                    rows = []
                    previous_row_id = row['id']
                else:
                    rows.append(row)
            if rows:
                self._add_trip_rows(rows)

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
            fare=self.DEFAULT_FARE
        )


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Dump uber tsv file to trip analyzer.'
    )
    parser.add_argument('uber_path')
    args = parser.parse_args()

    analyzer = linestring_mysql_trip_analyzer.LinestringMySQLTripAnalyzer()
    tsv_loader = get_tsv_loader(args.uber_path)

    UberDataLoader(analyzer, tsv_loader).load_uber_data()
