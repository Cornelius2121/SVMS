import pyodbc
from Helper.DatabaseHelper import create_connection_string


def insert_new_student_with_no_group(student_number: str, password: str, tutorial_id: int,
                                     prototype: bool) -> int:
    sql = """INSERT INTO student (studentnumber, password, tutorial) VALUES (?,?,?)"""
    cnxn = pyodbc.connect(create_connection_string(prototype))
    cursor = cnxn.cursor()
    cursor.execute(sql, student_number, password, tutorial_id)
    cursor.commit()
    student_id_sql = "SELECT @@IDENTITY"
    cursor.execute(student_id_sql)
    student_id = -1
    for row in cursor.fetchall():
        student_id = row
    cursor.close()
    cnxn.close()
    return student_id[0]


def select_student_from_student_number(student_number: str, prototype: bool = False):
    sql = """SELECT * FROM student WHERE studentnumber = ?"""
    cnxn = pyodbc.connect(create_connection_string(prototype))
    cursor = cnxn.cursor()
    cursor.execute(sql, student_number)
    columns = [column[0] for column in cursor.description]
    results = []
    for row in cursor.fetchall():
        results.append(dict(zip(columns, row)))
    cursor.close()
    cnxn.close()
    return results


def select_all_students(prototype: bool = False):
    sql = """SELECT * FROM student"""
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


def select_all_students_who_gave_feedback_for_week(week: int, prototype: bool = False):
    sql = """
        SELECT studentnumber
        FROM student
        WHERE student.id IN (SELECT f.author FROM feedback f WHERE f.weeksubmitted = ?);
    """
    cnxn = pyodbc.connect(create_connection_string(prototype))
    cursor = cnxn.cursor()
    cursor.execute(sql, week)
    columns = [column[0] for column in cursor.description]
    results = []
    for row in cursor.fetchall():
        results.append(dict(zip(columns, row)))
    cursor.close()
    cnxn.close()
    return results


def select_all_students_who_received_feedback_for_week(week: int, prototype: bool = False):
    sql = """
        SELECT studentnumber
        FROM student
        WHERE student.id IN (SELECT f.target FROM feedback f WHERE f.weeksubmitted = ?);
    """
    cnxn = pyodbc.connect(create_connection_string(prototype))
    cursor = cnxn.cursor()
    cursor.execute(sql, week)
    columns = [column[0] for column in cursor.description]
    results = []
    for row in cursor.fetchall():
        results.append(dict(zip(columns, row)))
    cursor.close()
    cnxn.close()
    return results


def select_all_students_who_actioned_feedback_for_week(week: int, prototype: bool = False):
    sql = """
        SELECT DISTINCT(s.studentnumber)
        FROM actionfeedback
                 LEFT JOIN feedback f on actionfeedback.feedbackid = f.id
                 LEFT JOIN student s on f.target = s.id
        WHERE f.weeksubmitted = ?;
    """
    cnxn = pyodbc.connect(create_connection_string(prototype))
    cursor = cnxn.cursor()
    cursor.execute(sql, week)
    columns = [column[0] for column in cursor.description]
    results = []
    for row in cursor.fetchall():
        results.append(dict(zip(columns, row)))
    cursor.close()
    cnxn.close()
    return results


def select_all_students_who_are_in_an_inactive_group(prototype: bool = False):
    sql = """
        SELECT studentnumber
        FROM student s
                 LEFT JOIN studentgroup s2 on s.studentgroup = s2.id
        WHERE s2.groupactive = B'0';
    """
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


def select_group_from_student_id(student_id: int, prototype: bool = False):
    sql = """SELECT studentgroup FROM student WHERE id = ?"""
    cnxn = pyodbc.connect(create_connection_string(prototype))
    cursor = cnxn.cursor()
    cursor.execute(sql, student_id)
    columns = [column[0] for column in cursor.description]
    results = []
    for row in cursor.fetchall():
        results.append(dict(zip(columns, row)))
    cursor.close()
    cnxn.close()
    return results


def select_all_students_student_numbers_in_group(group_id: int, prototype: bool = False):
    sql = """SELECT studentnumber FROM student WHERE studentgroup = ?"""
    cnxn = pyodbc.connect(create_connection_string(prototype))
    cursor = cnxn.cursor()
    cursor.execute(sql, group_id)
    columns = [column[0] for column in cursor.description]
    results = []
    for row in cursor.fetchall():
        results.append(dict(zip(columns, row)))
    cursor.close()
    cnxn.close()
    return results


def select_student_id_from_student_number(student_number: str, prototype: bool = False):
    sql = """SELECT id FROM student WHERE studentnumber = ?"""
    cnxn = pyodbc.connect(create_connection_string(prototype))
    cursor = cnxn.cursor()
    cursor.execute(sql, student_number)
    columns = [column[0] for column in cursor.description]
    results = []
    for row in cursor.fetchall():
        results.append(dict(zip(columns, row)))
    cursor.close()
    cnxn.close()
    return results


def select_student_number_from_student_id(student_id: int, prototype: bool = False):
    sql = """SELECT studentnumber FROM student WHERE id = ?"""
    cnxn = pyodbc.connect(create_connection_string(prototype))
    cursor = cnxn.cursor()
    cursor.execute(sql, student_id)
    columns = [column[0] for column in cursor.description]
    results = []
    for row in cursor.fetchall():
        results.append(dict(zip(columns, row)))
    cursor.close()
    cnxn.close()
    return results


