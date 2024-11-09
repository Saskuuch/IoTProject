import mysql.connector
from mysql.connector import Error
from enum import Enum
from datetime import datetime
from datetime import timedelta
import random
import configparser
import os

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
    gas = parse_to_gas_enum (gas_index)

    query = f"SELECT `{gas}` FROM Gasses WHERE `{gas}` IS NOT NULL ORDER BY id DESC LIMIT 1"

    result = execute_query (query)

    if len (result) == 0:
        return 0
    else:
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
        gasses_string += f"AVG({parse_to_gas_enum(gas)}),"
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
        gasses_string += f"{parse_to_gas_enum(key)},"

        gasses_values_string += f"{value},"

        if (is_danger_level (key, value)):
            danger_level = 1
    
    query = f"INSERT INTO Gasses ({gasses_string}danger) VALUES ({gasses_values_string}{danger_level})"
    #print (query)

    result = insert_query (query)
    return result

def insert_gasses_with_timestamp (gas_levels, current_time):
    gasses_string = ""
    gasses_values_string = ""
    danger_level = 0

    for key, value in gas_levels.items():
        gasses_string += f"{parse_to_gas_enum(key)},"

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

def parse_to_gas_enum(value):
    if isinstance (value, GasType):
        return value.name
    elif isinstance (value, int):
        return GasType (value).name          
    else:
        raise ValueError (f"insert_gasses(), value {value} ({type(value)}) not supported. Use either int or GasType enum.")

def generate_config_file():
    if not os.path.exists("settings.ini"):
        config = configparser.ConfigParser()

        config.add_section('GasDangerLevels')
        config.set('GasDangerLevels', str(parse_to_gas_enum(10)), '1000')  # Ensure the gas is a string
        config.set('GasDangerLevels', str(parse_to_gas_enum(1)), '1000')
        config.set('GasDangerLevels', str(parse_to_gas_enum(4)), '1000')
        config.set('GasDangerLevels', str(parse_to_gas_enum(3)), '1000')

        with open("settings.ini", 'w') as configfile:
            config.write(configfile)

def update_danger_level(gas, value):
    generate_config_file()
    config = configparser.ConfigParser()
    config.read('settings.ini')

    try:
        # Ensure gas is a string
        config.set('GasDangerLevels', str(parse_to_gas_enum(gas)), str(value))

        with open('settings.ini', 'w') as configfile:
            config.write(configfile)
    except configparser.NoOptionError:
        print("Error, no setting found")

def get_danger_level_setting(gas):
    generate_config_file()
    config = configparser.ConfigParser()
    config.read('settings.ini')

    try:
        # Ensure gas is a string
        gas_str = str(parse_to_gas_enum(gas))  # Convert gas to string
        danger_level = config.getint('GasDangerLevels', gas_str)
        return danger_level
    except configparser.NoOptionError:
        print("Error, no setting found")
        return None

def is_danger_level (gas, level):
    danger_level = get_danger_level_setting (gas)
    if level >= danger_level:
        return True
    else:
        return False
