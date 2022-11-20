import pyodbc
from Helper.DatabaseHelper import create_connection_string


def select_all_flagged_comments(format_output=True, prototype: bool = False):
    sql = """SELECT NoTargetFeedback.id,
                   st.studentnumber as "target",
                   NoTargetFeedback.author,
                   NoTargetFeedback.timesubmitted,
                   NoTargetFeedback.metric1,
                   NoTargetFeedback.metric2,
                   NoTargetFeedback.metric3,
                   NoTargetFeedback.metric4,
                   NoTargetFeedback.report,
                   NoTargetFeedback.goodcomment,
                   NoTargetFeedback.badcomment,
                   NoTargetFeedback.weeksubmitted
            FROM (SELECT f.id,
                         f.target,
                         s.studentnumber as "author",
                         s.id            as "author_id",
                         f.timesubmitted,
                         f.metric1,
                         f.metric2,
                         f.metric3,
                         f.metric4,
                         f.report,
                         f.goodcomment,
                         f.badcomment,
                         f.weeksubmitted,
                         f.actionfeedbackrecorded
                  FROM feedback f
                           LEFT JOIN student s ON f.author = s.id
                  WHERE report = B'1'
                  ORDER BY weeksubmitted, target) as NoTargetFeedback
                     LEFT JOIN student st ON NoTargetFeedback.target = st.id"""
    cnxn = pyodbc.connect(create_connection_string(prototype))
    cursor = cnxn.cursor()
    cursor.execute(sql)
    columns = [column[0] for column in cursor.description]
    results = []
    for row in cursor.fetchall():
        results.append(dict(zip(columns, row)))
    cursor.close()
    cnxn.close()
    if not format_output:
        return results
    else:
        for result in results:
            result['timesubmitted'] = str(result['timesubmitted'])
        return results

