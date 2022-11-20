from flask import Blueprint, render_template, make_response, jsonify, g
import json

AdminHomePage = Blueprint('AdminHomePage', __name__)


@AdminHomePage.route('/admin/home')
def show_admin_menu():
    return render_template('Admin/Home/Home.html', admin_username=g.userDetails['username'], student_change_alert=0)
