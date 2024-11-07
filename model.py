import mysql.connector
from mysql.connector import Error
from enum import Enum
from datetime import datetime
from datetime import timedelta
import random

class GasType (Enum):
    air_quality = 1
    alcohol = 2
    butane = 3
    carbon_monoxide = 4
    cng = 5
    ethanol = 6
    flammable_gasses = 7
    hydrogen = 8
    lpg = 9
    methane = 10
    natural_gas = 11
    smoke = 12

class TimePeriod (Enum):
    minute = 1
    hour = 2
    day = 3
    week = 4

def init_connection ():
    try:
        db_connection = mysql.connector.connect(
            host="localhost", #172.218.153.209
            user="iot_user",
            password="iot_pass",
            database="iot_project"
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

def get_gas (gas_index):
    if (isinstance (gas_index, int)):
        gas = GasType (gas_index)
    elif (isinstance (gas_index, GasType)):
        gas = gas_index
    else:
        raise ValueError(f"get_gas(), type {type(gas_index)} is not supported. Use either int or GasType enum.")

    query = f"SELECT `{gas.name}` FROM Gasses WHERE `{gas.name}` IS NOT NULL ORDER BY id DESC LIMIT 1"

    result = execute_query (query)

    return result[0][0]

"""
    Input type: Array of GasType (Enum)
"""
def get_gasses_over_time (gasses, time_period: TimePeriod, interval: int):
    end_time = datetime.now()
    
    if isinstance (time_period, TimePeriod):
        time_period_value = time_period
    elif isinstance (time_period, int):
        time_period_value = TimePeriod (time_period)
    else:
        raise ValueError (f"get_gasses_over_time(), value {time_period} {type(time_period)} not supported. Should be of type: TimePeriod.")
    
    if time_period_value == TimePeriod.minute:
        start_time = end_time - timedelta(minutes=interval)
    elif time_period_value == TimePeriod.hour:
        start_time = end_time - timedelta(hours=interval)
    elif time_period_value == TimePeriod.day:
        start_time = end_time - timedelta(days=interval)
    elif time_period_value == TimePeriod.week:
        start_time = end_time - timedelta(weeks=interval)
    else:
        raise ValueError (f"get_gasses_over_time(), value {time_period} {type(time_period)} not supported. Should be of type: TimePeriod.")        
    
    gasses_string = ""
    for gas in gasses:
        if isinstance (gas, GasType):
            gasses_string += f"AVG({gas.name}),"
        elif isinstance (gas, int):
            gasses_string += f"AVG({GasType (gas).name}),"           
        else:
            raise ValueError (f"get_gasses_over_time(), value {gas} ({type(gas)}) not supported. Use either int or GasType enum.")
    query = f"""
        SELECT
            {gasses_string}
            {time_period_value.name.upper()}(datetime) AS {time_period_value.name}
        FROM
            Gasses
        WHERE
            datetime >= '{start_time.replace(microsecond=0)}' AND datetime <= '{end_time.replace(microsecond=0)}'
        GROUP BY 
            {time_period_value.name.upper()}(datetime)
        ORDER BY 
            {time_period_value.name} DESC
        LIMIT {interval};
    """
    results = execute_query (query)

    return results
    
def get_last_danger_level ():
    query = f"SELECT * FROM Gasses WHERE danger = 1 ORDER BY id DESC LIMIT 1"

    result = execute_query (query)

    return result[0]

"""
    Input type: Dictionary in format:
    {Enum or Int GasType: GasValue}
"""
def insert_gasses (gas_levels):
    gasses_string = ""
    gasses_values_string = ""
    danger_level = 0

    for key, value in gas_levels.items():

        if isinstance (key, GasType):
            gasses_string += f"{key.name},"
        elif isinstance (key, int):
            gasses_string += f"{GasType (key).name},"           
        else:
            raise ValueError (f"insert_gasses(), value {key} ({type(key)}) not supported. Use either int or GasType enum.")

        gasses_values_string += f"{value},"

        if (is_danger_level (key, value)):
            danger_level = 1
    
    query = f"INSERT INTO Gasses ({gasses_string}danger) VALUES ({gasses_values_string}{danger_level})"
    #print (query)

    result = insert_query (query)
    return result

def insert_gasses (gas_levels, current_time):
    gasses_string = ""
    gasses_values_string = ""
    danger_level = 0

    for key, value in gas_levels.items():
        if isinstance (key, GasType):
            gasses_string += f"{key.name},"
        elif isinstance (key, int):
            gasses_string += f"{GasType (key).name},"           
        else:
            raise ValueError (f"insert_gasses(), value {key} ({type(key)}) not supported. Use either int or GasType enum.")

        gasses_values_string += f"{value},"

        if (is_danger_level (key, value)):
            danger_level = 1
    
    query = f"INSERT INTO Gasses ({gasses_string}danger,datetime) VALUES ({gasses_values_string}{danger_level},'{current_time.replace(microsecond=0)}')"
    #print (query)

    result = insert_query (query)
    return result

def get_danger_level ():
    query = "SELECT * FROM Gasses WHERE danger = 1 ORDER BY id DESC LIMIT 1"

    result = execute_query (query)

    return result[0]

# TODO Implement this
def is_danger_level (gas, level):
    return False
