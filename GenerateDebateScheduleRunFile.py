from Helper.GenerateDebateScheduleHelper import GenerateDebateScheduleHelper
from config import SCHEDULE_UPDATE_EMAIL
from Helper.AutomatedScheduleHelper import send_email


def run_schedule_generation():
    generate = GenerateDebateScheduleHelper(db_prototype=False)
    generate.create_all_tutorial_one_weeks_round()
    generate.schedule_to_database()
    # Validate with email to admins
    for email in SCHEDULE_UPDATE_EMAIL:
        send_email(email, int(generate.week_number))


if __name__ == '__main__':
    run_schedule_generation()
