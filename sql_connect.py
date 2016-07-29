import MySQLdb as mysql
import log
import popup
import run

# some sql commands

show_tables = "SHOW TABLES"


# sql connection establish
def sql_connect(login):
    # this connects to the database and further queries can be made inside the sql database
    try:
        db = mysql.connect(login[0], login[1], login[2], login[3])
    except mysql.OperationalError:
        # here use more greedy technique for connecting to mysql server in-case the previous step fails
        log.logs('Invalid Credentials for database')
        popup.popup_widget('Fatal Error Occurred\nContact Admin to resolve the issue')
        exit(0)
    return db


def validate_database(login):        # method for validating whether the database is configured properly
    # define a cursor to the database
    valid_database_flag = False
    db = sql_connect(login)
    cursor = db.cursor()
    # sql query
    try:
        rows = str(cursor.execute(show_tables))
    except mysql.ProgrammingError:     # need to specify the particular exception
        log.logs('Invalid Command')

    if rows != '0':
        valid_database_flag = True
    else:
        log.logs('Database Empty')
    return db, cursor, valid_database_flag
