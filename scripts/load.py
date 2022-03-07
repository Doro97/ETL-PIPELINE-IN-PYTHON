from common.base import session
from common.tables import PprCleanAll,PprRawAll

from sqlalchemy import cast,Integer,Date
from sqlalchemy.dialects.postgresql import insert

def insert_transactions():
    """Insert operation: add new data"""

    # retrieve all the transaction ids from the clean table
    clean_transaction_ids= session.query(PprCleanAll.transaction_id)

    # date_of_sale and price need to be casted as Date and Integer
    transactions_to_insert=session.query(
        cast(PprRawAll.date_of_sale,Date),
        PprRawAll.address,
        PprRawAll.postal_code,
        PprRawAll.county,
        cast(PprRawAll.price,Integer),
        PprRawAll.description,
    ).filter(~PprRawAll.transaction_id.in_(clean_transaction_ids))

    # print the number of transactions to insert
    print("Transactions to insert : ", transactions_to_insert.count())

    # insert the rows from the previously selected transactions
    stm=insert(PprCleanAll).from_select(["date_of_sale","address","postal_code","county","price","description"], transactions_to_insert)

    # execute and commit 
    session.execute(stm)
    session.commit()


def delete_transactions():
    """Delete operation: delete any row not present in the previous table """

    # get all ppr_raw_all transaction_ids
    raw_transaction_ids=session.query(PprRawAll.transaction_id)

    # filter the transactions in ppr_clean_all table that are not in ppr_raw_all table
    transactions_to_delete=session.query(PprCleanAll).filter(~PprCleanAll.transaction_id.in_(raw_transaction_ids))

    # print number to transactions to be deleted
    print("Transactions to delete : ", transactions_to_delete.count())

    # delete
    transactions_to_delete.delete(synchronize_session=False)

    # commit
    session. commit



def main():
    print ("[Load] Start....")
    print ("[Load] Inserting new rows..")
    insert_transactions()
    print ("[Load] Deleting rows not available in the new transformed data")
    delete_transactions()
    print ("[Load] End....")

