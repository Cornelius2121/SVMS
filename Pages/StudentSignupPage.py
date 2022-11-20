from flask import Blueprint, request, make_response, jsonify, render_template
import json
import Services.StudentService as Service

StudentSignupPage = Blueprint('StudentSignupPage', __name__)


@StudentSignupPage.route('/student/create-account')
def student_signup_page():
    return render_template('SignUp/signUp.html')
