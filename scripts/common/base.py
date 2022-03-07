
# Import the function needed
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.orm import declarative_base


# Create the engine
# the engine is the starting point of SQLAlchemy applications
engine = create_engine("postgresql+psycopg2://postgres:doro19997@localhost:5432/property_transactions")

# Create the session
# the session establishes a connection with the database
session =Session(engine)
Base = declarative_base()
