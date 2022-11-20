from flask import Blueprint, render_template, make_response, jsonify, g
import json
from Services import GroupService, StudentService, TutorialService

EditGroupsPage = Blueprint('EditGroupsPage', __name__)


@EditGroupsPage.route('/admin/edit/groups')
def show_edit_groups_page():
    groups = GroupService.select_all_groups_and_students()
    unallocated_students = [{'studentnumber': Student['studentnumber'], 'tutorial': Student['tutorial']} for Student in
                            StudentService.get_all_unallocated_students()]
    tutorials = TutorialService.select_all_active_tutorials(False)
    return render_template('Admin/GroupManagement/EditGroups.html', groups=groups,
                           unallocated_students=unallocated_students, tutorials=tutorials)


@EditGroupsPage.route('/admin/edit/groups/<group_number>', methods=['GET'])
def show_edit_single_group_page(group_number: int):
    group_number = int(group_number)
    all_information = GroupService.select_all_groups_and_students()
    students = []
    active = True
    student_count = 0
    for group in all_information:
        if group['Group ID'] == group_number:
            students.extend(group['Students'])
            active = group['Group Active']
            student_count = group["Student Count"]
    groups = [group['Group ID'] for group in all_information]
    groups.remove(group_number)
    unallocated_students = [Student['studentnumber'] for Student in StudentService.get_all_unallocated_students()]
    return render_template('Admin/GroupManagement/EditSingleGroup.html', group_number=group_number, groups=groups,
                           students=students, group_active=active, unallocated_students=unallocated_students,
                           student_count=student_count)
