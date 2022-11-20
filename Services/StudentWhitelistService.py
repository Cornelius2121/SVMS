import pyodbc
from Helper.DatabaseHelper import create_connection_string


def get_all_students_from_whitelist(prototype: bool = False):
    sql = """SELECT * FROM studentwhitelist"""
    cnxn = pyodbc.connect(create_connection_string(prototype))
    cursor = cnxn.cursor()
    cursor.execute(sql)
    columns = [column[0] for column in cursor.description]
    results = []
    formatted_results = []
    for row in cursor.fetchall():
        results.append(dict(zip(columns, row)))
    cursor.close()
    cnxn.close()
    tuts = []
    for result in results:
        tuts.append(result['tutorialid'])
    tuts = list(set(tuts))
    for tut in tuts:

        current_tutorial = {
            "Tutorial Number": tut,
            "Students": []
        }
        for result in results:
            if result['tutorialid'] == tut:
                current_tutorial['Students'].append(result['studentid'])
        formatted_results.append(current_tutorial)
    return formatted_results


def insert_students_to_whitelist(student_data: list, prototype: bool = False):
    sql = """INSERT INTO studentwhitelist (studentid, tutorialid, accountcreated) VALUES (?,?,?)"""
    cnxn = pyodbc.connect(create_connection_string(prototype))
    cursor = cnxn.cursor()
    for tutorial in student_data:
        for student in tutorial['Students']:
            tutorial_number = tutorial['Tutorial Number']
            cursor.execute(sql, str(student), tutorial_number, False)
    cursor.commit()
    cursor.close()
    cnxn.close()


def check_account_created_whitelist(student_number: str, prototype: bool = False) -> bool:
    sql = """SELECT * FROM studentwhitelist WHERE studentid = ?"""
    cnxn = pyodbc.connect(create_connection_string(prototype))
    cursor = cnxn.cursor()
    cursor.execute(sql, student_number)
    columns = [column[0] for column in cursor.description]
    results = []
    for row in cursor.fetchall():
        results.append(dict(zip(columns, row)))
    cursor.close()
    cnxn.close()
    if len(results) == 0:
        return True
    if results[0]['accountcreated'] == '0':
        return False
    else:
        return True


def get_tutorial_from_student_number(student_number: str, prototype: bool = False) -> int:
    sql = """SELECT tutorialid FROM studentwhitelist WHERE studentid = ?"""
    cnxn = pyodbc.connect(create_connection_string(prototype))
    cursor = cnxn.cursor()
    cursor.execute(sql, student_number)
    columns = [column[0] for column in cursor.description]
    results = []
    for row in cursor.fetchall():
        results.append(dict(zip(columns, row)))
    cursor.close()
    cnxn.close()
    return results[0]['tutorialid']


def update_whitelist_flag(student_number: str, prototype: bool = False):
    sql = """UPDATE studentwhitelist SET accountcreated = B'1' WHERE studentid= ?"""
    cnxn = pyodbc.connect(create_connection_string(prototype))
    cursor = cnxn.cursor()
    cursor.execute(sql, student_number)
    cursor.commit()
    cursor.close()
    cnxn.close()
