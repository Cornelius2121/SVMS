# SVMS
The Scaleable Viva Management System (SVMS) is a web application designed to faciliate scalable viva voce oral micro-assessments.

# Functionality

## Version 1.0.0

### Import Student Data

Files are placed in a specified location, as per `config.py`, and a separate script to the Flask
server, `AddStudentAccountsFromSpreadSheetRunFile.py`, is executed on the spreadsheet. In this script, the following
functionality is executed:

- The file is imported to the `ImportStudentData` class from the file `StudentWhitelistDataImportHelper.py`, held within
  a pandas dataframe.
- The current whitelist of students is obtained.
- Students who are already within the whitelist are cut from the whitelist
- Students who are not in the whitelist are then added to the whitelist, and an account is created.

## Version 1.1.0

### Import Student Data

Files are uploaded through a page in the admin section of the web application. The `new_file_upload` method is called
from `AdminFileUploadHelper.py`. This method has the following functionality:

- The file is imported to the `ImportStudentData` class from the file `StudentWhitelistDataImportHelper.py`, held within
  a pandas dataframe.
- The current whitelist of students is obtained.
- Students who are already within the whitelist are cut from the whitelist
- Students who are not in the whitelist are then added to the whitelist, and an account is created.
- Students who were already in the whitelist and have changed tutorials are then unallocated from their group and moved
  to their new tutorial. It should be noted that students are not assigned to a new group, as this is a manual process.

# Development Installation

Development of the SVMS Server is only currently tested on the Windows operating system.

## Windows

In order to install and initialise a development environment for the SVMS server, the below procedure can be
followed:

- Clone the git repository
- Install PostgreSQL
- Create an empty database called `svms`
- Create a custom PostgreSQL user
- Install the latest version of the [ODBC drivers](https://www.postgresql.org/ftp/odbc/versions/msi/)
- Duplicate `config.sample.py` and rename to `config.py` and populate.
- Set the `ODBC_DRIVER` field to `PostgreSQL Unicode`

<a href="https://www.flaticon.com/free-icons/iron" title="iron icons">Iron icons created by Smashicons - Flaticon</a>
