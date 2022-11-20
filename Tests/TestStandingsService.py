from Services import TestDatabaseService as Service
from Services import StatsService
from Services import StandingsService
from unittest import TestCase
from Services import GroupService
from Services import StudentService
import numpy as np


class StandingsServiceTest(TestCase):
    @classmethod
    def setUp(self) -> None:
        Service.setup_prototype_database(prototype=True)

    def test_standings_aligns_with_sum_of_students_stats_one_group(self):
        # Note: This method requires production data, and may need to be altered for test data
        target_students = [106, 154, 245, 177]
        target_group = 76
        stats_results = [StatsService.select_all_statistics_for_student_id(student_id=target_student) for target_student
                         in target_students]
        standings_results = StandingsService.get_standings()
        target_score = 0
        for st in standings_results:
            if st['Group'] == target_group:
                target_score = st['Score']
        result_score = 0
        for result in stats_results:
            result_score += result[1]['total']
        self.assertEqual(result_score, target_score)

    def test_standings_aligns_with_sum_of_students_stats_all_active_groups(self):
        # Note: This method requires production data, and may need to be altered for test data
        all_groups = GroupService.select_all_active_groups()
        group_ids = [group['id'] for group in all_groups]
        data = []
        for group in group_ids:
            student_ids = [student['id'] for student in StudentService.select_all_student_ids_in_group(group)]
            group_data = {
                'group': group,
                'score': 0.
            }
            for student in student_ids:
                student_data = StatsService.select_all_statistics_for_student_id(student_id=student)
                group_data['score'] += student_data[1]['total']
            data.append(group_data)
        standings_results = StandingsService.get_standings()
        for st_group in standings_results:
            for data_comp in data:
                if data_comp['group'] == st_group['Group']:
                    self.assertEqual(st_group['Score'], np.round(data_comp['score'], 3))

    def test_standings_aligns_with_sum_of_students_stats_one_group_with_weeks_excluded(self):
        # Note: This method requires production data, and may need to be altered for test data
        target_students = [106, 154, 245, 177]
        target_group = 76
        weeks_excluded = [3, 5]
        stats_results = [StatsService.select_all_statistics_for_student_id(student_id=target_student,
                                                                           exclude_certain_weeks=weeks_excluded) for
                         target_student
                         in target_students]
        standings_results = StandingsService.get_standings(weeks_to_exclude=weeks_excluded)
        target_score = 0
        for st in standings_results:
            if st['Group'] == target_group:
                target_score = st['Score']
        result_score = 0
        for result in stats_results:
            result_score += result[1]['total']
        self.assertEqual(result_score, target_score)

    def test_standings_aligns_with_sum_of_students_stats_all_active_groups(self):
        # Note: This method requires production data, and may need to be altered for test data
        all_groups = GroupService.select_all_active_groups()
        group_ids = [group['id'] for group in all_groups]
        weeks_excluded = [3, 5]
        data = []
        for group in group_ids:
            student_ids = [student['id'] for student in StudentService.select_all_student_ids_in_group(group)]
            group_data = {
                'group': group,
                'score': 0.
            }
            for student in student_ids:
                student_data = StatsService.select_all_statistics_for_student_id(student_id=student,
                                                                                 exclude_certain_weeks=weeks_excluded)
                group_data['score'] += student_data[1]['total']
            data.append(group_data)
        standings_results = StandingsService.get_standings(weeks_to_exclude=weeks_excluded)
        for st_group in standings_results:
            for data_comp in data:
                if data_comp['group'] == st_group['Group']:
                    self.assertEqual(st_group['Score'], np.round(data_comp['score'], 3))
