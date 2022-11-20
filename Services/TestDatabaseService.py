import pyodbc
from Helper.DatabaseHelper import create_connection_string


def setup_prototype_database(prototype: bool):
    cnxn = pyodbc.connect(create_connection_string(prototype=bool))
    cursor = cnxn.cursor()
    sql_file = open("../DatabaseScripts/create.sql")
    sql_as_string = sql_file.read()
    cursor.execute(sql_as_string)
    cursor.commit()
    cursor.close()
    cnxn.close()
    cnxn = pyodbc.connect(create_connection_string(prototype=bool))
    cursor = cnxn.cursor()
    sql_file = open("../DatabaseScripts/test_data.sql")
    sql_as_string = sql_file.read()
    cursor.execute(sql_as_string)
    cursor.commit()
    cursor.close()
    cnxn.close()
