import pyodbc
import random
from Helper.DatabaseHelper import create_connection_string
import config


def select_all_active_groups_for_tutorial(tutorial_number: int, prototype: bool):
    if config.MOCK_DATA:
        group_numbers_total = random.randrange(20, 26)
        while group_numbers_total % 2 != 0:
            group_numbers_total = random.randrange(20, 26)
        group_numbers_list = []
        for group_number in range(1, group_numbers_total + 1):
            group_numbers_list.append(group_number)

        return group_numbers_list
    else:
        cnxn = pyodbc.connect(create_connection_string(prototype))
        cursor = cnxn.cursor()
        cursor.execute("""
            SELECT * FROM studentgroup WHERE tutorial = ? AND groupactive = B'1';
        """, tutorial_number)
        columns = [column[0] for column in cursor.description]
        results = []
        for row in cursor.fetchall():
            results.append(dict(zip(columns, row)))
        cursor.close()
        cnxn.close()
        return results


def select_all_groups_for_tutorial_with_names(tutorial_number: int, prototype: bool, format_results=True):
    sql = """SELECT sg.id, sg.tutorial, s.studentnumber, s.firstname, s.lastname
            FROM studentgroup sg
                     LEFT JOIN student s on sg.id = s.studentgroup
            WHERE sg.tutorial = ?
              and sg.groupactive = b'1'"""
    cnxn = pyodbc.connect(create_connection_string(prototype))
    cursor = cnxn.cursor()
    cursor.execute(sql, tutorial_number)
    columns = [column[0] for column in cursor.description]
    results = []
    for row in cursor.fetchall():
        results.append(dict(zip(columns, row)))
    cursor.close()
    cnxn.close()
    if format_results:
        group_numbers = []
        for result in results:
            group_numbers.append(result['id'])
        group_numbers = set(group_numbers)
        groups = []
        for group_number in group_numbers:
            group = {'id': group_number,
                     'tutorialNumber': tutorial_number,
                     'students': []}
            for result in results:
                if result['id'] == group['id']:
                    group['students'].append({'firstname': result['firstname'], 'lastname': result['lastname']})
            groups.append(group)
    return groups


def insert_new_group(prototype: bool, tutorial_id: int) -> int:
    sql = """INSERT INTO studentgroup (tutorial, studentcount, groupactive)  VALUES (?,?,?)"""
    cnxn = pyodbc.connect(create_connection_string(prototype))
    cursor = cnxn.cursor()
    cursor.execute(sql, tutorial_id, 0, 1)
    cursor.commit()
    group_id_sql = "SELECT @@IDENTITY"
    cursor.execute(group_id_sql)
    group_id = -1
    for row in cursor.fetchall():
        group_id = row
    cursor.close()
    cnxn.close()
    return group_id[0]


def insert_students_to_group(students: list, group_id: int, prototype: bool):
    sql = """UPDATE student SET studentgroup = ? WHERE id = ?"""
    cnxn = pyodbc.connect(create_connection_string(prototype))
    cursor = cnxn.cursor()
    for student in students:
        cursor.execute(sql, group_id, student)
    cursor.commit()
    sql = """UPDATE studentgroup SET studentcount = studentcount + ? WHERE id = ?"""
    cursor.execute(sql, len(students), group_id)
    cursor.commit()
    cursor.close()
    cnxn.close()


def select_group_from_id(group_id: int, prototype: bool = False):
    sql = """SELECT * FROM studentgroup WHERE id = ?"""
    cnxn = pyodbc.connect(create_connection_string(prototype))
    cursor = cnxn.cursor()
    cursor.execute(sql, group_id)
    columns = [column[0] for column in cursor.description]
    results = []
    for row in cursor.fetchall():
        results.append(dict(zip(columns, row)))
    return results


def select_all_active_groups(prototype: bool = False):
    sql = """SELECT id FROM studentgroup WHERE groupactive = B'1'"""
    cnxn = pyodbc.connect(create_connection_string(prototype))
    cursor = cnxn.cursor()
    cursor.execute(sql)
    columns = [column[0] for column in cursor.description]
    results = []
    for row in cursor.fetchall():
        results.append(dict(zip(columns, row)))
    return results


def remove_student_from_group(student_id: int, prototype: bool = False):
    sql = """UPDATE student SET studentgroup = NULL WHERE id = ?"""
    cnxn = pyodbc.connect(create_connection_string(prototype))
    cursor = cnxn.cursor()
    cursor.execute(sql, student_id)
    cursor.commit()
    cursor.close()
    cnxn.close()


