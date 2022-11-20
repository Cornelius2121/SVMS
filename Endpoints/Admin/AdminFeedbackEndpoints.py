from flask import Blueprint, request, make_response, jsonify, g
from flask_cors import cross_origin
import re

import Services.ScheduleService
from Services.ActionFeedbackService import insert_actioned_feedback
from Helper.StudentHelper import parse_student_number
from config import METRIC_COUNT as METRICS
from Services import FeedbackService as Service
from Services import StudentService
from Services import WeekService
from datetime import timedelta
import pytz
import datetime

AdminFeedbackEndpoints = Blueprint('AdminFeedbackEndpoints', __name__)


@AdminFeedbackEndpoints.route('/admin/feedback/submission', methods=['POST'])
def submit_feedback():
    content = request.form
    target_student_id = content['Student']  # This is the student to which the feedback is about
    number_no_c = parse_student_number(target_student_id)
    # If the patten has not matched, it means that the student number is not in a valid form
    if number_no_c == "-1":
        response = make_response(jsonify({
            'Error': 'Student number did not match the expected format'
        }), 422)
        response.headers["Content-Type"] = "application/json"
        return response
    else:
        # Make the target student number into a database id
        target_id = StudentService.select_student_from_student_number(number_no_c)[0]['id']
        metrics = []
        for i in range(1, METRICS + 1):
            metrics.append(content['Metric ' + str(i)])
        # Good comment
        good_comment = content['PositiveComment']
        # Clean data for good comment
        good_comment = good_comment.replace('\'', '')
        good_comment = good_comment.replace('\"', '')
        good_comment = good_comment.replace('}', '')
        good_comment = good_comment.replace('{', '')

        good_comment = re.sub('[^a-zA-Z.\d\s]', '', good_comment)
        good_comment = good_comment.replace("\n", " ")
        # Bad comment
        bad_comment = content['NegativeComment']
        # Clean data for bad comment
        bad_comment = bad_comment.replace('\'', '')
        bad_comment = bad_comment.replace('\"', '')
        bad_comment = bad_comment.replace('}', '')
        bad_comment = bad_comment.replace('{', '')

        bad_comment = re.sub('[^a-zA-Z.\d\s]', '', bad_comment)
        bad_comment = bad_comment.replace("\n", " ")

        # Get the current week
        week = Services.WeekService.get_current_week()
        time = datetime.datetime.now(tz=pytz.timezone('Australia/Sydney'))
        Service.insert_new_feedback(metrics=metrics, goodcomment=good_comment, badcomment=bad_comment,
                                    submitter=-1, target=target_id, time=time, week=week)
        response = make_response(jsonify({
            'success': True
        }), 200)
        response.headers["Content-Type"] = "application/json"
        return response


@AdminFeedbackEndpoints.route('/admin/feedback/check-number', methods=['POST'])
def check_student_number_whitelist():
    content = request.form
    target_student_number = parse_student_number(content['Student Number'])
    number_no_c = parse_student_number(target_student_number)
    # If the patten has not matched, it means that the student number is not in a valid form
    if number_no_c == "-1":
        response = make_response(jsonify({
            'Error': 'Student number did not match the expected format'
        }), 422)
        response.headers["Content-Type"] = "application/json"
        return response
    else:
        # Make the target student number into a database id
        try:
            target_id = StudentService.select_student_from_student_number(number_no_c)[0]['id']
        # This means that the target does not exist in the database
        except IndexError as e:
            response = make_response(jsonify({
                'Error': 'Target student number does not exist in the database'
            }), 422)
            response.headers["Content-Type"] = "application/json"
            return response
        response = make_response(jsonify({
            'Available Student': True
        }), 200)
        response.headers["Content-Type"] = "application/json"
        return response


@AdminFeedbackEndpoints.route('/admin/feedback/action-feedback/record', methods=['POST'])
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
