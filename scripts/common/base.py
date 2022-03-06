
# Import the function needed
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.orm import declarative_base


# Create the engine
# the engine is the starting point of SQLAlchemy applications
engine = create_engine("postgresql+psycopg2://usr:pwd@localhost:5432/mydatabase")

# Create the session
# the session establishes a connection with the database
session =Session(engine)
Base = declarative_base()