def check_if_group_exists(group_id: int, prototype: bool = False) -> bool:
    sql = """SELECT * FROM studentgroup WHERE id = ? """
    cnxn = pyodbc.connect(create_connection_string(prototype))
    cursor = cnxn.cursor()
    cursor.execute(sql, group_id)
    columns = [column[0] for column in cursor.description]
    results = []
    for row in cursor.fetchall():
        results.append(dict(zip(columns, row)))
    if len(results) == 0:
        return False
    else:
        return True


def reduce_student_group_count(group_id: int, prototype: bool = False):
    sql = """UPDATE studentgroup SET studentcount = studentcount - 1 WHERE id = ?;"""
    cnxn = pyodbc.connect(create_connection_string(prototype))
    cursor = cnxn.cursor()
    cursor.execute(sql, group_id)
    cursor.commit()
    cursor.close()
    cnxn.close()

    group = select_group_from_id(group_id)[0]
    if group['studentcount'] == 0:
        sql = """UPDATE studentgroup SET groupactive = B'0' WHERE id = ?;"""
        cnxn = pyodbc.connect(create_connection_string(prototype))
        cursor = cnxn.cursor()
        cursor.execute(sql, group_id)
        cursor.commit()
        cursor.close()
        cnxn.close()


def increase_student_group_count(group_id: int, prototype: bool = False):
    sql = """UPDATE studentgroup SET studentcount = studentcount + 1 WHERE id = ?;"""
    cnxn = pyodbc.connect(create_connection_string(prototype))
    cursor = cnxn.cursor()
    cursor.execute(sql, group_id)
    cursor.commit()
    cursor.close()
    cnxn.close()

    group = select_group_from_id(group_id)[0]
    if group['studentcount'] == 1:
        sql = """UPDATE studentgroup SET groupactive = B'1' WHERE id = ?;"""
        cnxn = pyodbc.connect(create_connection_string(prototype))
        cursor = cnxn.cursor()
        cursor.execute(sql, group_id)
        cursor.commit()
        cursor.close()
        cnxn.close()


def select_all_groups_and_students(prototype: bool = False):
    sql = """SELECT sg.id as "Group ID", sg.tutorial as "Tutorial Number", s.studentnumber, 
                sg.groupactive as "Group Active", sg.studentcount as "Student Count" FROM studentgroup sg
                LEFT JOIN student s on sg.id = s.studentgroup;"""
    cnxn = pyodbc.connect(create_connection_string(prototype))
    cursor = cnxn.cursor()
    cursor.execute(sql)
    columns = [column[0] for column in cursor.description]
    results = []
    for row in cursor.fetchall():
        results.append(dict(zip(columns, row)))
    groups = []
    for student in results:
        if student['Group ID'] not in groups:
            groups.append(student['Group ID'])
    student_groups = []
    for group in groups:
        current_group = {'Group ID': group, 'Students': []}
        for student in results:
            if student['Group ID'] == group:
                current_group['Students'].append(student['studentnumber'])
                current_group['Group Active'] = True if student['Group Active'] == '1' else False
                current_group['Tutorial Number'] = student['Tutorial Number']
                current_group['Student Count'] = student['Student Count']
        student_groups.append(current_group)
    student_groups = sorted(sorted(student_groups, key=lambda x: x['Group ID']), key=lambda x: x['Tutorial Number'])
    return student_groups


def update_groups_active_status(group_id: int, group_change: bool, prototype: bool = False):
    if group_change:
        sql = """UPDATE studentgroup SET groupactive = B'1' WHERE id = ?;"""
    else:
        sql = """UPDATE studentgroup SET groupactive = B'0' WHERE id = ?;"""
    cnxn = pyodbc.connect(create_connection_string(prototype))
    cursor = cnxn.cursor()
    cursor.execute(sql, group_id)
    cursor.commit()
    cursor.close()
    cnxn.close()


def create_group(tutorial_id: int, prototype: bool = False):
    sql = """INSERT INTO studentgroup (tutorial, studentcount, groupactive) VALUES (?, 0, B'0');"""
    cnxn = pyodbc.connect(create_connection_string(prototype))
    cursor = cnxn.cursor()
    cursor.execute(sql, tutorial_id)
    cursor.commit()
    cursor.close()
    cnxn.close()
