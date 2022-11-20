from unittest import TestCase
from Services.WeekService import get_all_remaining_weeks


class StudentHelperTest(TestCase):
    def test_get_all_remaining_weeks(self):
        for week in get_all_remaining_weeks():
            print(week)