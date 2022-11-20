from flask import Blueprint, request, make_response, jsonify
import json
from Services.Admin.UnactionedFeedbackService import insert_new_admin_actioned_feedback
import datetime, pytz

UnactionedFeedbackEndpoints = Blueprint('UnactionedFeedbackEndpoints', __name__)


@UnactionedFeedbackEndpoints.route('/admin/unactioned-feedback/submit', methods=['POST'])
def submit_unactioned_feedback():
    try:
        content = request.json
        for action in content:
            action['timesubmitted'] = datetime.datetime.now(tz=pytz.timezone('Australia/Sydney'))
        insert_new_admin_actioned_feedback(list(content))
        response = make_response(jsonify({
            'Status': 'Submission Successful'
        }), 200)
        response.headers["Content-Type"] = "application/json"
        return response
    except Exception as e:
        response = make_response(jsonify({
            'Status': 'Submission Failed'
        }), 422)
        response.headers["Content-Type"] = "application/json"
        return response
