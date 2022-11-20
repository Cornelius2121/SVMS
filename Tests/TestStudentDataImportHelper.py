from unittest import TestCase
from Helper.StudentWhitelistDataImportHelper import ImportStudentData
from Services import TestDatabaseService as Service
from Services import StudentWhitelistService as SWService


class TestStudentDataImportHelper(TestCase):
    @classmethod
    def setUp(self) -> None:
        Service.setup_prototype_database(prototype=True)

    def test_read_in_xlsx_file(self):
        data_collector = ImportStudentData()
        students = data_collector.input_file(open("TestFiles/MECH1750_SEM2_CALLAGHAN-classlist.xls", 'rb'))
        self.assertEqual(students[0]['Tutorial Number'], 1)
        self.assertEqual(students[0]['Students'][0], '3355696')

    def test_student_whitelist_service(self):
        results = SWService.get_all_students_from_whitelist(True)
        self.assertEqual(results[0]['Tutorial Number'], 1)
        self.assertEqual(results[0]['Students'][0], '3330168')

    def test_compare_whitelist(self):
        data = ImportStudentData()
        results = data.compare_whitelist(open("TestFiles/MECH1750_SEM2_CALLAGHAN-classlist.xls", 'rb'))
        self.assertTrue("3355696" not in results[0]["Students"])

    def test_insert_all_to_database(self):
        data = ImportStudentData()
        data.update_student_whitelist(open("TestFiles/MECH1750_SEM2_CALLAGHAN-classlist.xls", 'rb'))
        results = SWService.get_all_students_from_whitelist()
        self.assertEqual(results[0]['Students'][2], '3374456')

    def test_check_whitelist(self):
        self.assertFalse(SWService.check_account_created_whitelist("3330168"))
