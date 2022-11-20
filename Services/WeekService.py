import pyodbc
import random
from Helper.DatabaseHelper import create_connection_string
import config
import datetime
import pytz


def select_week_number_from_date(date: datetime.datetime, prototype: bool):
    cnxn = pyodbc.connect(create_connection_string(prototype))
    cursor = cnxn.cursor()
    cursor.execute("""
        SELECT id FROM week WHERE ? BETWEEN weekstart AND weekend;
    """, date)
    columns = [column[0] for column in cursor.description]
    results = []
    for row in cursor.fetchall():
        results.append(dict(zip(columns, row)))
    cursor.close()
    cnxn.close()
    if len(results) == 0:
        return -1
    else:
        return int(results[0]['id'])

def get_current_week(prototype: bool=False):
    date = datetime.datetime.now(tz=pytz.timezone('Australia/Sydney'))
    cnxn = pyodbc.connect(create_connection_string(prototype))
    cursor = cnxn.cursor()
    cursor.execute("""
            SELECT id FROM week WHERE ? BETWEEN weekstart AND weekend;
        """, date)
    columns = [column[0] for column in cursor.description]
    results = []
    for row in cursor.fetchall():
        results.append(dict(zip(columns, row)))
    cursor.close()
    cnxn.close()
    if len(results) == 0:
        return 1
    else:
        return int(results[0]['id'])

def get_all_remaining_weeks(prototype: bool=False):
    date = datetime.datetime.now(tz=pytz.timezone('Australia/Sydney'))
    cnxn = pyodbc.connect(create_connection_string(prototype))
    cursor = cnxn.cursor()
    cursor.execute("""
                SELECT * FROM week WHERE weekstart > ?;
            """, date)
    columns = [column[0] for column in cursor.description]
    results = []
    for row in cursor.fetchall():
        results.append(dict(zip(columns, row)))
    cursor.close()
    cnxn.close()
    if len(results) == 0:
        return []
    else:
        return results