import mysql.connector

db_conn = mysql.connector.connect(host="localhost", user="openapi",
password="password", database="openapi")

db_cursor = db_conn.cursor()

db_cursor.execute('''
                CREATE TABLE exercise_data
                (id INT NOT NULL AUTO_INCREMENT,
                user_id VARCHAR(250) NOT NULL,
                device_name VARCHAR(250) NOT NULL,
                heart_rate INTEGER NOT NULL,
                date_created VARCHAR(100) NOT NULL,
                recording_id VARCHAR(250) NOT NULL,
                trace_time VARCHAR(100) NOT NULL,
                trace_id VARCHAR(250) NOT NULL,
                CONSTRAINT exercise_data_pk PRIMARY KEY (id))
                ''')

db_cursor.execute('''
                CREATE TABLE user_parameters
                (id INT NOT NULL AUTO_INCREMENT, 
                user_id VARCHAR(250) NOT NULL,
                age INTEGER NOT NULL,
                weight INTEGER NOT NULL,
                device_name VARCHAR(250) NOT NULL,
                exercise VARCHAR(100) NOT NULL,
                reps INTEGER NOT NULL,
                met FLOAT NOT NULL,
                date_created VARCHAR(100) NOT NULL,
                recording_id VARCHAR(250) NOT NULL,
                trace_time VARCHAR(100) NOT NULL,
                trace_id VARCHAR(250) NOT NULL,
                CONSTRAINT user_parameters_pk PRIMARY KEY (id))
                ''')


db_conn.commit()
db_conn.close()