from flask import Blueprint, render_template, make_response, jsonify, g
from Services.Admin import ReportedFeedbackService as Service
import json

ReportedFeedbackPage = Blueprint('ReportedFeedbackPage', __name__)


@ReportedFeedbackPage.route('/admin/reported-feedback')
def show_reported_feedback():
    reported_feedback = Service.select_all_flagged_comments()
    # Force the data into JSON
    if len(reported_feedback) > 0:
        for fb in reported_feedback:
            if fb['target'] == None:
                fb['target'] = 'Admin'
            if fb['author'] == None:
                fb['author'] = 'Admin'
        reported_feedback = json.dumps(reported_feedback)
    else:
        reported_feedback = json.dumps({
            'Status': 'There is no reported feedback at this time.'
        })
    return render_template('Admin/UNF/Reported.html', reported_feedback=reported_feedback)

