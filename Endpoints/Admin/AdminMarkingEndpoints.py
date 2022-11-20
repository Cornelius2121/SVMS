from flask import Blueprint, request, make_response, jsonify, g, send_file
from Helper.Admin.AdminMarkingHelper import get_marking_selection, marking
import csv
import pandas as pd
import datetime
import pytz
from config import GENERATED_MARKING_PATH

AdminMarkingEndpoints = Blueprint('AdminMarkingEndpoints', __name__)


@AdminMarkingEndpoints.route('/admin/marking/generate', methods=['POST'])
def generate_marking():
    content = request.json
    columns = content['Columns']
    week = int(content['Week'])
    submitted_keys = [key for key, value in columns.items()]
    actual_marking_selection = get_marking_selection()
    invalid = False
    for key, value in actual_marking_selection.items():
        if key not in submitted_keys:
            invalid = True
    if invalid:
        response = make_response(jsonify({
            'Error': 'The format of the submitted keys is not correct'
        }), 400)
    else:
        marker = marking(week=week)
        data = pd.DataFrame(marker.run_selection(marking_selection=columns))
        tz = pytz.timezone('Australia/Sydney')
        sydney_now = datetime.datetime.now(tz)
        filename = f'Generated_Marking_{sydney_now.strftime("%d%m%Y-%H %M %S")}.csv'
        csv_data = data.to_csv(f'{GENERATED_MARKING_PATH}\\{filename}')
        return send_file(path_or_file=(f'{GENERATED_MARKING_PATH}\\{filename}'), as_attachment=True,
                         download_name=filename)
