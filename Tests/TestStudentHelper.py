from unittest import TestCase
from Helper.StudentHelper import parse_student_number


class StudentHelperTest(TestCase):
    def test_parse_student_number_no_c(self):
        self.assertEqual("1234567", parse_student_number("1234567"))

    def test_parse_student_number_no_c_too_short(self):
        self.assertEqual("-1", parse_student_number("123456"))

    def test_parse_student_number_no_c_too_long(self):
        self.assertEqual("-1", parse_student_number("12345678"))

    def test_parse_student_number_capital_c(self):
        self.assertEqual("1234567", parse_student_number("C1234567"))

    def test_parse_student_number_capital_c_too_short(self):
        self.assertEqual("-1", parse_student_number("C123456"))

    def test_parse_student_number_capital_c_too_long(self):
        self.assertEqual("-1", parse_student_number("C12345678"))

    def test_parse_student_number_lower_c(self):
        self.assertEqual("1234567", parse_student_number("c1234567"))

    def test_parse_student_number_lower_c_too_short(self):
        self.assertEqual("-1", parse_student_number("c123456"))

    def test_parse_student_number_lower_c_too_long(self):
        self.assertEqual("-1", parse_student_number("c12345678"))

    def test_parse_student_number_wrong_letter(self):
        self.assertEqual("-1", parse_student_number("d1234567"))