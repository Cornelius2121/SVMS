from flask import Blueprint, render_template, make_response, jsonify, g
import json

AdminUploadStudentInformation = Blueprint('AdminUploadStudentInformation', __name__)


@AdminUploadStudentInformation.route('/admin/upload-students')
def load_admin_marking():
    return render_template('Admin/GroupManagement/UploadStudentFile.html')
