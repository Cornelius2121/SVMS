import pyodbc
from Helper.DatabaseHelper import create_connection_string


def select_all_unactioned_feedback_from_student_id(student_id: int, prototype: bool = False):
    cnxn = pyodbc.connect(create_connection_string(prototype))
    cursor = cnxn.cursor()
    cursor.execute(
        """SELECT id, goodcomment, badcomment FROM feedback 
        WHERE actionfeedbackrecorded = B'0' 
        AND target = ?""",
        student_id)
    columns = [column[0] for column in cursor.description]
    results = []
    for row in cursor.fetchall():
        results.append(dict(zip(columns, row)))
    cursor.close()
    cnxn.close()
    feedback = []
    for result in results:
        current_feedback = {
            'id': result['id'],
            'goodcomment': result['goodcomment'],
            'badcomment': result['badcomment']
        }
        feedback.append(current_feedback)
    return feedback


def insert_actioned_feedback(feedback: list, prototype: bool = False):
    cnxn = pyodbc.connect(create_connection_string(prototype))
    cursor = cnxn.cursor()
    sql = """INSERT INTO actionfeedback (feedbackid, goodcommentreaction, badcommentreaction, timesubmitted) 
    VALUES (?, ?, ?, ?)"""
    feedback_ids = []
    for feedback_item in feedback:
        # create list of feedback ids, in order for the feedback table to be updated
        feedback_ids.append(feedback_item['id'])
        cursor.execute(sql, feedback_item['id'], feedback_item['goodcomment'], feedback_item['badcomment'],
                       feedback_item['timesubmitted'])
    cursor.commit()
    cursor.close()
    cnxn.close()
    feedback_for_flag = []
    for fb_item in feedback:
        if fb_item['goodcomment'] == '4' or fb_item['badcomment'] == '4':
            feedback_for_flag.append(int(fb_item['id']))

    # update the feedback table
    update_feedback_table_for_actioned_feedback(feedback_ids)
    if len(feedback_for_flag) > 0:
        update_feedback_to_be_flagged(feedback_for_flag)



def update_feedback_table_for_actioned_feedback(feedback_ids: list, prototype: bool = False):
    cnxn = pyodbc.connect(create_connection_string(prototype))
    cursor = cnxn.cursor()
    sql = """UPDATE feedback SET actionfeedbackrecorded = B'1' WHERE id = ?"""
    for id in feedback_ids:
        cursor.execute(sql, id)
    cursor.commit()
    cursor.close()
    cnxn.close()


def select_all_historical_action_feedback(student_id: int, prototype: bool = False):
    cnxn = pyodbc.connect(create_connection_string(prototype))
    cursor = cnxn.cursor()
    cursor.execute(
        """SELECT f.id, f.goodcomment, afb.goodcommentreaction, f.badcomment, afb.badcommentreaction, f.weeksubmitted
            FROM actionfeedback afb
            LEFT JOIN feedback f on f.id = afb.feedbackid and f.target = ?
        ORDER BY f.weeksubmitted asc""",
        student_id)
    columns = [column[0] for column in cursor.description]
    results = []
    for row in cursor.fetchall():
        results.append(dict(zip(columns, row)))
    cursor.close()
    cnxn.close()
    weeks = []
    for result in results:
        weeks.append(result['weeksubmitted'])
    weeks = list(set(weeks))
    comments = []
    for week in weeks:
        current_week = {
            'Week': week,
            "Week Comments": []
        }
        for result in results:
            if result['weeksubmitted'] == week:
                current_comment = {
                    "id": result['id'],
                    "good": {
                        "goodcomment": result['goodcomment'],
                        "goodcomment_score": result['goodcommentreaction']
                    },
                    "bad": {
                        "badcomment": result['badcomment'],
                        "badcomment_score": result['badcommentreaction']
                    }
                }
                current_week["Week Comments"].append(current_comment)
        comments.append(current_week)
    return comments


def update_feedback_to_be_flagged(ids: list, prototype: bool = False):
    cnxn = pyodbc.connect(create_connection_string(prototype))
    cursor = cnxn.cursor()
    sql = """UPDATE feedback SET report = B'1' WHERE id = ?"""
    for id in ids:
        cursor.execute(sql, id)
    cursor.commit()
    cursor.close()
    cnxn.close()