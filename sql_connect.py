import MySQLdb as mysql
import log
import popup
import run

# some sql commands
database_name = ''
table_name = ''
field_name = ''
field_value = ''
column_name = ''
create_database = "CREATE DATABASE {0}"
use_database = "USE {0}"
create_table = "CREATE TABLE {0}"
show_tables = "SHOW TABLES"
select_row_from_table = "SELECT {0} FROM {1} WHERE {2}='{3}'"


# sql connection establish
def sql_connect(login):
    # this connects to the database and further queries can be made inside the sql database
    try:
        db = mysql.connect(login[0], login[1], login[2], login[3])
    except mysql.OperationalError:
        # here use more greedy technique for connecting to mysql server in-case the previous step fails
        log.logs('Invalid Credentials for database')
        popup.popup_widget('Fatal Error Ocurred\nContact Admin to resolve the issue')
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
    except:     # need to specify the particular exception
        log.logs('not connected to the database')

    if rows != '0':
        valid_database_flag = True
    else:
        log.logs('Database Empty')
    return db, cursor, valid_database_flag
