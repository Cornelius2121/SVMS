from flask import Blueprint, render_template, make_response, jsonify, g
from Services.Admin import UnactionedFeedbackService as Service
import json

UnactionedFeedbackPage = Blueprint('UnactionedFeedbackPage', __name__)


@UnactionedFeedbackPage.route('/admin/unactioned-feedback')
def show_action_feedback():
    unactioned_feedback = Service.select_all_unactioned_feedback()
    for week in unactioned_feedback:
        for unactioned_feedback_item in week['Unactioned Feedback']:
            if unactioned_feedback_item['target'] == None:
                unactioned_feedback_item['target'] = 'Admin'
            if unactioned_feedback_item['author'] == None:
                unactioned_feedback_item['author'] = 'Admin'
    # Force the data into JSON
    unactioned_feedback = json.dumps(unactioned_feedback)

    return render_template('Admin/UNF/Unactioned.html', unactioned_feedback=unactioned_feedback)
