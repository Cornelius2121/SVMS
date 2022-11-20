from Services.GroupService import select_all_active_groups_for_tutorial as current_groups
from Services.TutorialService import select_all_active_tutorials as current_tutorials
from sklearn.utils import shuffle
from collections import deque
from Services.ScheduleService import insert_full_week_schedule
from Services.WeekService import get_current_week


class GenerateDebateScheduleHelper:
    def __init__(self, db_prototype: bool, week_number=get_current_week()):
        self.db_prototype = db_prototype
        self.week_number = week_number
        self.tutorials = current_tutorials(db_prototype)
        self.groups = []
        self.active_tutorials = []
        for tutorial in self.tutorials:
            current_group = current_groups(tutorial, db_prototype)
            if len(current_group) % 2 == 1:
                current_group.append({
                    'id': None,
                    'tutorial': tutorial,
                    'studentcount': 0,
                    'groupactive': B'1'
                })
            if len(current_group) > 0:
                self.groups.append(current_group)
                self.active_tutorials.append(tutorial)
        self.tutorials = self.active_tutorials
        self.full_schedule = []
        self.left_list = []
        self.right_list = []

    def create_weeks_rounds(self):
        rounds = []
        for i in range(0, 4):
            round = []
            rl = deque(self.right_list)
            rl.rotate(i)
            for index in range(0, len(self.left_list)):
                round.append([self.left_list[index], rl[index]])
            rounds.append(round)
        return rounds

    def prep_list(self, tutorial_number):
        current_tutorials_groups = [group for group in self.groups if group[0]['tutorial'] == tutorial_number][0]
        current_tutorials_groups = shuffle(current_tutorials_groups)
        self.left_list = current_tutorials_groups[:len(current_tutorials_groups) // 2]
        self.right_list = deque(current_tutorials_groups[len(current_tutorials_groups) // 2:])

    def create_all_tutorial_one_weeks_round(self):
        for tutorial in self.tutorials:
            self.prep_list(tutorial)
            rounds = self.create_weeks_rounds()
            tutorial_schedule = {
                'tutorial number': tutorial,
                'groups': [group for group in self.groups if group[0]['tutorial'] == tutorial][0],
                'schedule': rounds
            }
            self.full_schedule.append(tutorial_schedule)
        return self.full_schedule

    def schedule_to_database(self):
        insert_full_week_schedule(self.full_schedule, self.week_number, self.db_prototype)
