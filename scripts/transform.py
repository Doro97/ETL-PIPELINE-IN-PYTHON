import os
import csv
from datetime import datetime
from sqlalchemy import text

from common.tables import PprRawAll
from common.base import session


# raw path to extract the data
raw_path ="E:\Data engineering projects\etl-python\ETL-PIPELINE-IN-PYTHON\data\ppr_raw.csv"

def transform_case(input_string):
    """Convert all the strings to lowercase"""
    return input_string.lower()



def update_date(date_input):
    """Convert the date format from DD/MM/YYYY to YYYY-MM-DD"""
    current_format=datetime.strptime(date_input,"%d/%m/%Y")
    new_format=current_format.strftime("%Y-%m-%d")

    return new_format

def update_description(description_input):
    """
    Simplify the property description field to show
    whether a property is 'new' or 'second-hand'
    -"new" if a string contains 'new' substring
    -"second-hand" if a string contains 'second-hand' substring
    """
    description_input=transform_case(description_input)
    if "new" in description_input:
        return "new"
    elif "second-hand" in description_input:
        return "second-hand"

    return description_input

def update_price(price_input):
    """
    Returns the price as integer by :
    - removing the Euro symbol
    - converting it to a floating
    - removing the commas 
    """  

    price_input=price_input.replace("€", "")
    price_input=float(price_input.replace(",",""))
    return int(price_input)


def truncate_table():
    """
    Ensure that the table is always in an empty state
    before running any transformations.
    And the primary-key(id) always restarts from 1 
    """
    session.execute(text("TRUNCATE TABLE ppr_raw_all; ALTER SEQUENCE ppr_raw_all_id_seq RESTART;"))
    session.commit()


def transform_new_data():
    """Apply transformations for each roe in the csv file before saving it to the database"""
    with open (raw_path, mode="r", encoding="windows-1252") as csv_file:
        # read the csv file
        reader=csv.DictReader(csv_file)
        # initialize an empty list for all the PprRawAll objects
        ppr_raw_objects=[]
        for row in reader:
            # apply all the transformations and save as PprRawAll objects
            ppr_raw_objects.append(
                PprRawAll(
                    date_of_sale=update_date(row["date_of_sale"]),
                    address=transform_case(row["address"]),
                    postal_code=transform_case(row["postal_code"]),
                    county=transform_case(row["county"]),
                    price=update_price(row["price"]),
                    # description=update_description(row["description"]),
                )
            )

            # save all new processed objects and commit
            session.bulk_save_objects(ppr_raw_objects)



def main():
    print ("[Transform] Start...")
    print ("[Transform] Remove any old data from the table....")
    truncate_table()
    print ("[Transform] Transform the new data available....")
    transform_new_data()
    print ("[Transform] End....")
