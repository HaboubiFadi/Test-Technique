
"""
Purpose:
* Serves as the foundational setup for database interaction using SQLAlchemy.

* Implements session handling and schema initialization.
"""



from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine_string='postgresql://admin:admin@postgres:5432/postgres' #  Contains the credentials and database details.
engine = create_engine(engine_string, echo=True) # Establishes the connection to the PostgreSQL database. 

_Session = sessionmaker(bind=engine) # Session for database manipulation

Base = declarative_base()  # Acts as a base class for all ORM models .
def session_factory(drop_tables):
    if drop_tables: 
        Base.metadata.drop_all(engine) # if drop_table is true drop all the mapped tables that been detected by the engine
    Base.metadata.create_all(engine) # Map all entites to the database 
    return _Session(),engine # Return session objects to perform database operations

    