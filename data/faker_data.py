import pandas as pd
from faker import Faker
from cryptography.fernet import Fernet
import random

try:
    df_insurance = pd.read_csv("data\insurance.csv")  # Loading insurance dataset
except Exception:
    print("An error occurred during the dataset loading")

fake = Faker()

# Generating a key for encryption
key = Fernet.generate_key()
fernet = Fernet(key)

key_str = key.decode()
print(f"Fernet key: {key_str}")

def faker_insurance():
    """
    Generates fake data for new columns in the insurance dataset
    """
    df_insurance["first_name"] = [fernet.encrypt((fake.first_name()).encode()) for _ in range(len(df_insurance))]
    df_insurance["last_name"] = [fernet.encrypt((fake.last_name()).encode()) for _ in range(len(df_insurance))]
    df_insurance["patient_email"] = [fernet.encrypt((fake.unique.email()).encode()) for _ in range(len(df_insurance))]

    df_insurance.to_csv("data\insurance_enriched.csv", index=False) # Saving back to CSV

    print(df_insurance.head()) # Just to check if faker worked properly

def faker_user():
    """
    Creates an app user table and generates fake data to fill it
    """
    df_user = pd.DataFrame()
    df_user["username"] = [fake.unique.user_name() for _ in range(10)]
    df_user["password"] = [fernet.encrypt((fake.password()).encode()) for _ in range(10)]
    df_user["user_email"] = [fake.unique.email() for _ in range(10)]
    df_user["role_name"] = [random.choice(["admin", "medic", "patient"]) for _ in range(10)]

    df_user.to_csv("data/app_user.csv", index=False) # Saving to CSV

    print(df_user.head()) # Just to check if faker worked properly

faker_insurance()
faker_user()

print(fernet.decrypt(df_insurance['patient_email'][0]).decode())
