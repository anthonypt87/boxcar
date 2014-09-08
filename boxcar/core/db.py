from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


Base = declarative_base()


engine = create_engine('mysql://root@localhost/boxcar')
Session = sessionmaker(bind=engine)

def patch_geoalchemy():
    import sqlalchemy
    sqlalchemy.sql.expression.Function = sqlalchemy.sql.functions.Function
    sqlalchemy.orm.properties.ColumnProperty.ColumnComparator = \
        sqlalchemy.orm.properties.ColumnProperty.Comparator
    import geoalchemy
    old_column_collection = geoalchemy.geometry.expression.ColumnCollection

    def new_column_collection_creator(*args):
        collection = old_column_collection()
        for arg in args:
            collection.add(arg)
        return collection
    geoalchemy.geometry.expression.ColumnCollection = \
        new_column_collection_creator


patch_geoalchemy()
