from config import PROTOTYPE_POSTGRESQL_SERVER, \
    PROTOTYPE_POSTGRESQL_DATABASE,\
    DEVELOPMENT_POSTGRESQL_SERVER,\
    DEVELOPMENT_POSTGRESQL_DATABASE,\
    PROTOTYPE_DATABASE,\
    DEVELOPMENT_POSTGRESQL_PORT,\
    PROTOTYPE_POSTGRESQL_PORT,\
    DEVELOPMENT_POSTGRESQL_ID,\
    DEVELOPMENT_POSTGRESQL_PASSWORD,\
    PROTOTYPE_POSTGRESQL_ID,\
    PROTOTYPE_POSTGRESQL_PASSWORD,\
    ODBC_DRIVER


def create_connection_string(prototype=PROTOTYPE_DATABASE) -> str:
    if prototype:
        cnxn_str = ("Driver={" + ODBC_DRIVER + "};"
                    "Server=" + PROTOTYPE_POSTGRESQL_SERVER + ";"
                    "Database=" + PROTOTYPE_POSTGRESQL_DATABASE + ";"
                    "Port=" + PROTOTYPE_POSTGRESQL_PORT + ";"
                    "ID=" + PROTOTYPE_POSTGRESQL_ID + ";"
                    "Password=" + PROTOTYPE_POSTGRESQL_PASSWORD + ";"
                    "Trusted_Connection=yes;")
        return cnxn_str
    else:
        cnxn_str = ("Driver={" + ODBC_DRIVER + "};"
                    "Server=" + DEVELOPMENT_POSTGRESQL_SERVER + ";"
                    "Database=" + DEVELOPMENT_POSTGRESQL_DATABASE + ";"
                    "Port=" + DEVELOPMENT_POSTGRESQL_PORT + ";"
                    "ID=" + DEVELOPMENT_POSTGRESQL_ID + ";"
                    "Password=" + DEVELOPMENT_POSTGRESQL_PASSWORD + ";"
                    "Trusted_Connection=yes;")
        return cnxn_str

