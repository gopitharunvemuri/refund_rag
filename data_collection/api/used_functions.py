import pandas as pd
from datetime import date
from Objects_mappings.Employee import Employee
from Objects_mappings.Expense_claim import ExpenseClaim
from Objects_mappings.Expense_items import ExpenseItem
from sqlalchemy import create_engine, insert
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os 
from Exceptions.Exceptions import CustomExcpetion

load_dotenv()

def get_session():
    url = os.getenv("DATABASE_URL")
    engine = create_engine(
        url = url,
        pool_pre_ping=True
    )
    Session = sessionmaker(
        bind = engine
    )
    return Session()

def load_csv_and_insert_employees(csv_path: str, classname: str):
    dataset = pd.read_csv(csv_path)
    dataset["join_date"] = pd.to_datetime(
        dataset["join_date"], errors = "coerce"
    ).dt.date
    session = get_session()
    try:
        for i in range(len(dataset)):
            data = dataset.iloc[i,:].to_dict()
            session.execute(insert(Employee), data)
        session.commit()
    except CustomExcpetion as e:
        session.rollback()
    finally:
        session.close()

def load_csv_and_insert_claims(csv_path: str):
    dataset = pd.read_csv(csv_path)
    date_columns = ["payment_date", "approval_date", "claim_date", "trip_start", "trip_end"]
    for i in date_columns:
        dataset[i] = pd.to_datetime(
            dataset[i], errors = "coerce"
        ).dt.date
    float_columns = ["total_amount", "approved_amount"]
    for i in float_columns:
        dataset[i] = pd.to_numeric(
            dataset[i], errors = "coerce"
        )
    dataset = dataset.astype(object).where(
        pd.notna(dataset), None
    )
    session = get_session()
    try:
        for i in range(len(dataset)):
            data = dataset.iloc[i,:].to_dict()
            session.execute(insert(ExpenseClaim), data)
        session.commit()
    except CustomExcpetion as e:
        session.rollback()
    finally:
        session.close()

def load_csv_and_insert_items(csv_path: str):
    dataset = pd.read_csv(csv_path)
    date_columns = ["item_date"]
    for i in date_columns:
        dataset[i] = pd.to_datetime(
            dataset[i], errors = "coerce"
        ).dt.date
    float_columns = ["amount", "policy_limit"]
    for i in float_columns:
        dataset[i] = pd.to_numeric(
            dataset[i], errors = "coerce"
        )
    dataset = dataset.astype(object).where(
        pd.notna(dataset), None
    )
    session = get_session()
    try:
        for i in range(len(dataset)):
            data = dataset.iloc[i,:].to_dict()
            session.execute(insert(ExpenseItem), data)
        session.commit()
    except CustomExcpetion as e:
        session.rollback()
    finally:
        session.close()
