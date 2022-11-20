DROP TABLE IF EXISTS Student cascade;
DROP TABLE IF EXISTS StudentGroup cascade;
DROP TABLE IF EXISTS Debate cascade;
DROP TABLE IF EXISTS Tutorial cascade;
DROP TABLE IF EXISTS Feedback cascade;
DROP TABLE IF EXISTS Week cascade;
DROP TABLE IF EXISTS ActionFeedback cascade;
DROP TABLE IF EXISTS StudentWhitelist cascade;
DROP TABLE IF EXISTS Admin cascade;
DROP TABLE IF EXISTS AvailableMarkingColumns cascade;
DROP TABLE IF EXISTS AutomaticMarkingColumns cascade;

CREATE TABLE Tutorial
(
    ID       serial PRIMARY KEY,
    day      VARCHAR NOT NULL,
    time     VARCHAR NOT NULL,
    activity INT     NOT NULL
);

CREATE TABLE StudentGroup
(
    ID           serial PRIMARY KEY,
    tutorial     integer REFERENCES Tutorial (ID),
    studentCount INT    NOT NULL,
    groupactive  BIT(1) NOT NULL
);

CREATE TABLE Debate
(
    ID             serial PRIMARY KEY,
    weekNumber     INT NOT NULL,
    tutorialNumber integer REFERENCES Tutorial (ID),
    roundNumber    INT NOT NULL,
    deskNumber     INT NOT NULL,
    groupX         integer REFERENCES StudentGroup (ID),
    groupY         integer REFERENCES StudentGroup (ID)
);

CREATE TABLE Student
(
    ID            serial PRIMARY KEY,
    studentNumber VARCHAR NOT NULL,
    password      VARCHAR NOT NULL,

    studentGroup  integer REFERENCES StudentGroup (ID),
    tutorial      integer REFERENCES Tutorial (ID)
);

CREATE TABLE Week
(
    ID        serial PRIMARY KEY,
    -- Week Starts on Sunday
    weekstart DATE NOT NULL,
    -- Week Ends on Saturday
    weekend   DATE NOT NULL
);

CREATE TABLE Feedback
(
    ID                     serial PRIMARY KEY,
    target                 integer REFERENCES Student (ID),
    author                 integer REFERENCES Student (ID),
    timeSubmitted          timestamp NOT NULL,
    metric1                integer   NOT NULL,
    metric2                integer   NOT NULL,
    metric3                integer   NOT NULL,
    metric4                integer   NOT NULL,
    report                 BIT(1)    NOT NULL,
    goodcomment            VARCHAR   NOT NULL,
    badcomment             VARCHAR   NOT NULL,
    weeksubmitted          integer REFERENCES Week (ID),
    actionfeedbackrecorded BIT(1)    NOT NULL
);

CREATE TABLE ActionFeedback
(
    ID                  serial PRIMARY KEY,
    feedbackID          integer REFERENCES Feedback (ID),
    goodcommentreaction integer   NOT NULL,
    badcommentreaction  integer   NOT NULL,
    timeSubmitted       timestamp NOT NULL,
    adminactioned       BIT(1)
);

CREATE TABLE StudentWhitelist
(
    ID             serial PRIMARY KEY,
    studentID      VARCHAR NOT NULL,
    tutorialID     INT     NOT NULL,
    accountcreated BIT(1)  NOT NULL
);

CREATE TABLE Admin
(
    ID       serial PRIMARY KEY,
    username VARCHAR NOT NULL UNIQUE,
    password VARCHAR NOT NULL
);

CREATE TABLE AvailableMarkingColumns
(
    ID          serial PRIMARY KEY,
    column_name VARCHAR NOT NULL UNIQUE,
    method_name VARCHAR NOT NULL UNIQUE
);

CREATE TABLE AutomaticMarkingColumns
(
    ID                       serial PRIMARY KEY,
    column_name              VARCHAR NOT NULL,
    prerequisite_method_name VARCHAR NOT NULL UNIQUE
);

INSERT INTO AvailableMarkingColumns (column_name, method_name)
VALUES ('Student Gave Feedback', 'add_given_feedback_column'),
       ('Student Received Feedback', 'add_received_feedback_column'),
       ('Student Actioned Feedback', 'add_actioned_feedback_column'),
       ('Student In Inactive Group', 'add_students_in_inactive_group');

INSERT INTO AvailableMarkingColumns (column_name, method_name)
VALUES ('Student Level One Scaling', 'add_student_level_one_scaling');

INSERT INTO AutomaticMarkingColumns (column_name, prerequisite_method_name)
VALUES ('total_level_one_scaling', 'add_student_level_one_scaling'),
       ('total_level_one_scaling', 'add_given_feedback_column'),
       ('total_level_one_scaling', 'add_received_feedback_column'),
       ('total_level_one_scaling', 'add_actioned_feedback_column');