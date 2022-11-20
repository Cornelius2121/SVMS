from unittest import TestCase
from Helper.Admin import AdminGroupManagerHelper
from Services import StudentService as SService
from Helper.Admin import AdminFileUploadHelper


class TestStudentDataImportHelper(TestCase):
    def test_student_information(self):
        student_number = '3355926'
        results = AdminGroupManagerHelper.student_information(student_number)
        expected_student_id = SService.select_student_id_from_student_number(student_number)[0]['id']
        expected_group_id = SService.select_group_from_student_id(expected_student_id)[0]['studentgroup']
        expected_tutorial_id = SService.select_student_tutorial_from_student_id(expected_student_id)[0]['tutorial']
        self.assertIsInstance(results, dict)
        self.assertEqual(results['id'], expected_student_id)
        self.assertEqual(results['tutorial_id'], expected_tutorial_id)
        self.assertEqual(results['group_id'], expected_group_id)

    def test_new_file_upload(self):
        path = "TestFiles/MECH1750_SEM2_CALLAGHAN-classlist.xls"
        AdminFileUploadHelper.new_file_upload(path)