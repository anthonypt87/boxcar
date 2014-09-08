from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.dialects.mysql import TINYINT
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, DateTime

# HACKS
import sqlalchemy
sqlalchemy.sql.expression.Function = sqlalchemy.sql.functions.Function
sqlalchemy.orm.properties.ColumnProperty.ColumnComparator = sqlalchemy.orm.properties.ColumnProperty.Comparator
import geoalchemy
old_column_collection = geoalchemy.geometry.expression.ColumnCollection


def new_column_collection_creator(*args):
    collection = old_column_collection()
    for arg in args:
        collection.add(arg)
    return collection
geoalchemy.geometry.expression.ColumnCollection = new_column_collection_creator


from geoalchemy import GeometryColumn
from geoalchemy import Point
from geoalchemy import LineString
from geoalchemy import mysql
from geoalchemy import GeometryDDL



engine = create_engine('mysql://root@localhost/boxcar')
Base = declarative_base()


class TripEvent(Base):
    __tablename__ = 'trip_event'
    __table_args__ = {'mysql_engine': 'MyISAM'}
    id = Column(Integer, primary_key=True)
    event_id = Column(Integer)
    coordinate = GeometryColumn(
        Point(2),
        comparator=mysql.MySQLComparator
    )
    time = Column(DateTime)
    type = Column(TINYINT(2), default=0)


class WholeTrip(Base):
    __tablename__ = 'whole_trip'
    __table_args__ = {'mysql_engine': 'MyISAM'}
    id = Column(Integer, primary_key=True)
    event_id = Column(Integer)
    path = GeometryColumn(
        LineString,
        comparator=mysql.MySQLComparator
    )


GeometryDDL(TripEvent.__table__)

#Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
