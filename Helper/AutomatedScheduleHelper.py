from templates.Email.ScheduleGenerationEmail import get_email
import boto3
from botocore.exceptions import ClientError
from Services.WeekService import get_all_remaining_weeks
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, time
from Helper.GenerateDebateScheduleHelper import GenerateDebateScheduleHelper
from config import SCHEDULE_UPDATE_EMAIL


def run_schedule_generation():
    generate = GenerateDebateScheduleHelper(db_prototype=False)
    generate.create_all_tutorial_one_weeks_round()
    generate.schedule_to_database()
    # Validate with email to admins
    for email in SCHEDULE_UPDATE_EMAIL:
        send_email(email, int(generate.week_number))


def add_scheduler_jobs():
    all_remaining_weeks = get_all_remaining_weeks()
    scheduler = BackgroundScheduler()
    for week in all_remaining_weeks:
        start_time = datetime.combine(week['weekstart'], time(hour=14, minute=0))
        scheduler.add_job(run_schedule_generation, 'date', run_date=start_time)
    scheduler.start()
    return scheduler


# It should be noted that the student number in this method has no c
def send_email(email: str, week: int):
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
    SUBJECT = f"mech1750.com Week {week} Schedule"

    # The email body for recipients with non-HTML email clients.
    BODY_TEXT = (
        f"The schedule for week {week} has now been created. Any changes to groups will not be reflected in this schedule. This is an automated email - please do not reply directly to this email. Please contact your system administrator for further information if required.")

    # The HTML body of the email.
    BODY_HTML = get_email(week)

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
