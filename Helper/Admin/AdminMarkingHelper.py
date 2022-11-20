from Services import StudentService as StuSer
from Services.Admin.MarkingService import select_all_marking_columns as mk_cols
from Services.Admin.MarkingService import select_all_automated_marking_columns as auto_mk_cols
from Services.Admin.MarkingService import select_method_name_from_column_for_marking_column as method_name
from Services.WeekService import get_current_week
from Services.FeedbackService import get_all_feedback_in_week_submitted
from Services.StudentService import select_student_number_from_student_id
import pandas as pd
import numpy as np


def get_marking_selection() -> dict:
    marking_selection = {}
    for row in mk_cols():
        marking_selection[row['column_name']] = False
    return marking_selection


def create_level_one_scaling(week: int):
    # Get all feedback data for the given week
    seperated_students = get_all_feedback_in_week_submitted(week=week)
    # Get a list of all the students who were targets
    target_students = list(set([student['target'] for student in seperated_students if student['target'] is not None]))
    # Set the student feedback list
    student_feedback = [
        {'Student ID': student, 'Student Number': select_student_number_from_student_id(student)[0]['studentnumber'],
         'Feedback': [], 'Staff Grade': None, 'Weighting Factor': None} for
        student in target_students]
    # Append the feedback to the students ID
    for feedback in seperated_students:
        for student in target_students:
            if student == feedback['target'] and feedback['author'] != feedback['target']:
                for dictionary in student_feedback:
                    if dictionary['Student ID'] == student:
                        dictionary['Feedback'].append(feedback)
    # Get each students average
    for student_dict in student_feedback:
        sum = 0
        count = 0
        for feedback in student_dict['Feedback']:
            sum = sum + feedback['metric1']
            count = count + 1
            sum = sum + feedback['metric2']
            count = count + 1
            sum = sum + feedback['metric3']
            count = count + 1
            sum = sum + feedback['metric4']
            count = count + 1
        if count > 0:
            student_dict['Average Score'] = float(sum / count)
        else:
            student_dict['Average Score'] = 0.0
    # For each student that had a staff member give them feedback get the average score of the staff feedback
    for student_dict in student_feedback:
        sum = 0
        count = 0
        for feedback in student_dict['Feedback']:
            if feedback['author'] is None:
                sum = sum + feedback['metric1']
                count = count + 1
                sum = sum + feedback['metric2']
                count = count + 1
                sum = sum + feedback['metric3']
                count = count + 1
                sum = sum + feedback['metric4']
                count = count + 1
        if count != 0:
            student_dict['Staff Grade'] = float(sum / count)
            student_dict['Weighting Factor'] = float(student_dict['Staff Grade'] / student_dict['Average Score'])
    # Calculate Average Weighting Factor
    average_weighting_factor = 1.0
    sum = 0
    count = 0
    for student_dict in student_feedback:
        if student_dict['Weighting Factor'] is not None:
            sum = sum + student_dict['Weighting Factor']
            count = count + 1
    if count != 0:
        average_weighting_factor = float(sum / count)
    # scale all students to give them better marks if the average is greater than 1
    if average_weighting_factor > 1:
        for student_dict in student_feedback:
            student_dict['Weekly Score'] = student_dict['Average Score'] * average_weighting_factor
            if student_dict['Weekly Score'] > 4:
                student_dict['Weekly Score'] = 4.0
    else:
        for student_dict in student_feedback:
            student_dict['Weekly Score'] = student_dict['Average Score']
    return student_feedback, average_weighting_factor


