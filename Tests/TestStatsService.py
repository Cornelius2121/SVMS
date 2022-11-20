from Services import TestDatabaseService as Service
from Services import StatsService
from unittest import TestCase
import numpy as np


class GroupServiceTest(TestCase):
    @classmethod
    def setUp(self) -> None:
        Service.setup_prototype_database(prototype=True)

    def test_get_all_stats_for_user(self):
        results, averages = StatsService.select_all_statistics_for_student_id(177, prototype=False)
        self.assertEqual(results[0]['week'], 2)
        self.assertEqual(results[0]['metric1'], 2.5)
        self.assertEqual(results[1]['week'], 4)
        self.assertEqual(results[1]['metric1'], 3.6)

    def test_average_mark_for_given_week(self):
        # Note: This method requires production data, and may need to be altered for test data
        target_student = 177
        target_week = 2
        results, total_avg = StatsService.select_all_statistics_for_student_id(student_id=target_student)
        target_result = None
        for res in results:
            if res['week'] == target_week: target_result = res
        expected_metric_1_avg = 2.5
        expected_metric_2_avg = 22. / 6.
        expected_metric_3_avg = 20. / 6.
        expected_metric_4_avg = 2.5
        total_avg = 3.
        self.assertEqual(target_result['metric1'], expected_metric_1_avg)
        self.assertEqual(target_result['metric2'], expected_metric_2_avg)
        self.assertEqual(target_result['metric3'], expected_metric_3_avg)
        self.assertEqual(target_result['metric4'], expected_metric_4_avg)
        self.assertEqual(target_result['total'], total_avg)

    def test_average_mark_for_all_weeks(self):
        # Note: This method requires production data, and may need to be altered for test data
        target_student = 177
        results, averages = StatsService.select_all_statistics_for_student_id(student_id=target_student)
        expected_metric_1_avg = np.round(33. / 11., 3)
        expected_metric_2_avg = np.round(38. / 11., 3)
        expected_metric_3_avg = np.round(38. / 11., 3)
        expected_metric_4_avg = np.round(30. / 11., 3)
        expected_total_average = np.round(139. / 44., 3)
        self.assertEqual(averages['metric1'], expected_metric_1_avg)
        self.assertEqual(averages['metric2'], expected_metric_2_avg)
        self.assertEqual(averages['metric3'], expected_metric_3_avg)
        self.assertEqual(averages['metric4'], expected_metric_4_avg)
        self.assertEqual(averages['total'], expected_total_average)

    def test_average_mark_for_all_weeks_with_weeks_excluded(self):
        # Note: This method requires production data, and may need to be altered for test data
        target_student = 177
        weeks_excluded = [4]
        results, averages = StatsService.select_all_statistics_for_student_id(student_id=target_student,
                                                                              exclude_certain_weeks=weeks_excluded)
        expected_metric_1_avg = np.round(2.5, 3)
        expected_metric_2_avg = np.round(22. / 6., 3)
        expected_metric_3_avg = np.round(20. / 6., 3)
        expected_metric_4_avg = np.round(2.5, 3)
        expected_total_average = np.round(3., 3)
        self.assertEqual(averages['metric1'], expected_metric_1_avg)
        self.assertEqual(averages['metric2'], expected_metric_2_avg)
        self.assertEqual(averages['metric3'], expected_metric_3_avg)
        self.assertEqual(averages['metric4'], expected_metric_4_avg)
        self.assertEqual(averages['total'], expected_total_average)

    def test_get_total_average_for_student_no_weeks_excluded(self):
        # Note: This method requires production data, and may need to be altered for test data
        target_student = 177
        total_avg = StatsService.get_total_average_for_student(student_id=target_student)
        expected_total_average = np.round(139. / 44., 3)
        self.assertEqual(expected_total_average, total_avg)

    def test_get_total_average_for_student_with_weeks_excluded(self):
        # Note: This method requires production data, and may need to be altered for test data
        target_student = 177
        week_to_exclude = 4
        total_avg = StatsService.get_total_average_for_student(student_id=target_student,
                                                               exclude_certain_weeks=[week_to_exclude])
        expected_total_average = 3.
        self.assertEqual(expected_total_average, total_avg)

    def test_get_total_average_for_student_with_all_weeks_excluded(self):
        # Note: This method requires production data, and may need to be altered for test data
        target_student = 177
        weeks_to_exclude = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        total_avg = StatsService.get_total_average_for_student(student_id=target_student,
                                                               exclude_certain_weeks=weeks_to_exclude)
        expected_total_average = 0.
        self.assertEqual(expected_total_average, total_avg)
