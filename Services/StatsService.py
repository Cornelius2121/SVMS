import pyodbc
from Helper.DatabaseHelper import create_connection_string


def select_all_statistics_for_student_id(student_id: int, exclude_certain_weeks=None, prototype: bool = False):
    if exclude_certain_weeks is None:
        exclude_certain_weeks = []
    cnxn = pyodbc.connect(create_connection_string(prototype))
    cursor = cnxn.cursor()
    if len(exclude_certain_weeks) == 0:
        cursor.execute(
            """SELECT id, target, author, timesubmitted, metric1, metric2, metric3, metric4, report, goodcomment, 
            badcomment, weeksubmitted
            FROM feedback 
            WHERE target = ?
            AND weeksubmitted > 1""",
            student_id)
    else:
        placeholders = ", ".join(["?"] * len(exclude_certain_weeks))
        query = """SELECT id, target, author, timesubmitted, metric1, metric2, metric3, metric4, report, goodcomment, 
            badcomment, weeksubmitted
            FROM feedback 
            WHERE target = ?
            AND weeksubmitted > 1 
            AND weeksubmitted NOT IN (""" + placeholders + ")"
        cursor.execute(query, student_id, *exclude_certain_weeks)
    columns = [column[0] for column in cursor.description]
    results = []
    for row in cursor.fetchall():
        results.append(dict(zip(columns, row)))
    cursor.close()
    cnxn.close()

    # Format the results in order to get the averages for each week
    weeks = []
    for result in results:
        weeks.append(result['weeksubmitted'])
    weeks = list(set(weeks))
    weeks_data = []
    for week in weeks:
        week_data = {
            'week': week
        }
        metric_one_avg = 0
        metric_two_avg = 0
        metric_three_avg = 0
        metric_four_avg = 0
        total_avg = 0
        count1 = 0
        count2 = 0
        count3 = 0
        count4 = 0
        for result in results:
            if result['weeksubmitted'] == week:
                if result['metric1'] > 0:
                    metric_one_avg = metric_one_avg + result['metric1']
                    count1 = count1 + 1
                if result['metric2'] > 0:
                    metric_two_avg = metric_two_avg + result['metric2']
                    count2 = count2 + 1
                if result['metric3'] > 0:
                    metric_three_avg = metric_three_avg + result['metric3']
                    count3 = count3 + 1
                if result['metric4'] > 0:
                    metric_four_avg = metric_four_avg + result['metric4']
                    count4 = count4 + 1
        metric_one_avg = float(metric_one_avg) / float(count1)
        metric_two_avg = float(metric_two_avg) / float(count2)
        metric_three_avg = float(metric_three_avg) / float(count3)
        metric_four_avg = float(metric_four_avg) / float(count4)
        total_avg = (metric_one_avg + metric_two_avg + metric_three_avg + metric_four_avg) / 4.0
        week_data['metric1'] = metric_one_avg
        week_data['metric2'] = metric_two_avg
        week_data['metric3'] = metric_three_avg
        week_data['metric4'] = metric_four_avg
        week_data['total'] = float(total_avg)
        weeks_data.append(week_data)

    return weeks_data, {
        'total': get_total_average_for_student(student_id=student_id, prototype=prototype,
                                               exclude_certain_weeks=exclude_certain_weeks),
        'metric1': get_metric_average(student_id=student_id, prototype=prototype, metric_number='1',
                                      exclude_certain_weeks=exclude_certain_weeks),
        'metric2': get_metric_average(student_id=student_id, prototype=prototype, metric_number='2',
                                      exclude_certain_weeks=exclude_certain_weeks),
        'metric3': get_metric_average(student_id=student_id, prototype=prototype, metric_number='3',
                                      exclude_certain_weeks=exclude_certain_weeks),
        'metric4': get_metric_average(student_id=student_id, prototype=prototype, metric_number='4',
                                      exclude_certain_weeks=exclude_certain_weeks),
    }


def get_total_average_for_student(student_id: int, exclude_certain_weeks=None, prototype: bool = False):
    if exclude_certain_weeks is None:
        exclude_certain_weeks = []
    cnxn = pyodbc.connect(create_connection_string(prototype))
    cursor = cnxn.cursor()
    if len(exclude_certain_weeks) == 0:
        cursor.execute(
            """
                SELECT ROUND(CAST(SUM(metric1 + metric2 + metric3 + metric4) AS decimal) / CAST((COUNT(metric1)) * 4 AS decimal),
                    3) as "total average"
                FROM feedback
                WHERE target = ?""",
            student_id)
    else:
        placeholders = ", ".join(["?"] * len(exclude_certain_weeks))
        query = """
                SELECT ROUND(CAST(SUM(metric1 + metric2 + metric3 + metric4) AS decimal) / CAST((COUNT(metric1)) * 4 AS decimal),
                        3) as "total average"

                FROM feedback f
                WHERE target = ? and weeksubmitted not in (""" + placeholders + ")"
        cursor.execute(query, student_id, *exclude_certain_weeks)
    columns = [column[0] for column in cursor.description]
    results = []
    for row in cursor.fetchall():
        results.append(dict(zip(columns, row)))
    cursor.close()
    cnxn.close()
    if results[0]['total average'] is not None:
        return float(results[0]['total average'])
    else:
        return 0.


def get_metric_average(student_id: int, metric_number: str, exclude_certain_weeks=None, prototype: bool = False):
    if exclude_certain_weeks is None:
        exclude_certain_weeks = []
    cnxn = pyodbc.connect(create_connection_string(prototype))
    cursor = cnxn.cursor()
    if len(exclude_certain_weeks) == 0:
        cursor.execute(
            "SELECT ROUND(CAST(SUM(metric" + metric_number + ") AS decimal) / CAST((COUNT(metric" + metric_number + ")) AS decimal),3) as \"metric average\" FROM feedback WHERE target = ?",
            student_id)
    else:
        placeholders = ", ".join(["?"] * len(exclude_certain_weeks))
        query = "SELECT ROUND(CAST(SUM(metric" + metric_number + ") AS decimal) / CAST((COUNT(metric" + metric_number + ")) AS decimal),3) as \"metric average\" FROM feedback WHERE target = ? and weeksubmitted not in (" + placeholders + ")"
        cursor.execute(query, student_id, *exclude_certain_weeks)
    columns = [column[0] for column in cursor.description]
    results = []
    for row in cursor.fetchall():
        results.append(dict(zip(columns, row)))
    cursor.close()
    cnxn.close()
    if results[0]['metric average'] is not None:
        return float(results[0]['metric average'])
    else:
        return 0.
