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

conn = sqlite3.connect("data/db_insurance.db", detect_types=sqlite3.PARSE_DECLTYPES) # Creating database if not exist
cursor = conn.cursor() # Creating a cursor


def db_tables_creation():
    """
    Creates the database's tables.
    """
    try:
        # Creating tables in database
        cursor.executescript(sql_requests.CREATE_TABLE_QUERY)
        conn.commit()

    except sqlite3.OperationalError:
        print("Error during database creation.")


def create_df_unique(df_input, col_list, id_pk):
    """
    Creating a dataframe corresponding to a specific table WITHOUT FKs.

    Parameters:
        df_input: the dataframe from which to extract data
        col_list: the list of column names needed
        id_pk: the name of the id column to add (for PK)

    Return:
        df_output: the dataframe corresponding to the specified table
    """
    df_output = df_input[col_list].drop_duplicates().reset_index(drop=True)
    df_output.insert(0, id_pk, range(0, len(df_output)))

    return df_output


def create_df_foreign(df_main, df_foreign_list, col_list, id_pk, merge_col_list):
    """
    Creating a dataframe corresponding to a specific table WITH FKs.

    Parameters:
        df_main: the main dataframe from which to extract data
        df_foreign_list: list of dataframes to which the output df is connected by FK
        col_list: the list of column names needed
        id_pk: the name of the id column to add (for PK)
        merge_col_list: list of columns on which to merge 2 linked dataframes
    
    Return:
        df_output: the dataframe corresponding to the specified table
    """
    df_output = df_main.copy()

    for i, merge_col in enumerate(merge_col_list):
        df_output = df_output.merge(df_foreign_list[i], on=merge_col, how="left")

    df_output = df_output[col_list]
    df_output.insert(0, id_pk, range(0, len(df_output)))

    return df_output


def renaming_columns(df, col_list, new_col_names):
    """
    Renames the columns of a dataframe.

    Parameters:
        df: the dataframe in which to change the columns names
        col_list: the list of the old columns names
        new_col_names: the list the new columns names
    """
    if new_col_names != "" and len(new_col_names) == len(col_list):
        for i, name in enumerate(col_list):
            df.rename(columns={name: new_col_names[i]}, inplace=True)


def insert_data_to_db(df, table_name):
    """
    Inserts data from a dataframe into one of the database's tables.

    Parameters:
        df: the dataframe from where to extract the data
        table_name: the database's table in which to insert the extracted data
    """
    try:
        conn.execute("PRAGMA foreign_keys = ON;")
        df.to_sql(table_name, conn, if_exists="append", index=False)
    except sqlite3.OperationalError:
        print("Error during data insertion into table.")


# Creating database's tables
db_tables_creation()

# Creating dataframes corresponding to tables without FKs
df_smoker = create_df_unique(df_insurance, ["smoker"], "id_smoker")
df_sex = create_df_unique(df_insurance, ["sex"], "id_sex")
df_region = create_df_unique(df_insurance, ["region"], "id_region")

df_role = create_df_unique(df_app_user, ["role_name"], "id_role")

# Creating the dataframe corresponding to the patient table
patient_col_list = ["last_name", "first_name", "age", "bmi", "patient_email", "children", "charges", "id_smoker", "id_sex", "id_region"]
df_foreign_list = [df_smoker, df_sex, df_region]
merge_col_list = ["smoker", "sex", "region"]
df_patient = create_df_foreign(df_insurance, df_foreign_list, patient_col_list, "id_patient", merge_col_list)

# Creating the dataframe corresponding to the app_user table
app_user_col_list = ["username", "password", "user_email", "id_role"]
df_user = create_df_foreign(df_app_user, [df_role], app_user_col_list, "id_user", ["role_name"])

# Renaming columns to adapt to columns names in some tables
renaming_columns(df_smoker, ["smoker"], ["is_smoker"])
renaming_columns(df_sex, ["sex"], ["sex_label"])
renaming_columns(df_region, ["region"], ["region_name"])

# Inserting data from dataframes into the corresponding tables in database
insert_data_to_db(df_smoker, "smoker")
insert_data_to_db(df_sex, "sex")
insert_data_to_db(df_region, "region")
insert_data_to_db(df_patient, "patient")

insert_data_to_db(df_role, "user_role")
insert_data_to_db(df_user, "app_user")

conn.close()
