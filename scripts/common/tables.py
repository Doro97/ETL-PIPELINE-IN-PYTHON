from sqlalchemy import cast, Column,Integer,String,Date
from sqlalchemy.orm import column_property
from common.base import Base


class PprRawAll(Base):
    __tablename__="ppr_raw_all"

    id=Column(Integer, primary_key=True)
    date_of_sale=Column(String(55))
    address=Column(String(255))
    postal_code=Column(String(55))
    county=Column(String(55))
    price=Column(String(55))
    descriptiom=Column(String(55))
    # add a uniqueness constraint by concatenating the columns
    # transaction_id=column_property(date_of_sale+"_"+address+"_"+county+"_"+price)
    
