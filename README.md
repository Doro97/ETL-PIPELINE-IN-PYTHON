# ETL-PIPELINE-IN-PYTHON
The project will involve building a pipeline that automates the process of extracting, transforming and loading data using Python and SQLAlchemy.
This automated ETL pipeline will extract the [zip](data\PPR-2021.zip) file that contains the data and process the transactions in one go. 

## Steps followed
### 1. Extracting the data

### 2. Connecting to the postgresql database using SQLAlchemy
SQLAlchemy is an SQL toolkit that is written in Python. It provides a Pythonic framework that can be used to streamline the workflow and efficiently query the data.

The connection to the database is found on the [base.py](scripts\common\base.py) file.

In order to connect to the postgresql database, you have to create an engine using the connection string. The syntax to creating an engine is:

*create_engine(db+dialect://username:password@database_url:port/database_name)*

where:
* *db* is the database
* *dialect* is the driver that allows SQLAlchemy obtain a connection to postgres


### 3. Creating an SQL table
In order to create an sql table, the Python class is mapped to the sql table. To do this, the following steps are followed:
* Initialize a declarative base to ensure the Python class inherits from it
* Set the table name to map the class with the PostgreSQL table
* Set id to primary key
* Declare the rest of the columns

The Base class the model inherited has the definition of the PprRawAll model in its metadata. Therefore to [create a table](scripts\common\create_tables.py), call the *create_all* function with the engine as an argument.

### 4. Transforming the data

In this step the following will be done: Moving the data from the csv file to a table-this will make it easy to apply transformation on the data using python and SQL and the data cleaning process.

#### Data cleaning
On the [transform.py](scripts\transform.py)  script the following actions would be used to transform the data to the required form: 
1.	Lowercase all the strings in all columns 
2.	Change date format 
3.	Change the price to an integer by:
    * Removing the Euro symbol
    * Removing the comma
    * Converting it to a float 
    * Converting to an integer
4.	Change the description to only show whether a property is new or second hand.












