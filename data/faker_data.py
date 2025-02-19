import pandas as pd
from faker import Faker
import hashlib
import random

try:
    df_insurance = pd.read_csv("data\insurance.csv")  # Loading insurance dataset
except Exception:
    print("An error occurred during the dataset loading")

fake = Faker()

def faker_insurance():
    """
    Generates fake data for new columns in the insurance dataset
    """
    df_insurance["first_name"] = [hashlib.sha256((fake.first_name()).encode()).hexdigest() for _ in range(len(df_insurance))]
    df_insurance["last_name"] = [hashlib.sha256((fake.last_name()).encode()).hexdigest() for _ in range(len(df_insurance))]
    df_insurance["patient_email"] = [hashlib.sha256((fake.email()).encode()).hexdigest() for _ in range(len(df_insurance))]

    df_insurance.to_csv("data\insurance_enriched.csv", index=False) # Saving back to CSV

    print(df_insurance.head()) # Just to check if faker worked properly

def faker_user():
    """
    Creates an app user table and generates fake data to fill it
    """
    df_user = pd.DataFrame()
    df_user["username"] = [fake.user_name() for _ in range(10)]
    df_user["password"] = [hashlib.sha256((fake.password()).encode()).hexdigest() for _ in range(10)]
    df_user["user_email"] = [fake.password() for _ in range(10)]
    df_user["role_name"] = [random.choice(["admin", "medic", "patient"]) for _ in range(10)]

    df_user.to_csv("data/app_user.csv", index=False) # Saving to CSV

    print(df_user.head()) # Just to check if faker worked properly

faker_insurance()
faker_user()
