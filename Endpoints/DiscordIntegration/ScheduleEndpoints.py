from flask import Blueprint, request, make_response, jsonify
import json
import Services.ScheduleService as Service

DiscordIntegrationScheduleEndpoints = Blueprint('DiscordIntegrationScheduleEndpoints', __name__)


@DiscordIntegrationScheduleEndpoints.route('/schedule/data/<week_number>', methods=['GET'])
def get_schedule_for_week(week_number=1):
    data = Service.select_all_rounds_and_tutorials_from_week(week_number)
    data = json.dumps(data)
    response = make_response(data, 200)
    response.headers["Content-Type"] = "application/json"
    return response
