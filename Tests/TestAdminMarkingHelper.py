from Helper.Admin import AdminMarkingHelper as AMH
from Services import TestDatabaseService as Service
from Helper.StudentHelper import parse_student_number
from unittest import TestCase
import json


class AdminMarkingHelperTest(TestCase):
    @classmethod
    def setUp(self) -> None:
        Service.setup_prototype_database(prototype=True)

    def test_get_all_student_columns(self):
        marking = AMH.marking()
        students = marking.df
        for index, row in students.iterrows():
            self.assertTrue(parse_student_number(row['Student Number']) != '-1')
            self.assertTrue(isinstance(row['Student ID'], int))

    def test_get_author_for_week(self):
        marking = AMH.marking(2)
        marking.add_given_feedback_column()
        students = marking.df
        for index, row in students.iterrows():
            self.assertTrue(row['Gave Feedback In Week 2'] == 0 or row['Gave Feedback In Week 2'] == 1)

    def test_get_target_for_week(self):
        marking = AMH.marking(2)
        marking.add_received_feedback_column()
        students = marking.df
        for index, row in students.iterrows():
            self.assertTrue(row['Received Feedback In Week 2'] == 0 or row['Received Feedback In Week 2'] == 1)

    def test_get_target_for_week(self):
        marking = AMH.marking(2)
        marking.add_actioned_feedback_column()
        students = marking.df
        for index, row in students.iterrows():
            self.assertTrue(row['Actioned Feedback In Week 2'] == 0 or row['Actioned Feedback In Week 2'] == 1)

    def test_get_inactive_group_students_for_week(self):
        marking = AMH.marking(2)
        marking.add_students_in_inactive_group()
        students = marking.df
        for index, row in students.iterrows():
            self.assertTrue(
                row['Student In Inactive Group In Week 2'] == 0 or row['Student In Inactive Group In Week 2'] == 1)

    def test_column_selection(self):
        column_selection = AMH.get_marking_selection()
        for key, value in column_selection.items():
            if key == 'Student Gave Feedback':
                column_selection[key] = True
            if key == 'Student Received Feedback':
                column_selection[key] = True
            if key == 'Student Actioned Feedback':
                column_selection[key] = True
            if key == 'Student In Inactive Group':
                column_selection[key] = True
        marking = AMH.marking(2)
        df = marking.run_selection(column_selection)
        self.assertTrue('Gave Feedback In Week 2' in df)
        self.assertTrue('Student In Inactive Group In Week 2' in df)
        self.assertTrue('Actioned Feedback In Week 2' in df)
        self.assertTrue('Received Feedback In Week 2' in df)

    def test_column_selection_not_all_columns(self):
        column_selection = AMH.get_marking_selection()
        data = json.dumps(column_selection)
        for key, value in column_selection.items():
            if key == 'Student Gave Feedback':
                column_selection[key] = True
            if key == 'Student Received Feedback':
                column_selection[key] = True
            if key == 'Student Actioned Feedback':
                column_selection[key] = True
            if key == 'Student In Inactive Group':
                column_selection[key] = False
        marking = AMH.marking(2)
        df = marking.run_selection(column_selection)
        self.assertTrue('Gave Feedback In Week 2' in df)
        self.assertFalse('Student In Inactive Group In Week 2' in df)
        self.assertTrue('Actioned Feedback In Week 2' in df)
        self.assertTrue('Received Feedback In Week 2' in df)

    def test_get_all_automated_columns(self):
        marking = AMH.marking(1)
        res = marking.retrieve_automated_columns()
        self.assertTrue(len(res['total_level_one_scaling']) == 4)

    def test_get_all_valid_automated_columns_not_valid(self):
        marking = AMH.marking(1)
        all_auto_cols = marking.retrieve_automated_columns()
        column_selection = AMH.get_marking_selection()
        for key, value in column_selection.items():
            if key == 'Student Gave Feedback':
                column_selection[key] = True
            if key == 'Student Received Feedback':
                column_selection[key] = True
            if key == 'Student Actioned Feedback':
                column_selection[key] = True
            if key == 'Student In Inactive Group':
                column_selection[key] = True
        columns = [key for key, value in column_selection.items() if value]
        res = marking.check_automated_columns(columns, all_auto_cols)
        self.assertTrue('total_level_one_scaling' not in res)

    def test_get_all_valid_automated_columns_valid(self):
        marking = AMH.marking(1)
        all_auto_cols = marking.retrieve_automated_columns()
        column_selection = AMH.get_marking_selection()
        for key, value in column_selection.items():
            if key == 'Student Gave Feedback':
                column_selection[key] = True
            if key == 'Student Received Feedback':
                column_selection[key] = True
            if key == 'Student Actioned Feedback':
                column_selection[key] = True
            if key == 'Student In Inactive Group':
                column_selection[key] = True
            if key == 'Student Level One Scaling':
                column_selection[key] = True
        columns = [key for key, value in column_selection.items() if value]
        res = marking.check_automated_columns(columns, all_auto_cols)
        self.assertTrue('total_level_one_scaling' in res)
