from flask import Flask, g
from flask import render_template, make_response, jsonify, request, redirect
import datetime
import jwt
from config import JWT_PRIVATE_KEY as JWTKey
import logging
from Pages.TutorialPage import TutroialPage
from Pages.SchedulePage import SchedulePage
from Pages.Admin.AdminMarkingPage import AdminMarkingPage
from Endpoints.GroupEndpoints import GroupEndpoints
from Endpoints.FeedbackEndpoints import FeedbackEndpoints
from Pages.FeedbackPage import FeedbackPage
from Helper.Admin.AdminPasswordHelper import check_admin_password
from Pages.Admin.StandingsPage import AdminStandingsPage
from Pages.StatsPage import StatsPage
from Pages.ActionFeedbackPage import ActionFeedbackPage
from Endpoints.ActionFeedbackEndpoints import ActionFeedbackEndpoints
from Pages.GroupPage import GroupPage
from Endpoints.DiscordIntegration.ScheduleEndpoints import DiscordIntegrationScheduleEndpoints
from Pages.StandingsPage import StandingsPage
from Endpoints.DiscordIntegration.StudentEndpoints import DiscordIntegrationStudentEndpoints
from Helper import PasswordHelper, StudentHelper
from Pages.HomePage import MenuPage
from Endpoints.Admin.AdminFeedbackEndpoints import AdminFeedbackEndpoints
from Pages.Admin.UnactionedFeedbackPage import UnactionedFeedbackPage
from Endpoints.StudentSignupEndpoints import StudentSignup
from Pages.StudentSignupPage import StudentSignupPage
from Pages.Admin.AdminHomePage import AdminHomePage
from Pages.Admin.ReportedFeedbackPage import ReportedFeedbackPage
from Endpoints.Admin.UnactionedFeedbackEndpoints import UnactionedFeedbackEndpoints
from Pages.Admin.AdminFeedbackPage import AdminFeedbackPage
from Pages.Admin.SchedulePage import AdminSchedulePage
from Endpoints.Admin.AdminMarkingEndpoints import AdminMarkingEndpoints
from Pages.Admin.AdminUploadStudentInformationPage import AdminUploadStudentInformation
from Endpoints.Admin.AdminUploadStudentInformationEndpoints import AdminUploadStudentInformationEndpoints
from Pages.Admin.EditGroupsPage import EditGroupsPage
from Endpoints.Admin.AdminEditGroupsEndpoints import AdminEditGroupsEndpoints
from Helper.AutomatedScheduleHelper import add_scheduler_jobs

app = Flask(__name__)
app.register_blueprint(EditGroupsPage)
app.register_blueprint(AdminEditGroupsEndpoints)
app.register_blueprint(AdminFeedbackPage)
app.register_blueprint(AdminUploadStudentInformationEndpoints)
app.register_blueprint(AdminUploadStudentInformation)
app.register_blueprint(AdminMarkingEndpoints)
app.register_blueprint(AdminMarkingPage)
app.register_blueprint(AdminStandingsPage)
app.register_blueprint(AdminFeedbackEndpoints)
app.register_blueprint(ReportedFeedbackPage)
app.register_blueprint(UnactionedFeedbackPage)
app.register_blueprint(UnactionedFeedbackEndpoints)
app.register_blueprint(AdminHomePage)
app.register_blueprint(StudentSignupPage)
app.register_blueprint(StudentSignup)
app.register_blueprint(TutroialPage)
app.register_blueprint(MenuPage)
app.register_blueprint(SchedulePage)
app.register_blueprint(GroupEndpoints)
app.register_blueprint(FeedbackEndpoints)
app.register_blueprint(FeedbackPage)
app.register_blueprint(StatsPage)
app.register_blueprint(ActionFeedbackEndpoints)
app.register_blueprint(ActionFeedbackPage)
app.register_blueprint(GroupPage)
app.register_blueprint(StandingsPage)
app.register_blueprint(DiscordIntegrationScheduleEndpoints)
app.register_blueprint(DiscordIntegrationStudentEndpoints)
app.register_blueprint(AdminSchedulePage)


# Render access denied page
def accessDenied():
    return make_response(render_template('HTTP_Status/403.html'), 403)


# Get JWT token ethier from Auth cookie or Token http header
def getJWT():
    jwtToken = request.cookies.get("Auth")

    if jwtToken == None:
        # Check if Token header
        jwtToken = request.headers.get('Token')

    return jwtToken


# Retrieves the user details from the jwt token if possible
def decodeJWT(token):
    payload = ""
    try:
        payload = jwt.decode(token, JWTKey, algorithms=["HS256"])
    except:
        return False

    return payload


