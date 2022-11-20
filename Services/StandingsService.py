import pyodbc
from Helper.DatabaseHelper import create_connection_string
from Services import StatsService
import numpy as np


def get_full_standings(prototype: bool = False):
    cnxn = pyodbc.connect(create_connection_string(prototype))
    cursor = cnxn.cursor()
    cursor.execute(
        """SELECT ROW_NUMBER()
                   OVER (ORDER BY ROUND(CAST(SUM(fs.metric1 + fs.metric2 + fs.metric3 + fs.metric4) AS decimal) /
                                        CAST((COUNT(fs.metric1)) AS decimal), 1) desc) AS "Rank",
                   fs.studentgroup                                                     AS "Group",
                   ROUND(CAST(SUM(fs.metric1 + fs.metric2 + fs.metric3 + fs.metric4) AS decimal) /
                         CAST((COUNT(fs.metric1)) AS decimal), 3)                      AS "Score"
            FROM (SELECT fb.metric1, fb.metric2, fb.metric3, fb.metric4, fb.studentgroup
                  FROM (SELECT fb.metric1, fb.metric2, fb.metric3, fb.metric4, s.studentgroup, s.id as "target", fb.author
                        FROM feedback fb
                                 LEFT JOIN student s on fb.target = s.id
                        WHERE weeksubmitted > 1) AS fb
                           LEFT JOIN student ss on fb.author = ss.id
                  WHERE ss.studentgroup != fb.studentgroup) as fs
            WHERE fs.studentgroup IS NOT NULL
            
            GROUP BY fs.studentgroup
            ORDER BY "Score" desc;
        """)
    columns = [column[0] for column in cursor.description]
    results = []
    for row in cursor.fetchall():
        # Hot fix for decimal issue with standing
        row[2] = float(row[2])

        results.append(dict(zip(columns, row)))
    cursor.close()
    cnxn.close()
    return results


def get_standings(prototype: bool = False, weeks_to_exclude=None):
    if weeks_to_exclude is None:
        weeks_to_exclude = []
    cnxn = pyodbc.connect(create_connection_string(prototype))
    cursor = cnxn.cursor()
    cursor.execute(
        """
        SELECT id
        FROM studentgroup WHERE groupactive = B'1'
        """)
    columns = [column[0] for column in cursor.description]
    results = []
    for row in cursor.fetchall():
        results.append(dict(zip(columns, row)))
    student_groups = results
    groups = []
    for sg in student_groups:
        sg = sg['id']
        cursor.execute(
            """
            SELECT id
            FROM student WHERE studentgroup = ?
            """, sg)
        columns = [column[0] for column in cursor.description]
        results = []
        for row in cursor.fetchall():
            results.append(dict(zip(columns, row)))
        group = {
            'groupid': sg,
            'students': [],
            'score': 0
        }
        for res in results:
            group['students'].append(res['id'])
        groups.append(group)
    for group in groups:
        for student in group['students']:
            group['score'] += StatsService.get_total_average_for_student(student,
                                                                         exclude_certain_weeks=weeks_to_exclude)
    groups = sorted(groups, key=lambda i: i['score'], reverse=True)
    count = 0
    for group in groups:
        count = count + 1
        group['rank'] = count
    standings = []
    for group in groups:
        standings.append({
            'Rank': group['rank'],
            'Score': np.round(group['score'], 3),
            'Group': group['groupid']
        })
    cursor.close()
    cnxn.close()
    for st in standings:
        st['Rank'] = int(st['Rank'])
        st['Group'] = int(st['Group'])
        st['Score'] = float(st['Score'])
    return standings
