# Specify the database path for the development database
DEVELOPMENT_POSTGRESQL_SERVER = ''
DEVELOPMENT_POSTGRESQL_PORT = ''
DEVELOPMENT_POSTGRESQL_DATABASE = ''
DEVELOPMENT_POSTGRESQL_ID = ''
DEVELOPMENT_POSTGRESQL_PASSWORD = ''

# Specify the database path for the prototype database
PROTOTYPE_POSTGRESQL_SERVER = ''
PROTOTYPE_POSTGRESQL_PORT = ''
PROTOTYPE_POSTGRESQL_DATABASE = ''
PROTOTYPE_POSTGRESQL_ID = ''
PROTOTYPE_POSTGRESQL_PASSWORD = ''

# Set to true to connect to prototype database
PROTOTYPE_DATABASE = False

# Set to true in order to pass back any mock data
MOCK_DATA = True

# Set the number of user metrics for feedback
METRIC_COUNT = 5

# AWS EMAIL CONFIG NEEDS TO BE SETUP USING THE FOLLOWING TUTORIAL:
# https://docs.aws.amazon.com/ses/latest/DeveloperGuide/create-shared-credentials-file.html

# This is an email used for the test email script
AWS_TEST_EMAIL = ""

# JWT private key 128bit AES can use openssl -rand 16
JWT_PRIVATE_KEY = ""

# ODBC Driver
ODBC_DRIVER = ""

# Manual XLS Upload Location
XLS_LOCATION = ""

# Path to generated marking folder
GENERATED_MARKING_PATH = ''

# List of weeks to exclude from the students statistics
STATISTICS_WEEKS_TO_EXCLUDE = []

# List of schedule update email addresses that the schedule notification is sent too
SCHEDULE_UPDATE_EMAIL = ['']

# Email configurations
# Given an email address in the format uni1234567@uni.edu.au, the email precursor would be 'uni'
# and the domain '@uni.edu.au". This allows for the students identifier to be dynamic.
# The email precursor is an optional field.
EMAIL_PRECURSOR = ''
EMAIL_DOMAIN = ''