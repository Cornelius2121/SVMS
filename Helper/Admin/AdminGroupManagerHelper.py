from Services import StudentService, GroupService


# Function to change a students group in the same tutorial
def change_group(student_number: str, new_group: int) -> bool:
    try:
        # Get the student data
        student_data = student_information(student_number)
        # Remove the student from their current group
        remove_student_from_group(student_data['id'], student_data['group_id'])
        # Add the student to their new group
        add_student_to_group(student_data['id'], new_group)
        # Return True
        return True
    except:
        return False


# Function to change a students tutorial and group
def change_tutorial_and_group(student_number: str, tutorial_id: int, new_group: int) -> bool:
    try:
        # Get the student data
        student_data = student_information(student_number)
        # Remove the student from their current group
        remove_student_from_group(student_data['id'], student_data['group_id'])
        # Move the students tutorial
        StudentService.update_student_tutorial(student_data['id'], tutorial_id)
        # Add the student to their new group
        add_student_to_group(student_data['id'], new_group)
        # Return True
        return True
    except:
        return False


# Function to change a students tutorial only and move them into no group
def change_only_tutorial(student_number: str, tutorial_id: int) -> bool:
    try:
        # Get the student data
        student_data = student_information(student_number)
        # Remove the student from their current group
        remove_student_from_group(student_data['id'], student_data['group_id'])
        # Move the students tutorial
        StudentService.update_student_tutorial(student_data['id'], tutorial_id)
        # Return True
        return True
    except:
        return False


# collects the default information required
def student_information(student_number: str) -> dict:
    student_data = {
        'id': StudentService.select_student_id_from_student_number(student_number)[0]['id']

    }
    student_data['group_id'] = StudentService.select_group_from_student_id(student_data['id'])[0]['studentgroup']
    student_data['tutorial_id'] = StudentService.select_student_tutorial_from_student_id(student_data['id'])[0][
        'tutorial']
    return student_data


def remove_student_from_group(student_id: int, group_id: int):
    StudentService.remove_student_from_group(student_id)
    # check if group exists first
    if GroupService.check_if_group_exists(group_id):
        GroupService.reduce_student_group_count(group_id)


def add_student_to_group(student_id: int, group_id: int):
    StudentService.add_student_to_group(student_id, group_id)
    GroupService.increase_student_group_count(group_id)
