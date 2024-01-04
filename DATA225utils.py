#--------------------------------#
# Python database utilities file #
#--------------------------------#

import os
from configparser import ConfigParser
from mysql.connector import MySQLConnection, Error

def read_config(config_file = 'config.ini', section = 'mysql'):
    """
    Read the configuration file config_file with the given section.
    If successful, return the configuration as a dictionary,
    else raise an exception.
    """
    parser = ConfigParser()
    
    # Does the configuration file exist?
    if os.path.isfile(config_file):
        parser.read(config_file)
    else:
        raise Exception(f"Configuration file '{config_file}' "
                        "doesn't exist.")
    
    config = {}
    
    if parser.has_section(section):
        # Parse the configuration file.
        items = parser.items(section)
        
        # Construct the parameter dictionary.
        for item in items:
            config[item[0]] = item[1]
            
    else:
        raise Exception(f'Section [{section}] missing ' + \
                        f'in config file {config_file}')
    
    return config

def make_connection(config_file = 'config.ini', section = 'mysql'):
    """
    Make a database connection with the configuration file config_file
    with the given section. If successful, return the connection,
    else raise an exception.
    """
    try:
        db_config = read_config(config_file, section)
        conn = MySQLConnection(**db_config)

        if conn.is_connected():
            return conn

    except Error as e:
        raise Exception(f'Connection failed: {e}')

from pandas import DataFrame

def dataframe_query(conn, sql):
    """
    Use the database connection conn to execute
    the SQL code. Return the resulting row count
    and the rows as a dataframe or (0, None) 
    if there were no rows. If the query failed,
    raise an exception.
    """
    try:
        cursor = conn.cursor()
        cursor.execute(sql)

        rows  = cursor.fetchall()
        count = cursor.rowcount

        if count > 0:

            # Get the names of the columns.
            columns = cursor.description
            column_names = [column_info[0] 
                            for column_info in columns]

            # Return the query results in a dataframe.
            df = DataFrame(rows)
            df.columns = column_names
            cursor.close()
            return count, df

        else:
            cursor.close()
            return 0, None
        
    except Error as e:
        raise Exception(f'Query failed: {e}')

# Copyright (c) 2023 by Ronald Mak