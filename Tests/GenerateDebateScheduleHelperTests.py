from unittest import TestCase
from Helper.GenerateDebateScheduleHelper import GenerateDebateScheduleHelper
from Services import TestDatabaseService as Service


class TestGenerateDebateScheduleHelper(TestCase):
    @classmethod
    def setUp(self) -> None:
        Service.setup_prototype_database(prototype=True)

    def test_create_one_week_ensure_random(self):
        for loop in range(1000):
            print(f'Start Test {loop}')
            self.test_create_one_week()

    def test_create_one_week(self):
        generate = GenerateDebateScheduleHelper(1, db_prototype=True)
        rounds = generate.create_weeks_rounds()
        total_left = []
        total_right = []
        for round in rounds:
            for debate in round:
                total_left.append(debate[0])
                total_right.append(debate[1])
        for index in range(0, len(total_right)):
            current_left = total_left[index]
            current_right = total_right[index]
            for index2 in range(0, len(total_right)):
                if index2 != index:
                    self.assertFalse(current_left == total_left[index2] and current_right == total_right[index2])
                    self.assertFalse(current_right == total_left[index2] and current_left == total_right[index2])
        print('Test Complete')

    def test_all_tutorials_for_one_week(self):
        generate = GenerateDebateScheduleHelper(True, 1)
        data = generate.create_all_tutorial_one_weeks_round()
        generate.schedule_to_database()
        for tutorial in data:
            rounds = tutorial['schedule']
            total_left = []
            total_right = []
            for round in rounds:
                for debate in round:
                    total_left.append(debate[0])
                    total_right.append(debate[1])
            for index in range(0, len(total_right)):
                current_left = total_left[index]
                current_right = total_right[index]
                for index2 in range(0, len(total_right)):
                    if index2 != index:
                        self.assertFalse(current_left == total_left[index2] and current_right == total_right[index2])
                        self.assertFalse(current_right == total_left[index2] and current_left == total_right[index2])

    def test_all_tutorials_one_week_ensure_random(self):
        for loop in range(1000):
            print(f'Start Test {loop}')
            self.test_all_tutorials_for_one_week()