# Prepares user details for the controllers and views
# Controls which request can get to other controllers
# Main code for authentication
@app.before_request
def authentication():
    # Whitelist of urls that don't need authentication
    whitelist = ["/auth", "/login", "/logout", "/student/create-account", "/", "/student/signup", "/admin/login",
                 "/admin/auth", "/static/pincode.js", "/static/pincode.css"]

    # 404 page if no route avaliable
    if request.url_rule == None:
        return make_response(render_template('HTTP_Status/404.html'), 404)

    url = request.url_rule.rule
    if url.startswith("/static/"):
        return

    # Check if current url is in the white list
    if url in whitelist:
        return

    # Find JWT cookie in request
    jwtToken = getJWT()

    authenticated = False

    # If token is avaliable
    if jwtToken != None:
        # Get user details
        payload = decodeJWT(jwtToken)

        # Check if token is valid
        if payload != False:
            authenticated = True

            # Pass it to global context for controllers and views
            g.userDetails = payload

            # If requesting access to discord endpoints
            discordRoleWhiteList = ["/student/data", "/schedule/data/<week_number>"]

            if url.startswith("/admin") and payload["role"] != 'admin':
                return accessDenied()
            if not url.startswith("/admin") and payload["role"] == 'admin':
                return accessDenied()

            if url in discordRoleWhiteList:
                if payload["role"] != "discord":
                    return accessDenied()

            # Restricts discord role to not access other parts of the system
            if payload["role"] == "discord" and url not in discordRoleWhiteList:
                return accessDenied()
    else:  # If not access denied
        return accessDenied()

    # Request not authenticated then 403 the response
    if authenticated == False:
        return accessDenied()


@app.route('/login')
def auth():
    return render_template("Auth/login.html")


@app.route('/admin/login')
def admin_login_page():
    return render_template("Admin/Login/Login.html")


@app.route('/admin/auth', methods=['POST'])
def admin_login():
    data = request.form

    username = data["username"]
    password = data["password"]

    auth, msg = check_admin_password(username, password)

    if auth == True:
        JWT_Token = create_admin_jwt(username=username)
        # It can be any make_response
        response = make_response(jsonify({
            'Login': "Successful"
        }), 200)

        # Make sure below is added to the response
        # 30 day expire
        response.set_cookie('Auth', value=JWT_Token, max_age=2592000, expires=None)

        return response
    else:
        response = make_response(jsonify({
            'Login': "Failed"
        }), 403)
        return response


def create_admin_jwt(username: str, role: str = 'admin'):
    exp = datetime.datetime.utcnow() + datetime.timedelta(30)
    payload = {
        "username": username,
        "role": role,
        "exp": exp  # Expiries in 30 days
    }

    return jwt.encode(payload, JWTKey, algorithm="HS256")


@app.route('/auth', methods=['POST'])
def login():
    # If user credientals are valid then use the code below to grant them access
    # Takes all the user details and creates a signed JWT token expires in 30 days.

    data = request.form

    username = data["username"]
    password = data["password"]

    student_number = StudentHelper.parse_student_number(username)

    if student_number != "-1":
        try:
            auth, msg = PasswordHelper.check_password(student_number, password)
            if auth == True:
                JWT_Token = createJWT(*PasswordHelper.get_student_jwt_auth(student_number))
                # It can be any make_response
                response = make_response(jsonify({
                    'Login': "Successful"
                }), 200)

                # Make sure below is added to the response
                # 30 day expire
                response.set_cookie('Auth', value=JWT_Token, max_age=2592000, expires=None)

                return response
            else:
                response = make_response(jsonify({
                    'Login': "Failed"
                }), 403)
                return response
        except Exception as e:
            response = make_response(jsonify({
                'Login': "Failed",
                'Exception': True,
                'Exception Value': str(e)
            }), 403)
            return response

    else:
        response = make_response(jsonify({
            'Login': "Failed"
        }), 403)
        return response


# Removes Auth cookie from browser not needed for Token http header
@app.route('/logout')
def logout():
    response = make_response(redirect('/login'))
    response.set_cookie('Auth', '', expires=0)

    return response


VERSION_NUMBER = "1.2.1"


@app.route('/')
def hello_world():
    return render_template("Links.html", version_number=VERSION_NUMBER)


def createJWT(studentNumber, student_id, tutorial_id, role, group_id):
    exp = datetime.datetime.utcnow() + datetime.timedelta(30)
    payload = {
        "studentNumber": studentNumber,
        "student_id": student_id,
        "tutorial_id": tutorial_id,
        "role": role,
        "group_id": group_id,
        "exp": exp  # Expiries in 30 days
    }

    return jwt.encode(payload, JWTKey, algorithm="HS256")


scheduler = None


@app.before_first_request
def prepare_scheduler():
    global scheduler
    scheduler = add_scheduler_jobs()


@app.route('/admin/schedule/jobs')
def show_admin_menu():
    jobs = scheduler.get_jobs()
    job_strings = []
    for job in jobs:
        job_strings.append(u'    %s' % job)
    return render_template('Admin/Schedule/ScheduledJobs.html', jobs=job_strings)


if __name__ == '__main__':
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
    app.run()
