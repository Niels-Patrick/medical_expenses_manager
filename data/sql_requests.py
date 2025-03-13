CREATE_TABLE_QUERY = """
CREATE TABLE region(
   id_region INTEGER PRIMARY KEY AUTOINCREMENT,
   region_name TEXT NOT NULL
);

CREATE TABLE sex(
   id_sex INTEGER PRIMARY KEY AUTOINCREMENT,
   sex_label TEXT NOT NULL
);

CREATE TABLE smoker(
   id_smoker INTEGER PRIMARY KEY AUTOINCREMENT,
   is_smoker TEXT NOT NULL
);

CREATE TABLE user_role(
   id_role INTEGER PRIMARY KEY AUTOINCREMENT,
   role_name TEXT NOT NULL UNIQUE
);

CREATE TABLE patient(
   id_patient INTEGER PRIMARY KEY AUTOINCREMENT,
   last_name TEXT NOT NULL,
   first_name TEXT NOT NULL,
   age INTEGER NOT NULL,
   bmi REAL NOT NULL,
   patient_email TEXT NOT NULL UNIQUE,
   children INTEGER NOT NULL,
   charges REAL NOT NULL,
   id_smoker INTEGER NOT NULL,
   id_sex INTEGER NOT NULL,
   id_region INTEGER NOT NULL,
   FOREIGN KEY(id_smoker) REFERENCES smoker(id_smoker),
   FOREIGN KEY(id_sex) REFERENCES sex(id_sex),
   FOREIGN KEY(id_region) REFERENCES region(id_region)
);

CREATE TABLE app_user(
   id_user INTEGER PRIMARY KEY AUTOINCREMENT,
   username TEXT NOT NULL UNIQUE,
   password TEXT NOT NULL,
   user_email TEXT NOT NULL UNIQUE,
   id_role INTEGER NOT NULL,
   FOREIGN KEY(id_role) REFERENCES user_role(id_role)
);
"""