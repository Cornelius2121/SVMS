from flask import Blueprint, request, make_response, jsonify
import json
import Services.StudentService as Service

DiscordIntegrationStudentEndpoints = Blueprint('DiscordIntegrationStudentEndpoints', __name__)


@DiscordIntegrationStudentEndpoints.route('/student/data', methods=['GET'])
def get_schedule_for_week():
    data = Service.get_all_student_numbers_with_c_group_numbers_and_formatted_tutorial_day_and_time()
    results = {}
    for result in data:
        results[result['Student Number']] = {
            "Group Number": result['Group Number'],
            "Tutorial": result["Tutorial"]
        }
    data = json.dumps(results)
    response = make_response(data, 200)
    response.headers["Content-Type"] = "application/json"
    return response