class marking():
    def __init__(self, week: int = get_current_week()):
        self.week = week
        self.df = self.create_student_number_and_id_column()
        self.marking_columns = mk_cols()
        self.marking_methods = {}
        for row in self.marking_columns:
            self.marking_methods[row['column_name']] = row['method_name']

    def retrieve_automated_columns(self):
        automated_columns = auto_mk_cols()
        column_names = list(set([column['column_name'] for column in automated_columns]))
        prerequisite = {}
        for column_name in column_names:
            prerequisite[column_name] = []
        for row in automated_columns:
            prerequisite[row['column_name']].append(row['prerequisite_method_name'])
        return prerequisite

    def check_automated_columns(self, columns_selected, automated_cols):
        columns_selected = [method_name(column) for column in columns_selected]
        valid_automated_columns = []
        for key, value in automated_cols.items():
            prerequisite_not_found = False
            for prerequisite in value:
                if prerequisite not in columns_selected:
                    prerequisite_not_found = True
            if not prerequisite_not_found:
                valid_automated_columns.append(key)
        return valid_automated_columns

    def run_selection(self, marking_selection: dict):
        columns = [key for key, value in marking_selection.items() if value]
        for column in columns:
            getattr(self, self.marking_methods[column])()
        self.automated_cols = self.retrieve_automated_columns()
        self.automated_cols = self.check_automated_columns(columns, self.automated_cols)
        for column in self.automated_cols:
            getattr(self, column)()
        # add the c to each value of student number
        self.df['Student Number'] = 'c' + self.df['Student Number']
        return self.df

    def create_student_number_and_id_column(self) -> pd.DataFrame:
        students = StuSer.select_all_students()
        student_ids = [student['id'] for student in students]
        student_numbers = [student['studentnumber'] for student in students]
        index = np.arange(1, len(student_ids) + 1)
        students_df = pd.DataFrame(columns=['Student ID', 'Student Number'], index=index,
                                   data=list(zip(student_ids, student_numbers)))
        return students_df

    def add_given_feedback_column(self):
        students = [student['studentnumber'] for student in
                    StuSer.select_all_students_who_gave_feedback_for_week(self.week)]
        self.df[f"Gave Feedback In Week {self.week}"] = -1
        for index, row in self.df.iterrows():
            if row['Student Number'] in students:
                self.df[f"Gave Feedback In Week {self.week}"][index] = 1
            else:
                self.df[f"Gave Feedback In Week {self.week}"][index] = 0

    def add_received_feedback_column(self):
        students = [student['studentnumber'] for student in
                    StuSer.select_all_students_who_received_feedback_for_week(self.week)]
        key = f"Received Feedback In Week {self.week}"
        self.df[key] = -1
        for index, row in self.df.iterrows():
            if row['Student Number'] in students:
                self.df[key][index] = 1
            else:
                self.df[key][index] = 0

    def add_actioned_feedback_column(self):
        students = [student['studentnumber'] for student in
                    StuSer.select_all_students_who_actioned_feedback_for_week(self.week)]
        key = f"Actioned Feedback In Week {self.week}"
        self.df[key] = -1
        for index, row in self.df.iterrows():
            if row['Student Number'] in students:
                self.df[key][index] = 1
            else:
                self.df[key][index] = 0

    def add_students_in_inactive_group(self):
        students = [student['studentnumber'] for student in
                    StuSer.select_all_students_who_are_in_an_inactive_group()]
        key = f"Student In Inactive Group In Week {self.week}"
        self.df[key] = -1
        for index, row in self.df.iterrows():
            if row['Student Number'] in students:
                self.df[key][index] = 1
            else:
                self.df[key][index] = 0

    def add_student_level_one_scaling(self):
        students, average_weighting_factor = create_level_one_scaling(self.week)
        student_dict = {}
        for student in students:
            student_dict[student['Student Number']] = student['Weekly Score']
        key = f"Level One Scaling Weekly Score In Week {self.week}"
        self.df[key] = -1.0
        for index, row in self.df.iterrows():
            if row['Student Number'] in student_dict:
                self.df[key][index] = student_dict[row['Student Number']]
            else:
                self.df[key][index] = 0.0
        self.add_weighting_factor_column('Level One Scaling Weighting Factor', average_weighting_factor)

    def add_weighting_factor_column(self, key, weighting_factor):
        self.df[key] = float(weighting_factor)

    def total_level_one_scaling(self):
        key = 'Total Level One Scaling'
        self.df[key] = -1.0
        for index, row in self.df.iterrows():
            gave_fb = row[f"Gave Feedback In Week {self.week}"]
            received_fb = row[f"Received Feedback In Week {self.week}"]
            actioned_fb = row[f"Actioned Feedback In Week {self.week}"]
            level_one_scaling_score = row[f"Level One Scaling Weekly Score In Week {self.week}"]
            sum_vals = gave_fb + received_fb + actioned_fb + level_one_scaling_score
            ranged = (((sum_vals - 0) / (7 - 0)) * (3 - 0)) + 0
            self.df[key][index] = ranged
