import logging
from flask import Blueprint, render_template, make_response, jsonify, g
from Helper.GenerateDebateScheduleHelper import GenerateDebateScheduleHelper as generate_schedule
from Services import ScheduleService as Service
from Services import StudentService as SService
from Helper.StudentHelper import check_in_group
import json

AdminSchedulePage = Blueprint('AdminSchedulePage', __name__)


@AdminSchedulePage.route('/admin/schedule')
def schedule_from_tutorial():
    schedule = Service.select_all_tutorials_for_all_weeks()

    if len(schedule) < 1:
        logging.error("The schedule was not returned from the database and had no results.")
        response = make_response(jsonify({
            'Error': 'Schedule Not Found'
        }), 400)
        response.headers["Content-Type"] = "application/json"
        return render_template('Admin/Schedule/Schedule.html')
    else:
        for week in schedule:
            for tutorial in week['tutorials']:
                for round in tutorial['rounds']:
                    for debate in round['debates']:
                        if debate['group x'] == None:
                            debate['group x'] = 'Admin'
                        if debate['group y'] == None:
                            debate['group y'] = 'Admin'
        schedule_json = str(json.dumps(schedule))
        return render_template('Admin/Schedule/Schedule.html', JSONData=schedule_json)
