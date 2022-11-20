import pandas as pd
import Services.StudentWhitelistService as Service
import Services.StudentService as SService
import Helper.PasswordHelper as pw
import config


class ImportStudentData():
    def get_current_whitelist(self) -> list:
        return Service.get_all_students_from_whitelist()

    def extract_students(self, df) -> list:
        students_col = df.iloc[:, 0].tolist()
        students = students_col[6:]
        return students

    def input_file(self, path_to_file) -> list:
        xl_file = pd.ExcelFile(path_to_file)

        dfs = {sheet_name: xl_file.parse(sheet_name)
               for sheet_name in xl_file.sheet_names}

        print('The dataframes have been created')
        keys_to_remove = []
        for key, value in dfs.items():
            if "unallocated" in key:
                keys_to_remove.append(key)
        for key in keys_to_remove:
            del dfs[str(key)]
        print("Unallocated Sheets in the Spreadsheet have been removed")
        number_of_tutorials_raw = len(dfs.items())
        count = 0
        tutorial_count = 0
        all_students = []
        current_students = []
        for key, value in dfs.items():
            count = count + 1
            current_students.extend(self.extract_students(dfs[key]))
            if count % 2 == 0:
                tutorial_count = tutorial_count + 1
                all_students.append({
                    "Tutorial Number": tutorial_count,
                    "Students": current_students
                })
                current_students = []
        return all_students

    def compare_whitelist(self, path_to_file):
        input = self.input_file(path_to_file)
        current = self.get_current_whitelist()
        number_of_tutorials = len(current)
        if not len(current) > len(input):
            number_of_tutorials = len(input)
        tutorial_duplicates = []
        for tutorial in current:
            current_tutorial_id = tutorial['Tutorial Number']
            for input_tutorial in input:
                if input_tutorial['Tutorial Number'] == current_tutorial_id:
                    current_tutorial_duplicates = {
                        "Tutorial Number": current_tutorial_id,
                        "Students": set(input_tutorial['Students']) & set(tutorial['Students'])
                    }
                    tutorial_duplicates.append(current_tutorial_duplicates)
        for duplicate in tutorial_duplicates:
            for current_tutorial in input:
                if current_tutorial['Tutorial Number'] == duplicate['Tutorial Number']:
                    current_tutorial["Students"] = [x for x in current_tutorial["Students"] if
                                                    x not in duplicate["Students"]]

        # Check to see if any of the tutorial lists are empty and remove them
        to_remove = []
        for tutorial in input:
            if len(tutorial['Students']) == 0:
                to_remove.append(tutorial)
        for tutorial in to_remove:
            input.remove(tutorial)

        return input

    def update_student_whitelist(self, path_to_file):
        Service.insert_students_to_whitelist(self.compare_whitelist(path_to_file))

    def update_student_whitelist_and_create_account(self, path_to_file):
        whitelist_additions = self.compare_whitelist(path_to_file)
        Service.insert_students_to_whitelist(whitelist_additions)
        for tutorial in whitelist_additions:
            for student in tutorial['Students']:
                print(f'Creating Account For {str(student)}')
                create_account(str(student))


def check_student_number_against_whitelist(student_number: str):
    return Service.check_account_created_whitelist(student_number)


def create_account(student_number: str):
    # firstly, generate password
    password_unhashed = pw.generate_password()
    # get the hashed pw
    password_hashed = pw.hash_password(password_unhashed)
    # get the tutorial of the new student
    tutorial_id = Service.get_tutorial_from_student_number(student_number)
    # insert the new user to the database
    SService.insert_new_student_with_no_group(student_number=student_number, password=password_hashed,
                                              tutorial_id=tutorial_id, prototype=False)
    # Send the password email to the student
    pw.send_email(f'{config.EMAIL_PRECURSOR}{student_number}{config.EMAIL_DOMAIN}', password_unhashed)
    # update whitelist flag
    Service.update_whitelist_flag(student_number)

