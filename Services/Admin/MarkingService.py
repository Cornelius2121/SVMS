import pyodbc
from Helper.DatabaseHelper import create_connection_string


def select_all_marking_columns(prototype: bool = False):
    sql = """SELECT * FROM AvailableMarkingColumns"""
    cnxn = pyodbc.connect(create_connection_string(prototype))
    cursor = cnxn.cursor()
    cursor.execute(sql)
    columns = [column[0] for column in cursor.description]
    results = []
    for row in cursor.fetchall():
        results.append(dict(zip(columns, row)))
    cursor.close()
    cnxn.close()
    return results

def select_method_name_from_column_for_marking_column(column_name, prototype: bool = False):
    sql = """SELECT * FROM AvailableMarkingColumns WHERE column_name = ?"""
    cnxn = pyodbc.connect(create_connection_string(prototype))
    cursor = cnxn.cursor()
    cursor.execute(sql, column_name)
    columns = [column[0] for column in cursor.description]
    results = []
    for row in cursor.fetchall():
        results.append(dict(zip(columns, row)))
    cursor.close()
    cnxn.close()
    return results[0]['method_name']

def select_all_automated_marking_columns(prototype: bool = False):
    sql = """SELECT * FROM AutomaticMarkingColumns"""
    cnxn = pyodbc.connect(create_connection_string(prototype))
    cursor = cnxn.cursor()
    cursor.execute(sql)
    columns = [column[0] for column in cursor.description]
    results = []
    for row in cursor.fetchall():
        results.append(dict(zip(columns, row)))
    cursor.close()
    cnxn.close()
    return results
