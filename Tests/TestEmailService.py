import boto3
from botocore.exceptions import ClientError
from config import AWS_TEST_EMAIL
from Helper.PasswordHelper import send_email as pse
from Helper.AutomatedScheduleHelper import send_email as shse


def password_email_service_tester():
    pse(AWS_TEST_EMAIL, "12345")


def schedule_email_service_tester():
    shse(AWS_TEST_EMAIL, "6")


if __name__ == "__main__":
    password_email_service_tester()
    schedule_email_service_tester()
