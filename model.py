import mysql.connector
from mysql.connector import Error


def init_connection ():
    try:
        db_connection = mysql.connector.connect(
            host="localhost", #172.218.153.209
            user="iot_user",
            password="iot_pass",
            database="Gasses"
        )

        return db_connection
    except Error as e:
        print (f"Error initializing connection: {e}")
        return None

def close_connection (db_connection):
    db_connection.close()

# Returns rows. for row in rows
def execute_query (query):
    db_connection = init_connection()
    try:
        cursor = db_connection.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()
        return results
    except Error as e:
        print(f"Error executing query. {e}")
    finally:
        close_connection (db_connection)
    
    return []

# Returns bool for success
def insert_query (query):
    db_connection = init_connection()
    try:
        cursor = db_connection.cursor()
        cursor.execute (query)
        db_connection.commit()
        return True
    except Error as e:
        print (f"Error executing query: {e}")
    finally:
        close_connection(db_connection)
    
    return False