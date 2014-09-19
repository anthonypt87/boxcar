from geoalchemy2 import Geometry
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import func
from sqlalchemy import or_
from sqlalchemy.types import DateTime

from boxcar.core import db


def create_geometry_column(geometry_type):
    return Column(
        Geometry(geometry_type=geometry_type, srid=4326, spatial_index=True)
    )


class TripModel(db.Base):

    __tablename__ = 'trip'

    id = Column(Integer, primary_key=True)
    path = create_geometry_column('LINESTRING')
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    start_point = create_geometry_column('POINT')
    end_point = create_geometry_column('POINT')
    fare = Column(Integer)