def select_student_tutorial_from_student_id(student_id: int, prototype: bool = False):
    sql = """SELECT tutorial FROM student WHERE id = ?"""
    cnxn = pyodbc.connect(create_connection_string(prototype))
    cursor = cnxn.cursor()
    cursor.execute(sql, student_id)
    columns = [column[0] for column in cursor.description]
    results = []
    for row in cursor.fetchall():
        results.append(dict(zip(columns, row)))
    cursor.close()
    cnxn.close()
    return results


def check_student_group_from_student_id(student_id: int, prototype: bool = False) -> bool:
    sql = """SELECT studentgroup FROM student WHERE id = ?"""
    cnxn = pyodbc.connect(create_connection_string(prototype))
    cursor = cnxn.cursor()
    cursor.execute(sql, student_id)
    columns = [column[0] for column in cursor.description]
    results = []
    for row in cursor.fetchall():
        results.append(dict(zip(columns, row)))
    cursor.close()
    cnxn.close()
    if results[0]['studentgroup'] == None:
        return True
    else:
        return False


def select_password_from_student_id(student_number: str, prototype: bool = False):
    sql = """SELECT password FROM student WHERE studentnumber = ?"""
    cnxn = pyodbc.connect(create_connection_string(prototype))
    cursor = cnxn.cursor()
    cursor.execute(sql, student_number)
    columns = [column[0] for column in cursor.description]
    results = []
    for row in cursor.fetchall():
        results.append(dict(zip(columns, row)))
    cursor.close()
    cnxn.close()
    return results[0]['password']


def select_all_student_ids_in_group(student_group: int, prototype: bool = False):
    sql = """SELECT id FROM student WHERE studentgroup = ?"""
    cnxn = pyodbc.connect(create_connection_string(prototype))
    cursor = cnxn.cursor()
    cursor.execute(sql, student_group)
    columns = [column[0] for column in cursor.description]
    results = []
    for row in cursor.fetchall():
        results.append(dict(zip(columns, row)))
    cursor.close()
    cnxn.close()
    return results


def update_new_password(student_id: int, password: str, prototype: bool = False):
    sql = """UPDATE student SET password = ? WHERE id = ?"""
    cnxn = pyodbc.connect(create_connection_string(prototype))
    cursor = cnxn.cursor()
    cursor.execute(sql, password, id)
    cursor.commit()
    cursor.close()
    cnxn.close()


def get_all_student_numbers_with_c_group_numbers_and_formatted_tutorial_day_and_time(prototype: bool = False):
    sql = """SELECT CONCAT('c', s.studentnumber) as "Student Number", s.studentgroup as "Group Number", CONCAT(t.day, ' ', t.time) as "Tutorial"
                FROM student s
                LEFT JOIN tutorial t on s.tutorial = t.id"""
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


def delete_student_from_student_number(student_number: str, prototype: bool = False):
    sql = """DELETE
    FROM actionfeedback afb
    WHERE feedbackid IN
          (SELECT ID as feedbackid
           FROM feedback
           WHERE target = (SELECT id FROM student WHERE studentnumber = ?)
              OR author = (SELECT id FROM student WHERE studentnumber = ?));
    
    DELETE
    FROM feedback
    WHERE author IN (SELECT id FROM student WHERE studentnumber = ?)
       OR target IN (SELECT id FROM student WHERE studentnumber = ?);
       
    UPDATE studentgroup SET studentcount = studentcount - 1 WHERE id = (SELECT studentgroup FROM student WHERE studentnumber = ?);

    DELETE FROM student WHERE studentnumber = ?;"""
    cnxn = pyodbc.connect(create_connection_string(prototype))
    cursor = cnxn.cursor()
    cursor.execute(sql, student_number, student_number, student_number, student_number, student_number, student_number)
    cursor.commit()
    cursor.close()
    cnxn.close()


def update_student_tutorial(student_id: int, tutorial_id: int, prototype: bool = False):
    sql = """UPDATE student SET tutorial = ? WHERE id = ?"""
    cnxn = pyodbc.connect(create_connection_string(prototype))
    cursor = cnxn.cursor()
    cursor.execute(sql, tutorial_id, student_id)
    cursor.commit()
    cursor.close()
    cnxn.close()


def add_student_to_group(student_id: int, group_id: int, prototype: bool = False):
    sql = """UPDATE student SET studentgroup = ? WHERE id = ?"""
    cnxn = pyodbc.connect(create_connection_string(prototype))
    cursor = cnxn.cursor()
    cursor.execute(sql, group_id, student_id)
    cursor.commit()
    cursor.close()
    cnxn.close()


def remove_student_from_group(student_id: int, prototype: bool = False):
    sql = """UPDATE student SET studentgroup = NULL WHERE id = ?"""
    cnxn = pyodbc.connect(create_connection_string(prototype))
    cursor = cnxn.cursor()
    cursor.execute(sql, student_id)
    cursor.commit()
    cursor.close()
    cnxn.close()


def get_all_unallocated_students(prototype: bool = False):
    sql = """SELECT * FROM student where studentgroup IS NULL;"""
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
