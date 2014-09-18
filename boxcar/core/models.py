from geoalchemy2 import Geometry
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import func
from sqlalchemy import or_
from sqlalchemy.types import DateTime

from boxcar.core import db


class TripModel(db.Base):
    __tablename__ = 'trip'

    id = Column(Integer, primary_key=True)
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
