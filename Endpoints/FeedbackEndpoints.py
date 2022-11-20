from flask import Blueprint, request, make_response, jsonify, g
from flask_cors import cross_origin
import re

import Services.ScheduleService
from Helper.StudentHelper import parse_student_number
from config import METRIC_COUNT as METRICS
from Services import FeedbackService as Service
from Services import StudentService
from Services import WeekService
from datetime import timedelta
import pytz
import datetime

FeedbackEndpoints = Blueprint('FeedbackEndpoints', __name__)


@FeedbackEndpoints.route('/feedback/submission', methods=['POST'])
def submit_feedback():
    content = request.form
    user = g.userDetails
    student_id = int(user['student_id'])
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
        try:
            target_id = StudentService.select_student_from_student_number(number_no_c)[0]['id']
        # This means that the target does not exist in the database
        except IndexError as e:
            response = make_response(jsonify({
                'Error': 'Target student number does not exist in the database'
            }), 422)
            response.headers["Content-Type"] = "application/json"
            return response
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
        good_comment = good_comment.replace("\t", " ")
        # Bad comment
        bad_comment = content['NegativeComment']
        # Clean data for bad comment
        bad_comment = bad_comment.replace('\'', '')
        bad_comment = bad_comment.replace('\"', '')
        bad_comment = bad_comment.replace('}', '')
        bad_comment = bad_comment.replace('{', '')

        bad_comment = re.sub('[^a-zA-Z.\d\s]', '', bad_comment)
        bad_comment = bad_comment.replace("\n", " ")
        bad_comment = bad_comment.replace("\t", " ")


        # Get the current week
        week = Services.WeekService.get_current_week()
        time = datetime.datetime.now(tz=pytz.timezone('Australia/Sydney'))
        Service.insert_new_feedback(metrics=metrics, goodcomment=good_comment, badcomment=bad_comment,
                                    submitter=student_id, target=target_id, time=time, week=week)
        response = make_response(jsonify({
            'success': True
        }), 200)
        response.headers["Content-Type"] = "application/json"
        return response


@FeedbackEndpoints.route('/feedback/check-number', methods=['POST'])
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
        week = WeekService.get_current_week()
        user = g.userDetails
        student_id = int(user['student_id'])
        student_group = StudentService.select_group_from_student_id(student_id)[0]['studentgroup']
        if student_group == None:
            response = make_response(jsonify({
                'Error': 'You are not a member of group yet, and therefore cannot submit feedback!'
            }), 422)
            response.headers["Content-Type"] = "application/json"
            return response
        debates = Services.ScheduleService.select_debate_from_group_number_and_week(week=week, group=student_group)
        groups = []
        for debate in debates:
            groups.append(debate['groupx'])
            groups.append(debate['groupy'])
        groups = list(set(groups))
        students = []
        for group in groups:
            current_students = StudentService.select_all_students_student_numbers_in_group(group_id=group)
            for student in current_students:
                students.append(student['studentnumber'])
        if len(debates) != 0:
            students.remove(StudentService.select_student_number_from_student_id(student_id)[0]['studentnumber'])
            if target_student_number in students:
                response = make_response(jsonify({
                    'Available Student': True
                }), 200)
                response.headers["Content-Type"] = "application/json"
                return response
            else:
                response = make_response(jsonify({
                    'Available Student': False
                }), 200)
                response.headers["Content-Type"] = "application/json"
                return response
        else:
            response = make_response(jsonify({
                'Available Student': False
            }), 200)
            response.headers["Content-Type"] = "application/json"
            return response