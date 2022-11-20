from flask import Blueprint, jsonify, make_response, request, render_template
import censusname

TutroialPage = Blueprint('TutorialPage', __name__)


@TutroialPage.route('/index')
def index():
    # generate random names
    student_names = [censusname.generate() for student in range(20)]
    groups = [
        {
            'group_number': 1,
            'group_members': list(student_names[0:4])
        },
        {
            'group_number': 2,
            'group_members': list(student_names[4:8])
        },
        {
            'group_number': 3,
            'group_members': list(student_names[8:12])
        },
        {
            'group_number': 4,
            'group_members': list(student_names[12:16])
        },
        {
            'group_number': 5,
            'group_members': list(student_names[16:])
        }]
    return render_template('Tutorial/Tutorial.html', tutorial_number='Home', students=student_names, groups=groups)
