import re
from flask import g
import Services


def parse_student_number(input: str) -> str:
    number_no_c = "-1"
    # Use some regex to see if the student number is in c form or not
    if re.match(r"^[c]\d{7}$", input):
        number_no_c = input.split('c')[1]
    elif re.match(r"^[C]\d{7}$", input):
        number_no_c = input.split('C')[1]
    elif re.match(r"^\d{7}$", input):
        number_no_c = input
    return number_no_c


def check_in_group():
    user = g.userDetails
    if user['group_id'] == None:
        group_number = Services.StudentService.select_group_from_student_id(user['student_id'])[0]['studentgroup']
    else:
        group_number = user['group_id']
    if group_number is not None:
        # This is returning false, as there is no need to show the signup page in the menu
        return False
    else:
        return True
