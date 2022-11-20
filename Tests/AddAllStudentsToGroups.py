from flask import Blueprint, request, make_response, jsonify
from Services import GroupService, StudentService
from Helper.StudentHelper import parse_student_number
import Services


def main():
    all_students = StudentService.select_all_students()
    tut2 = []
    tut3 = []
    for student in all_students:
        if student['tutorial'] == 2:
            tut2.append(student)
        else:
            tut3.append(student)
    while len(tut2) > 4:
        a = tut2.pop(0)['studentnumber']
        b = tut2.pop(0)['studentnumber']
        c = tut2.pop(0)['studentnumber']
        d = tut2.pop(0)['studentnumber']
        content = {
            'StudentA': a,
            'StudentB': b,
            'StudentC': c,
            'StudentD': d
        }
        print(addgroup(content))
    while len(tut3) > 4:
        a = tut3.pop(0)['studentnumber']
        b = tut3.pop(0)['studentnumber']
        c = tut3.pop(0)['studentnumber']
        d = tut3.pop(0)['studentnumber']
        content = {
            'StudentA': a,
            'StudentB': b,
            'StudentC': c,
            'StudentD': d
        }
        print(addgroup(content))


def addgroup(content):
    students = [content['StudentA'], content['StudentB'], content['StudentC'], content['StudentD']]
    new_students = []
    for student in students:
        new_student_number = parse_student_number(student)
        if new_student_number == "-1":
            response = make_response(jsonify({
                'Error': 'Student number did not match the expected format'
            }), 422)
            response.headers["Content-Type"] = "application/json"
            return response
        else:
            new_students.append(new_student_number)
    students = new_students
    new_students = []
    for student in students:
        try:
            students_id = Services.StudentService.select_student_from_student_number(student)[0]['id']
            new_students.append(students_id)
        except Exception as e:
            response = make_response(jsonify({
                'Error': f'Student number {student} is not found within the database'
            }), 422)
            response.headers["Content-Type"] = "application/json"
            return response
    # Students is now a list of the student ids
    students = new_students
    tutorials = []
    for student in students:
        tutorials.append(Services.StudentService.select_student_tutorial_from_student_id(student)[0]['tutorial'])
    tutorials = set(tutorials)
    tutorials = list(tutorials)
    if len(tutorials) > 1:
        response = make_response(jsonify({
            'Error': f'All students do not share the same tutorial'
        }), 422)
        response.headers["Content-Type"] = "application/json"
        return response
    tutorial_id = int(tutorials[0])
    for student in students:
        if not Services.StudentService.check_student_group_from_student_id(student):
            response = make_response(jsonify({
                'Error': f'Student {Services.StudentService.select_student_number_from_student_id(student)[0]["studentnumber"]} is already in a group'
            }), 422)
            response.headers["Content-Type"] = "application/json"
            return response
    # Insert the data
    group_id = GroupService.insert_new_group(prototype=False, tutorial_id=tutorial_id)
    GroupService.insert_students_to_group(students=students, group_id=group_id, prototype=False)
    return 'Yay'


if __name__ == '__main__':
    main()
