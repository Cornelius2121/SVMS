from flask import Blueprint, render_template, make_response, jsonify
from Services.StandingsService import get_standings
import json
from Helper.StudentHelper import check_in_group
from config import STATISTICS_WEEKS_TO_EXCLUDE

StandingsPage = Blueprint('StandingsPage', __name__)


@StandingsPage.route('/standings')
def show_stats():
    standings = get_standings(weeks_to_exclude=STATISTICS_WEEKS_TO_EXCLUDE)
    # Force the data into JSON
    standings = json.dumps(standings)
    return render_template('Standing/Standing.html', standings=standings,
                           student_show_group=check_in_group())
