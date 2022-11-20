from flask import Blueprint, render_template, make_response, jsonify

AdminFeedbackPage = Blueprint('AdminFeedbackPage', __name__)


@AdminFeedbackPage.route('/admin/feedback')
def load_feedback_submission_page():
    return render_template('Admin/Feedback/Feedback.html')
