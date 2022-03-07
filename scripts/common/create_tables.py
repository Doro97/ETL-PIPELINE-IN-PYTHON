from base import Base, engine
# import the PprRawAll table
from tables import PprRawAll,PprCleanAll

# create the table in the database

if __name__ == "__main__":
    Base.metadata.create_all(engine)
    