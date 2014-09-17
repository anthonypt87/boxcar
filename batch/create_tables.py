from boxcar.core import db
import boxcar.trip_analyzers.postgis_trip_analyzer
import boxcar.ongoing_trip_analyzer


db.Base.metadata.create_all(db.engine)
db.PostgresBase.metadata.drop_all(db.psql_engine)
db.PostgresBase.metadata.create_all(db.psql_engine)
