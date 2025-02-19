import sqlite3
import pandas as pd
import sql_requests

# Loading datasets
try:
    df_insurance = pd.read_csv("data/insurance_enriched.csv")
except Exception:
    print("Error during insurance dataset loading.")

try:
    df_app_user = pd.read_csv("data/app_user.csv")
except Exception:
    print("Error during user dataset loading.")


def data_split(df, col):
    """
    Creates a new dataframe from one or multiple columns of a dataframe.

    Parameters:
        df: the dataframe from which to extract column(s)
        col: the column name or list of column names to extract

    Return:
        a dataframe containing only the extracted column(s)
    """
    return df[col]


def insert_id_in_df(df, id):
    """
    Creates an ID column in a dataframe and fills it with an auto-incrementation.

    Parameters:
        df: the dataframe in which to insert and fill the ID column
        id: the name of the id column (must match with the name in the corresponding table)
    """
    df[id] = range(0, len(df))

conn = sqlite3.connect("data/db_insurance.db") # Creating database if not exist
cursor = conn.cursor() # Creating a cursor


def db_creation():
    """
    Creates the database.
    """
    try:
        # Creating tables in database
        cursor.execute(sql_requests.CREATE_TABLE_QUERY)
        conn.commit()

    except Exception:
        print("Error during database creation.")


def insert_data_to_db(df, table_name):
    """
    Inserts data from a dataframe into one of the database's tables.

    Parameters:
        df: the dataframe from where to extract the data
        table_name: the database's table in which to insert the extracted data
    """
    try:
        df.to_sql(table_name, conn, if_exists="append", index=False)
    except Exception:
        print("Error during data insertion into table.")

# Dataframes corresponding to the database's tables
df_patient = data_split(df_insurance, ["age", "bmi", "children", "charges", "first_name", "last_name", "patient_email"])
df_region = data_split(df_insurance, "region")
df_sex = data_split(df_insurance, "sex")
df_smoker = data_split(df_insurance, "smoker")

df_user = data_split(df_app_user, ["username", "password", "user_email"])
df_role = data_split(df_app_user, "role_name")

# Creating the id column for each dataframe, based on the index

insert_id_in_df(df_patient, "id_patient")
insert_id_in_df(df_region, "id_region")
insert_id_in_df(df_sex, "id_sex")
insert_id_in_df(df_smoker, "id_smoker")

insert_id_in_df(df_user, "id_user")
insert_id_in_df(df_role, "id_role")

# Creating database
db_creation()

# Inserting data into the database's tables
insert_data_to_db(df_patient, "patient")
insert_data_to_db(df_region, "region")
insert_data_to_db(df_sex, "sex")
insert_data_to_db(df_smoker, "smoker")

insert_data_to_db(df_user, "user")
insert_data_to_db(df_role, "role")

conn.close()
