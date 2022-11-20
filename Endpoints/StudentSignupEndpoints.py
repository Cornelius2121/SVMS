from flask import Blueprint, request, make_response, jsonify, render_template, g
from Helper.StudentWhitelistDataImportHelper import check_student_number_against_whitelist, create_account
from Helper.StudentHelper import parse_student_number

StudentSignup = Blueprint('StudentSignup', __name__)


@StudentSignup.route('/student/signuppage')
def student_signup_page():
    return render_template('SignUp/signUp.html')


@StudentSignup.route('/student/signup', methods=['POST'])
def student_signup():
    student_number = request.json['studentNumber']
    number_no_c = parse_student_number(student_number)
    # If the patten has not matched, it means that the student number is not in a valid form
    if number_no_c == "-1":
        response = make_response(jsonify({
            'Error': 'Student number did not match the expected format'
        }), 422)
        response.headers["Content-Type"] = "application/json"
        return response
    else:
        if not check_student_number_against_whitelist(number_no_c):
            create_account(number_no_c)
            response = make_response(jsonify({
                'success': True
            }), 200)
            response.headers["Content-Type"] = "application/json"
            return response
        else:
            response = make_response(jsonify({
                'Error': 'The students account could not be created, as it may already have been created or does not exist in account whitelist.'
            }), 422)
            response.headers["Content-Type"] = "application/json"
            return response
