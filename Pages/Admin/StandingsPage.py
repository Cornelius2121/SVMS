from flask import Blueprint, render_template, make_response, jsonify
from Services.StandingsService import get_standings
import json
from Helper.StudentHelper import check_in_group
from config import STATISTICS_WEEKS_TO_EXCLUDE

AdminStandingsPage = Blueprint('AdminStandingsPage', __name__)


@AdminStandingsPage.route('/admin/standings')
def show_stats():
    standings = get_standings(weeks_to_exclude=STATISTICS_WEEKS_TO_EXCLUDE)
    # Force the data into JSON
    standings = json.dumps(standings)
    return render_template('Admin/Standings/Standings.html', standings=standings)
