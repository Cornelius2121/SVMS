import random
import hashlib
from Services.StudentService import select_password_from_student_id
from Services import StudentService as Service
from templates.Email.PasswordEmail import get_email
import boto3
from botocore.exceptions import ClientError


# This file is used to generate and hash passwords for authentication purposes

# This method generates a random 5 digit password
def generate_password() -> str:
    password = ""
    for i in range(0, 5):
        password = password + str(random.randint(0, 9))
    return password


# Hashes a string password with MD5 and returns a hex string
def hash_password(password: str) -> str:
    hash_pw = hashlib.md5(password.encode())
    return str(hash_pw.hexdigest())


# This method checks the password from the student id
def check_password(student_number: str, given_password: str):
    hashed_given_password = hash_password(given_password)
    actual_hashed_password = select_password_from_student_id(student_number)
    if hashed_given_password == actual_hashed_password:
        return True, "Success"
    else:
        return False, "Password is not correct"


# It should be noted that the student number in this method has no c
def send_email(email: str, password_unhashed: str):
    # Replace sender@example.com with your "From" address.
    # This address must be verified with Amazon SES.
    SENDER = "info@mech1750.com"

    # Replace recipient@example.com with a "To" address. If your account
    # is still in the sandbox, this address must be verified.
    RECIPIENT = email

    # Specify a configuration set. If you do not want to use a configuration
    # set, comment the following variable, and the
    # ConfigurationSetName=CONFIGURATION_SET argument below.
    # CONFIGURATION_SET = "ConfigSet"

    # If necessary, replace us-west-2 with the AWS Region you're using for Amazon SES.
    AWS_REGION = "us-east-2"

    # The subject line for the email.
    SUBJECT = "Your mech1750.com Password"

    # The email body for recipients with non-HTML email clients.
    BODY_TEXT = ("Your password is now available for mech1750.com!\r\n"
                 f"Your new password is: {password_unhashed}"
                 "This password cannot be reset. Please do not delete this email and record this provided password in a safe location. "
                 )

    # The HTML body of the email.
    BODY_HTML = get_email(password_unhashed)

    # The character encoding for the email.
    CHARSET = "UTF-8"

    # Create a new SES resource and specify a region.
    client = boto3.client('ses', region_name=AWS_REGION)

    # Try to send the email.
    try:
        # Provide the contents of the email.
        response = client.send_email(
            Destination={
                'ToAddresses': [
                    RECIPIENT,
                ],
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': CHARSET,
                        'Data': BODY_HTML,
                    },
                    'Text': {
                        'Charset': CHARSET,
                        'Data': BODY_TEXT,
                    },
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': SUBJECT,
                },
            },
            Source=SENDER,
            # If you are not using a configuration set, comment or delete the
            # following line
            # ConfigurationSetName=CONFIGURATION_SET,
        )
    # Display an error if something goes wrong.
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("Email sent! Message ID:"),
        print(response['MessageId'])

def get_student_jwt_auth(student_number: str) -> list:
    data = [student_number]
    id = Service.select_student_id_from_student_number(student_number)[0]['id']
    data.append(id)
    data.append(Service.select_student_tutorial_from_student_id(id)[0]['tutorial'])
    data.append("student")
    data.append(Service.select_group_from_student_id(id)[0]['studentgroup'])
    return data
