CREATE_TABLE_QUERY = """
CREATE TABLE region(
   id_region INT,
   region_name VARCHAR(50) NOT NULL,
   PRIMARY KEY(id_region)
);

CREATE TABLE sex(
   id_sex INT,
   sex_label VARCHAR(50) NOT NULL,
   PRIMARY KEY(id_sex)
);

CREATE TABLE smoker(
   id_smoker INT,
   is_smoker VARCHAR(3) NOT NULL,
   PRIMARY KEY(id_smoker)
);

CREATE TABLE user_role(
   id_role INT,
   role_name VARCHAR(50) NOT NULL,
   PRIMARY KEY(id_role),
   UNIQUE(role_name)
);

CREATE TABLE patient(
   id_patient INT,
   last_name VARCHAR(50) NOT NULL,
   first_name VARCHAR(50) NOT NULL,
   age INT NOT NULL,
   bmi DECIMAL(6,3) NOT NULL,
   patient_email VARCHAR(50) NOT NULL,
   children INT NOT NULL,
   charges DECIMAL(15,5) NOT NULL,
   id_smoker INT NOT NULL,
   id_sex INT NOT NULL,
   id_region INT NOT NULL,
   PRIMARY KEY(id_patient),
   UNIQUE(patient_email),
   FOREIGN KEY(id_smoker) REFERENCES smoker(id_smoker),
   FOREIGN KEY(id_sex) REFERENCES sex(id_sex),
   FOREIGN KEY(id_region) REFERENCES region(id_region)
);

CREATE TABLE app_user(
   id_user INT,
   username VARCHAR(50) NOT NULL,
   password VARCHAR(50) NOT NULL,
   user_email VARCHAR(50) NOT NULL,
   id_role INT NOT NULL,
   PRIMARY KEY(id_user),
   UNIQUE(username),
   UNIQUE(user_email),
   FOREIGN KEY(id_role) REFERENCES user_role(id_role)
);
"""