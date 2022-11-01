import mysql.connector

db_conn = mysql.connector.connect(host="localhost", user="openapi",

password="password", database="openapi")
db_cursor = db_conn.cursor()

db_cursor.execute('''
                    DROP TABLE user_parameters , exercise_data
                    ''')
db_conn.commit()
db_conn.close()