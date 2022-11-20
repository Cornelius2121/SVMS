import pyodbc
import random
from Helper.DatabaseHelper import create_connection_string
import config


def select_all_active_tutorials(prototype: bool):
    if config.MOCK_DATA:
        tutorial_numbers_total = random.randrange(7, 12)
        tutorial_numbers_list = []
        for tutorial_number in range(1, tutorial_numbers_total + 1):
            tutorial_numbers_list.append(tutorial_number)
        return tutorial_numbers_list
    else:
        sql = """SELECT id FROM tutorial WHERE 1=1"""
        cnxn = pyodbc.connect(create_connection_string(prototype))
        cursor = cnxn.cursor()
        cursor.execute(sql)
        columns = [column[0] for column in cursor.description]
        results = []
        for row in cursor.fetchall():
            results.append(dict(zip(columns, row)))
        cursor.close()
        cnxn.close()
        ids = []
        for result in results:
            ids.append(result['id'])
        return ids



