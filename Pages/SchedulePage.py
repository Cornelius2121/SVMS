import logging
from flask import Blueprint, render_template, make_response, jsonify, g
from Helper.GenerateDebateScheduleHelper import GenerateDebateScheduleHelper as generate_schedule
from Services import ScheduleService as Service
from Services import StudentService as SService
from Helper.StudentHelper import check_in_group
import json

SchedulePage = Blueprint('SchedulePage', __name__)


@SchedulePage.route('/full-tutorial-schedule')
def full_schedule():
    handler = generate_schedule(1, False)
    handler.create_all_tutorial_one_weeks_round()
    handler.schedule_to_database()
    full_schedule = Service.select_all_rounds_for_tutorial_and_week(1, 1)
    # Force the data into JSON
    schedule_json = json.dumps(full_schedule)
    return render_template('Schedule/Schedule.html', week_number=1, full_schedule=full_schedule)


@SchedulePage.route('/schedule/tutorial', methods=['GET'])
def schedule_from_tutorial():
    user = g.userDetails
    try:
        tutorial_number = int(user['tutorial_id'])
    except Exception as e:
        return render_template('Schedule/TutorialSchedule.html',
                               student_show_group=check_in_group())
    # schedule = Service.select_all_rounds_from_tutorial_and_current_week(tutorial=int(tutorial_number))
    schedule = Service.select_all_rounds_from_tutorial(tutorial=int(tutorial_number))
    try:
        if user['group_id'] == None:
            group_number = SService.select_group_from_student_id(user['student_id'])[0]['studentgroup']
        else:
            group_number = user['group_id']
        if group_number == None:
            raise Exception("No Group ID")
    except Exception as e:
        return render_template('Schedule/TutorialSchedule.html',
                               student_show_group=check_in_group())

    if len(schedule) < 1:
        logging.error("The schedule was not returned from the database and had no results.")
        response = make_response(jsonify({
            'Error': 'Schedule Not Found'
        }), 400)
        response.headers["Content-Type"] = "application/json"
        return render_template('Schedule/TutorialSchedule.html',
                               student_show_group=check_in_group())
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
        return render_template('Schedule/TutorialSchedule.html', JSONData=schedule_json,
                               tutorial_number=tutorial_number, group_number=group_number,
                               student_show_group=check_in_group())
