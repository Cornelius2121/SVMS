from flask import Blueprint, request, make_response, jsonify, g, send_file, render_template
from Services import GroupService, StudentService
from Helper.Admin import AdminGroupManagerHelper

AdminEditGroupsEndpoints = Blueprint('AdminEditGroupsEndpoints', __name__)


@AdminEditGroupsEndpoints.route('/admin/edit/student', methods=['POST'])
def edit_student():
    content = request.json
    existing_group = GroupService.select_group_from_id(content['Old Group'])[0]
    existing_tutorial = existing_group['tutorial']
    new_group = GroupService.select_group_from_id(content['New Group'])[0]
    new_tutorial = new_group['tutorial']
    if existing_tutorial != new_tutorial:
        AdminGroupManagerHelper.change_tutorial_and_group(content['Student'], new_tutorial, content['New Group'])
    else:
        AdminGroupManagerHelper.change_group(content['Student'], content['New Group'])
    response = make_response(jsonify({
        'Status': 'Submission Successful'
    }), 200)
    response.headers["Content-Type"] = "application/json"
    return response


@AdminEditGroupsEndpoints.route('/admin/edit/student/unallocated', methods=['POST'])
def add_unallocated_student():
    content = request.json
    student_information = StudentService.select_student_from_student_number(content['Student'])[0]
    existing_tutorial = student_information['tutorial']
    new_group = GroupService.select_group_from_id(content['New Group'])[0]
    new_tutorial = new_group['tutorial']
    if existing_tutorial != new_tutorial:
        AdminGroupManagerHelper.change_only_tutorial(content['Student'], new_tutorial)
        AdminGroupManagerHelper.add_student_to_group(student_information['id'], content['New Group'])
    else:
        AdminGroupManagerHelper.add_student_to_group(student_information['id'], content['New Group'])
    response = make_response(jsonify({
        'Status': 'Submission Successful'
    }), 200)
    response.headers["Content-Type"] = "application/json"
    return response


@AdminEditGroupsEndpoints.route('/admin/edit/group/active', methods=['POST'])
def edit_group_status():
    content = request.json
    GroupService.update_groups_active_status(content['Group ID'], content['Change Value'])
    response = make_response(jsonify({
        'Status': 'Submission Successful'
    }), 200)
    response.headers["Content-Type"] = "application/json"
    return response


@AdminEditGroupsEndpoints.route('/admin/create/group', methods=['POST'])
def create_group():
    content = request.json
    GroupService.create_group(int(content['Tutorial']))
    response = make_response(jsonify({
        'Status': 'Submission Successful'
    }), 200)
    response.headers["Content-Type"] = "application/json"
    return response
