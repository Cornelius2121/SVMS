from flask import Blueprint, render_template, make_response, jsonify, g
from Services.ActionFeedbackService import select_all_unactioned_feedback_from_student_id
from Services.ActionFeedbackService import select_all_historical_action_feedback
import json
from Helper.StudentHelper import check_in_group

ActionFeedbackPage = Blueprint('ActionFeedbackPage', __name__)


@ActionFeedbackPage.route('/feedback/action-feedback')
def show_action_feedback():
    user = g.userDetails
    student_id = int(user['student_id'])
    comments = select_all_unactioned_feedback_from_student_id(student_id=student_id)
    # Force the data into JSON
    comments = json.dumps(comments).replace('\\t', ' ')
    return render_template('Review/ActionFeedback.html', comments=comments, student_show_group=check_in_group())


@ActionFeedbackPage.route('/feedback/action-feedback/historical')
def show_historical_action_feedback():
    user = g.userDetails
    student_id = int(user['student_id'])
    comments = select_all_historical_action_feedback(student_id=student_id)
    # Force the data into JSON
    comments = json.dumps(comments).replace('\\t', ' ')
    return render_template('Review/ActionFeedbackHistory.html', comments=comments, student_show_group=check_in_group())
