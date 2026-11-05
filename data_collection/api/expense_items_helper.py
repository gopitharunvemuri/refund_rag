from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
from data_collection.api.used_functions import load_csv_and_insert_items

load_dotenv()
from Objects_mappings.Employee import Base
def set_up_connection(url: str):
    engine = create_engine(
        url = url,
        pool_pre_ping=True
    )

    Base.metadata.create_all(engine)
    print("Table created in the db")

def insert_records():
    csv_path = "./data/expense_items.csv"
    load_csv_and_insert_items(csv_path)
    print("loaded sucessfully")
url = os.getenv("DATABASE_URL")
set_up_connection(url=url)
insert_records()