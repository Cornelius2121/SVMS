from flask import Blueprint, render_template, make_response, jsonify, g
from Helper.StudentHelper import check_in_group

import Services.StudentService
from Services import ActionFeedbackService, StudentService
import json

MenuPage = Blueprint('MenuPage', __name__)


@MenuPage.route('/home')
def show_menu():
    user = g.userDetails
    student_number = user['studentNumber']
    if user['group_id'] == None:
        group_number = Services.StudentService.select_group_from_student_id(user['student_id'])[0]['studentgroup']
    else:
        group_number = user['group_id']
    tutorial_number = user['tutorial_id']
    return render_template('Home/Home.html', student_number=student_number, group_number=group_number,
                           tutorial_number=tutorial_number,
                           pending_action_feedback=check_pending_action_feedback(student_number),
                           student_show_group=check_in_group())


def check_pending_action_feedback(student_number: str) -> bool:
    results = ActionFeedbackService.select_all_unactioned_feedback_from_student_id(
        StudentService.select_student_id_from_student_number(student_number)[0]['id'])
    if len(results) > 0:
        return True
    else:
        return False
