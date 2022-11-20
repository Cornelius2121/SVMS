from Helper.StudentWhitelistDataImportHelper import ImportStudentData
from Services.StudentService import select_all_students
from Helper.Admin.AdminGroupManagerHelper import change_only_tutorial


def new_file_upload(filename: str) -> int:
    # Add the new students to the whitelist
    whitelist_data_importer = ImportStudentData()
    whitelist_data_importer.update_student_whitelist_and_create_account(open(filename, 'rb'))
    # Get students who are in the whitelist and move them tutorials
    tutorial_change_data_importer = ImportStudentData()
    input_file = tutorial_change_data_importer.input_file((open(filename, 'rb')))
    all_students = select_all_students()
    all_student_formatted = []
    # Reformat the students from the database to match the students from the file
    for tutorial in input_file:
        tutorial_number = tutorial['Tutorial Number']
        new_formatted_tutorial = {
            'Tutorial Number': tutorial_number,
            'Students': []
        }
        for student in all_students:
            if student['tutorial'] == tutorial_number:
                new_formatted_tutorial['Students'].append(student['studentnumber'])
        all_student_formatted.append(new_formatted_tutorial)
    all_students = all_student_formatted
    all_students = sorted(all_students, key=lambda d: d['Tutorial Number'])
    input_file = sorted(input_file, key=lambda d: d['Tutorial Number'])
    flagged_students = []
    for tutorial in input_file:
        tutorial_number = tutorial['Tutorial Number']
        all_students_current_tutorial = [x for xs in
                                         [all_students_tutorial['Students'] for all_students_tutorial in all_students if
                                          all_students_tutorial['Tutorial Number'] == tutorial_number] for x in xs]
        all_students_all_other_tutorials = [x for xs in
                                            [all_students_tutorial['Students'] for all_students_tutorial in all_students
                                             if all_students_tutorial['Tutorial Number'] != tutorial_number] for x in
                                            xs]
        for student in tutorial['Students']:
            if student not in all_students_current_tutorial and student in all_students_all_other_tutorials:
                flagged_students.append(student)
    flagged_students_information = []
    for student in flagged_students:
        current_student_information = {'Student Number': student}
        for tutorial in input_file:
            if student in tutorial['Students']:
                current_student_information['New Tutorial'] = tutorial["Tutorial Number"]
        for tutorial in all_students:
            if student in tutorial['Students']:
                current_student_information['Old Tutorial'] = tutorial["Tutorial Number"]
        flagged_students_information.append(current_student_information)
    for student in flagged_students_information:
        change_only_tutorial(student['Student Number'], student['New Tutorial'])
    return len(flagged_students_information)
