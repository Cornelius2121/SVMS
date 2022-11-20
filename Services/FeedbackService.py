import pyodbc
import random
from Helper.DatabaseHelper import create_connection_string
import config
import datetime


def insert_new_feedback(metrics: list, goodcomment: str, badcomment: str, target: int, submitter: int,
                        time: datetime.datetime, week: int,
                        prototype: bool = False):
    if submitter == -1:
        submitter = None
    sql = """INSERT INTO feedback (target, author, metric1, metric2, metric3, metric4, report, timeSubmitted, 
    goodcomment, badcomment, weeksubmitted, actionfeedbackrecorded) 
    VALUES (?,?,?,?,?,?,?,?,?,?,?,?)"""
    cnxn = pyodbc.connect(create_connection_string(prototype))
    cursor = cnxn.cursor()
    cursor.execute(sql, target, submitter, *metrics, 0, time, goodcomment, badcomment, week, 0)
    cursor.commit()
    group_id_sql = "SELECT @@IDENTITY"
    cursor.execute(group_id_sql)
    id = -1
    for row in cursor.fetchall():
        id = row
    cursor.close()
    cnxn.close()
    return id[0]


def get_feedback_from_id(id: int, prototype: bool = False):
    sql = """SELECT * FROM Feedback WHERE ID = ?"""
    cnxn = pyodbc.connect(create_connection_string(prototype))
    cursor = cnxn.cursor()
    cursor.execute(sql, id)
    columns = [column[0] for column in cursor.description]
    results = []
    for row in cursor.fetchall():
        results.append(dict(zip(columns, row)))
    return results


def get_all_feedback_in_week_submitted(week: int, prototype: bool = False):
    sql = """SELECT * FROM Feedback WHERE weeksubmitted = ?"""
    cnxn = pyodbc.connect(create_connection_string(prototype))
    cursor = cnxn.cursor()
    cursor.execute(sql, week)
    columns = [column[0] for column in cursor.description]
    results = []
    for row in cursor.fetchall():
        results.append(dict(zip(columns, row)))
    return results
