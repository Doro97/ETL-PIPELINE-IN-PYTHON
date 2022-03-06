import os
import tempfile
from zipfile import ZipFile
import csv

# the path
source_path='E:\Data engineering projects\etl-python\ETL-PIPELINE-IN-PYTHON\data\PPR-2021.zip'
raw_path='E:\Data engineering projects\etl-python\ETL-PIPELINE-IN-PYTHON\data\ppr_raw.csv'


def create_folder(path):
    """
    Create a new folder if it doesn't exists
    """
    os.makedirs(os.path.dirname(path), exist_ok=True)

def save_raw_data():
    """saves the raw data from the source"""

    create_folder(raw_path)
    with tempfile.TemporaryDirectory() as dirpath:
        with ZipFile(source_path,"r") as zipfile:
            names_list=zipfile.namelist()
            csv_file_path=zipfile.extract(names_list[0],path=dirpath)
            # open the csv file in read mode 
            with open (csv_file_path, mode='r',encoding="windows-1252") as csv_file:
                reader=csv.DictReader(csv_file)
                # get the first row
                row=next(reader)
                print("[Extract] First row: ", row)

                # open csv in with mode
                with open(raw_path, mode="w",encoding="windows-1252")as csv_file:

                    #rename the field names
                    fieldnames={
                    "Date of Sale (dd/mm/yyyy)":"date_of_sale",
                    "Address":"address",
                    "Postal Code": "postal_code",
                    "County":"county",
                    "Price (€)":"price",
                    "Description of Property":"description",
                    "Property Size Description":"property_size",
                    "Not Full Market Price":"mkt_price",
                    "VAT Exclusive":"vat_exclusive",
                    }

                    writer=csv.DictWriter(csv_file, fieldnames=fieldnames)
                    # write headers as first line
                    writer.writerow(fieldnames)
                    for row in reader:
                        # write all rows in file
                        writer.writerow(row)


# main function 
def main():
    print("[Extract] Start")
    print("[Extract] Saving data from '{source_path}' to '{raw_path}'")
    save_raw_data()
    print(f"[Extract] End")
