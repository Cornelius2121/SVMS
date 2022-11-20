import pyodbc
from Helper.DatabaseHelper import create_connection_string
from Services.ActionFeedbackService import update_feedback_table_for_actioned_feedback


def insert_new_admin_actioned_feedback(feedback: list, prototype: bool = False):
    cnxn = pyodbc.connect(create_connection_string(prototype))
    cursor = cnxn.cursor()
    sql = """INSERT INTO actionfeedback (feedbackid, goodcommentreaction, badcommentreaction, timesubmitted, adminactioned) 
        VALUES (?, ?, ?, ?, ?)"""
    feedback_ids = []
    for feedback_item in feedback:
        # create list of feedback ids, in order for the feedback table to be updated
        feedback_ids.append(feedback_item['id'])
        cursor.execute(sql, feedback_item['id'], feedback_item['goodcomment'], feedback_item['badcomment'],
                       feedback_item['timesubmitted'], True)
    cursor.commit()
    cursor.close()
    cnxn.close()
    # update the feedback table
    update_feedback_table_for_actioned_feedback(feedback_ids)


def select_all_unactioned_feedback(format_output=True, prototype: bool = False):
    sql = """SELECT NoTargetFeedback.id,
       st.studentnumber as "target",
       st.id as "target_id",
       NoTargetFeedback.author,
       NoTargetFeedback.author_id,
       NoTargetFeedback.timesubmitted,
       NoTargetFeedback.metric1,
       NoTargetFeedback.metric2,
       NoTargetFeedback.metric3,
       NoTargetFeedback.metric4,
       NoTargetFeedback.report,
       NoTargetFeedback.goodcomment,
       NoTargetFeedback.badcomment,
       NoTargetFeedback.weeksubmitted,
       NoTargetFeedback.actionfeedbackrecorded
FROM (SELECT f.id,
             f.target,
             s.studentnumber as "author",
             s.id as "author_id",
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
      WHERE actionfeedbackrecorded = B'0'
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
        # {'id': 2, 'target': 1, 'author': 3, 'timesubmitted': datetime.datetime(2021, 7, 18, 15, 44, 44), 'metric1': 2,
        # 'metric2': 3, 'metric3': 2, 'metric4': 1, 'report': '0', 'goodcomment': 'You were good at metric 4',
        # 'badcomment': 'This was still a very poor presentation and you need to do more work',
        # 'weeksubmitted': 1, 'actionfeedbackrecorded': '0'}
        weeks = []
        for result in results:
            result['timesubmitted'] = str(result['timesubmitted'])
            weeks.append(result['weeksubmitted'])
        weeks = list(set(weeks))
        weeks_data = []
        for week in weeks:
            current_week = {
                'Week': week,
                'Unactioned Feedback': []
            }
            for result in results:
                if result['weeksubmitted'] == week:
                    current_week['Unactioned Feedback'].append(result)
            weeks_data.append(current_week)
        for week in weeks_data:
            for fb in week['Unactioned Feedback']:
                del fb['weeksubmitted']
                del fb['actionfeedbackrecorded']
        return weeks_data
