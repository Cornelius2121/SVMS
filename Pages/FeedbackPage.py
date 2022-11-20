from flask import Blueprint, render_template, make_response, jsonify

from Helper.StudentHelper import check_in_group

FeedbackPage = Blueprint('FeedbackPage', __name__)


@FeedbackPage.route('/feedback')
def load_feedback_submission_page():
    return render_template('feedback/Feedback.html', student_show_group=check_in_group())
