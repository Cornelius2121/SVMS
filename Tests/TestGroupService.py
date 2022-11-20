from Services import TestDatabaseService as Service
from Services import StudentService
from Services import GroupService
from unittest import TestCase


class GroupServiceTest(TestCase):
    @classmethod
    def setUp(self) -> None:
        Service.setup_prototype_database(prototype=True)

    def test_get_all_groups_in_tutorial(self):
        results = GroupService.select_all_active_groups_for_tutorial(1, True)
        expected = {'id': 1, 'tutorial': 1, 'studentcount': 3, 'groupactive': '1'}
        self.assertEqual(results[0], expected)

    def test_select_all_groups_for_tutorial_with_names(self):
        results = GroupService.select_all_groups_for_tutorial_with_names(1, True)
        expected = {'tutorialNumber': 1,
                    'students': [{'firstname': 'Jacqueline', 'lastname': 'Wiener'},
                                 {'firstname': 'William', 'lastname': 'Lawrence'},
                                 {'firstname': 'Susan', 'lastname': 'Vogel'}]}
        self.assertEqual(results[0], expected)

    def test_insert_group(self):
        id = GroupService.insert_new_group(prototype=True, tutorial_id=1)
        self.assertEqual(id, 9)

    def test_assign_student_to_group(self):
        student_id = StudentService.insert_new_student_with_no_group('3330168', 'password', 1, True)
        student = StudentService.select_student_from_student_number('3330168', True)
        self.assertEqual(student[0]['studentgroup'], None)
        group_id = GroupService.insert_new_group(prototype=True, tutorial_id=1)
        group = GroupService.select_group_from_id(group_id, True)
        self.assertEqual(group[0]['studentcount'], 0)
        GroupService.insert_students_to_group(['3330168'], group_id, True)
        group = GroupService.select_group_from_id(group_id, True)
        self.assertEqual(group[0]['studentcount'], 1)
        student = StudentService.select_student_from_student_number('3330168', True)
        self.assertEqual(student[0]['studentgroup'], group_id)

    def test_remove_student_from_group(self):
        # Set the initial data
        student_number = '3355926'
        student_group = 30
        current_student_group_size = 4
        student_id = StudentService.select_student_id_from_student_number(student_number)[0]['id']
        # Remove the student from a group
        GroupService.remove_student_from_group(student_id)
        # Check that the students group is now -1
        result_group_id = StudentService.select_group_from_student_id(student_id)
        self.assertEqual(result_group_id[0]['studentgroup'], None)

    def test_reduce_student_group_count_not_zero(self):
        # Set the initial data
        student_group = 19
        current_student_group_size = 4
        GroupService.reduce_student_group_count(student_group)
        results = GroupService.select_group_from_id(student_group)[0]
        self.assertEqual(int(results['groupactive']), 1)
        self.assertEqual(int(results['studentcount']), 3)

    def test_reduce_student_group_count_zero(self):
        # Set the initial data
        student_group = 65
        current_student_group_size = 1
        GroupService.reduce_student_group_count(student_group)
        results = GroupService.select_group_from_id(student_group)[0]
        self.assertEqual(int(results['groupactive']), 0)
        self.assertEqual(int(results['studentcount']), 0)

    def test_increase_student_group_count_not_zero(self):
        # Set the initial data
        student_group = 40
        current_student_group_size = 3
        GroupService.increase_student_group_count(student_group)
        results = GroupService.select_group_from_id(student_group)[0]
        self.assertEqual(int(results['groupactive']), 1)
        self.assertEqual(int(results['studentcount']), 4)

    def test_increase_student_group_count_zero(self):
        # Set the initial data
        student_group = 92
        current_student_group_size = 0
        GroupService.increase_student_group_count(student_group)
        results = GroupService.select_group_from_id(student_group)[0]
        self.assertEqual(int(results['groupactive']), 1)
        self.assertEqual(int(results['studentcount']), 1)
