from flask import Blueprint, render_template, make_response, jsonify, request
import datetime
import pytz
from Services.ActionFeedbackService import insert_actioned_feedback
import json
ActionFeedbackEndpoints = Blueprint('ActionFeedbackEndpoints', __name__)


@ActionFeedbackEndpoints.route('/feedback/action-feedback/record', methods=['POST'])
def record_action_feedback():
    content = request.json['Comments']
    for comment in content:
        comment['timesubmitted'] = datetime.datetime.now(tz=pytz.timezone('Australia/Sydney'))
    insert_actioned_feedback(content)
    response = make_response(jsonify({
        'Update Completed': True
    }), 200)
    response.headers["Content-Type"] = "application/json"
    return response
