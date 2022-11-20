from flask import Blueprint, render_template, make_response, jsonify, g
from Services.StatsService import select_all_statistics_for_student_id
import json
from Helper.StudentHelper import check_in_group
from config import STATISTICS_WEEKS_TO_EXCLUDE

StatsPage = Blueprint('StatsPage', __name__)


@StatsPage.route('/stats')
def show_stats():
    user = g.userDetails
    student_id = int(user['student_id'])
    stats, averages = select_all_statistics_for_student_id(student_id=student_id,
                                                           exclude_certain_weeks=STATISTICS_WEEKS_TO_EXCLUDE)
    # Force the data into JSON
    stats = json.dumps(stats)
    averages = json.dumps(averages)
    return render_template('Stats/stats.html', stats=stats, student_show_group=check_in_group(), averages=averages)
