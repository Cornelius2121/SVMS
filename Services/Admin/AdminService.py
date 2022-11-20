import pyodbc
from Helper.DatabaseHelper import create_connection_string


def select_password_from_admin_username(username: str, prototype: bool = False):
    sql = """SELECT password FROM admin WHERE username = ?"""
    cnxn = pyodbc.connect(create_connection_string(prototype))
    cursor = cnxn.cursor()
    cursor.execute(sql, username)
    columns = [column[0] for column in cursor.description]
    results = []
    for row in cursor.fetchall():
        results.append(dict(zip(columns, row)))
    cursor.close()
    cnxn.close()
    return results[0]['password']
