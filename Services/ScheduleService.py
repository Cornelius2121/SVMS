import pyodbc
from Helper.DatabaseHelper import create_connection_string
from Services.WeekService import get_current_week


def insert_full_week_schedule(full_schedule: list, week_number: int, prototype: bool):
    cnxn = pyodbc.connect(create_connection_string(prototype))
    cursor = cnxn.cursor()
    for tutorial in full_schedule:
        tutorial_number = tutorial['tutorial number']
        round_count = 0
        for round in tutorial['schedule']:
            round_count = round_count + 1
            desk_count = 0
            for debate in round:
                desk_count = desk_count + 1
                cursor.execute(
                    """INSERT INTO debate (weeknumber, tutorialnumber,roundnumber, desknumber, groupx, groupy) 
                    values (?,?,?,?,?,?)""",
                    *[week_number, tutorial_number, round_count, desk_count, debate[0]['id'], debate[1]['id']]
                )
    cursor.commit()
    cursor.close()
    cnxn.close()


def select_all_tutorials_for_week(week: int, prototype: bool):
    cnxn = pyodbc.connect(create_connection_string(prototype))
    cursor = cnxn.cursor()
    cursor.execute(
        """SELECT weeknumber, tutorialnumber, roundnumber, desknumber, groupx, groupy 
        FROM debate 
        WHERE weeknumber = ?""",
        week)
    columns = [column[0] for column in cursor.description]
    results = []
    for row in cursor.fetchall():
        results.append(dict(zip(columns, row)))
    cursor.close()
    cnxn.close()
    return results

def select_all_tutorials_for_all_weeks(prototype: bool = False):
    cnxn = pyodbc.connect(create_connection_string(prototype))
    cursor = cnxn.cursor()
    cursor.execute(
        """SELECT weeknumber, tutorialnumber, roundnumber, desknumber, groupx, groupy 
        FROM debate""")
    columns = [column[0] for column in cursor.description]
    results = []
    for row in cursor.fetchall():
        results.append(dict(zip(columns, row)))
    cursor.close()
    cnxn.close()
    return format_schedule(results)

def select_all_rounds_for_tutorial_and_week(week: int, tutorial: int, format_result: bool = True,
                                            prototype: bool = False):
    cnxn = pyodbc.connect(create_connection_string(prototype))
    cursor = cnxn.cursor()
    cursor.execute(
        """SELECT weeknumber, tutorialnumber, roundnumber, desknumber, groupx, groupy 
        FROM debate 
        WHERE weeknumber = ? AND tutorialnumber = ?""",
        week, tutorial)
    columns = [column[0] for column in cursor.description]
    results = []
    for row in cursor.fetchall():
        results.append(dict(zip(columns, row)))
    cursor.close()
    cnxn.close()
    if not format_result:
        return results
    else:
        return format_schedule(results)


def format_schedule(results: list) -> list:
    weeks = []
    tutorials = []
    for row in results:
        weeks.append(row['weeknumber'])
        tutorials.append(row['tutorialnumber'])
    weeks_numbers = set(weeks)
    tutorials_numbers = set(tutorials)
    weeks = []
    for week in list(weeks_numbers):
        current_week = {
            'week': week,
            'tutorials': []
        }
        for tutorial in list(tutorials_numbers):
            current_tutorial = {
                'tutorial_number': tutorial,
                'rounds': []
            }
            # now get all relevant dicts from the results list
            week_and_tutorial_rounds = []
            rounds = []
            for row in results:
                if row['weeknumber'] == week and row['tutorialnumber'] == tutorial:
                    week_and_tutorial_rounds.append(row)
                    rounds.append(row['roundnumber'])
            rounds = list(set(rounds))
            for round in rounds:
                current_round = {
                    'round': round,
                    'debates': []
                }
                for debate in week_and_tutorial_rounds:
                    if debate['roundnumber'] == round:
                        current_debate = {
                            'desk number': debate['desknumber'],
                            'group x': debate['groupx'],
                            'group y': debate['groupy']
                        }
                        current_round['debates'].append(current_debate)
                current_tutorial['rounds'].append(current_round)
            current_week['tutorials'].append(current_tutorial)
        weeks.append(current_week)
    return weeks


def select_all_rounds_and_tutorials_from_week(week: int, prototype: bool = False, format_result: bool = True):
    cnxn = pyodbc.connect(create_connection_string(prototype))
    cursor = cnxn.cursor()
    cursor.execute(
        """SELECT weeknumber, tutorialnumber, roundnumber, desknumber, groupx, groupy 
        FROM debate 
        WHERE weeknumber = ?""",
        int(week))
    columns = [column[0] for column in cursor.description]
    results = []
    for row in cursor.fetchall():
        results.append(dict(zip(columns, row)))
    cursor.close()
    cnxn.close()
    if not format_result:
        return results
    else:
        return format_schedule(results)


def select_all_rounds_from_tutorial(tutorial: int, prototype: bool = False, format_result: bool = True):
    cnxn = pyodbc.connect(create_connection_string(prototype))
    cursor = cnxn.cursor()
    cursor.execute(
        """SELECT weeknumber, tutorialnumber, roundnumber, desknumber, groupx, groupy 
        FROM debate 
        WHERE tutorialnumber = ?""",
        int(tutorial))
    columns = [column[0] for column in cursor.description]
    results = []
    for row in cursor.fetchall():
        results.append(dict(zip(columns, row)))
    cursor.close()
    cnxn.close()
    if not format_result:
        return results
    else:
        return format_schedule(results)


def select_all_rounds_from_tutorial_and_current_week(tutorial: int, week: int = get_current_week(),
                                                     prototype: bool = False, format_result: bool = True):
    cnxn = pyodbc.connect(create_connection_string(prototype))
    cursor = cnxn.cursor()
    cursor.execute(
        """SELECT weeknumber, tutorialnumber, roundnumber, desknumber, groupx, groupy 
        FROM debate 
        WHERE tutorialnumber = ? AND weeknumber = ?""",
        int(tutorial), week)
    columns = [column[0] for column in cursor.description]
    results = []
    for row in cursor.fetchall():
        results.append(dict(zip(columns, row)))
    cursor.close()
    cnxn.close()
    if not format_result:
        return results
    else:
        return format_schedule(results)


def select_debate_from_group_number_and_week(week: int, group: int, prototype: bool = False):
    cnxn = pyodbc.connect(create_connection_string(prototype))
    cursor = cnxn.cursor()
    cursor.execute(
        """SELECT * 
        FROM debate 
        WHERE groupx = ? OR groupy = ? and weeknumber = ?""",
        group, group, week)
    columns = [column[0] for column in cursor.description]
    results = []
    for row in cursor.fetchall():
        results.append(dict(zip(columns, row)))
    cursor.close()
    cnxn.close()
    return results
