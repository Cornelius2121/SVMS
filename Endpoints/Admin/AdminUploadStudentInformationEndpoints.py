from flask import Blueprint, request, make_response, jsonify, g, send_file, render_template
from werkzeug.utils import secure_filename
from datetime import datetime
from flask import current_app
import os
from Helper.Admin.AdminFileUploadHelper import new_file_upload
import re

AdminUploadStudentInformationEndpoints = Blueprint('AdminUploadStudentInformationEndpoints', __name__)


@AdminUploadStudentInformationEndpoints.route('/admin/upload-students/ingest', methods=['POST'])
def ingest_spreadsheet():
    f = request.files['file']
    isExist = os.path.exists(os.path.join(current_app.root_path, 'Uploads'))
    if not isExist:
        os.makedirs(os.path.join(current_app.root_path, 'Uploads'))
    path = os.path.join(current_app.root_path, 'Uploads', secure_filename(get_filename_with_datetime(f.filename)))
    f.save(path)
    number_of_students_changed_tutorials = new_file_upload(path)
    return render_template('Admin/Home/Home.html', admin_username=g.userDetails['username'],
                           student_change_alert=number_of_students_changed_tutorials)


def get_filename_with_datetime(existing_filename: str) -> str:
    now = datetime.now()  # current date and time
    date_time = now.strftime("%m-%d-%Y-%H-%M-%S")
    pattern = "(.+)(\.(?:.(?!\.))+$)"
    matches = re.finditer(pattern, existing_filename)
    string_split = []
    for match in matches:
        string_split.append(match.group(1))
        string_split.append(match.group(2))
    return string_split[0] + date_time + string_split[1]
