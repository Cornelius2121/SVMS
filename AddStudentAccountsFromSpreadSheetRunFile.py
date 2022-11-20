from config import XLS_LOCATION
from Helper.StudentWhitelistDataImportHelper import ImportStudentData


def add_student_accounts(filename: str):
    data_importer = ImportStudentData()
    data_importer.update_student_whitelist_and_create_account(open(filename, 'rb'))


if __name__ == '__main__':
    path = XLS_LOCATION
    add_student_accounts(path)
