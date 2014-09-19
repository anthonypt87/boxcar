import contextlib

from sqlalchemy import create_engine
from sqlalchemy import MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


metadata = MetaData()
Base = declarative_base(metadata=metadata)

engine = create_engine('postgresql://anthony@localhost/anthony')
Session = sessionmaker(bind=engine)



@contextlib.contextmanager
def session_manager():
    try:
        session = Session()
        yield session
    except Exception:
        session.rollback()
        raise
    else:
        session.commit()
