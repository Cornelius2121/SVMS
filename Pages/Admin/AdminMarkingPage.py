from flask import Blueprint, render_template, make_response, jsonify, g
from Helper.Admin.AdminMarkingHelper import get_marking_selection
from Services.WeekService import get_current_week
import json

AdminMarkingPage = Blueprint('AdminMarkingPage', __name__)


@AdminMarkingPage.route('/admin/marking')
def load_admin_marking():
    marking_selection = json.dumps(get_marking_selection())
    return render_template('Admin/Marking/AdminMarking.html', marking_selection=marking_selection,
                           latest_week=get_current_week())
