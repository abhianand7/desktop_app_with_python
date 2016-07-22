import kivy

# version = kivy.__version__

kivy.require("1.9.1")

# internal imports
# import random
import cProfile     # for profiling the python code
import re
import pexpect      # in-case you need to run native linux commands
import sys

# additional imports
import MySQLdb as mysql

# imports from kivy package
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
# from kivy.uix.popup import Popup
import popup

# custom imports
#import home

# determine the platform, whether it is linux, windows or mac
platform  = sys.platform

# regex patterns
email_pattern = re.compile('[a-z0-9_\.]+@{1}[a-z]+\.{1}[a-z]+$')
pwd_pattern = re.compile('[a-zA-Z0-9@\$]{8,}')
username_pattern = re.compile('[a-z0-9\._]{4,20}')

# flags used in this program
valid_email_flag = False
valid_pwd_flag = False
valid_database_flag = False
valid_username_flag = False
user_exist_flag = False
pwd_correct_flag = False

# popup widget for prompt when user enters invalid email and password
incorrect_input_popup = 'invalid email or password\n please try again'
database_empty_popup = 'User does not exit'
invalid_email_popup = 'user does not exist \n register first'
invalid_pwd_popup = 'Incorrect Password'

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


# method for running native linux commands
def run_cmd(cmd):                           # under development
    pexpect.run(cmd)
    child = pexpect.spawn(cmd)
    child.expect('')
    child.sendline('')
    return None


# method for logging/debugging errors
# finally logging module of python will be used
def logs(errors):                           # under development
    saveout = sys.stdout
    try:
        fsock = open('logs.txt', 'a')
    except IOError:
        fsock = open('logs.txt', 'w')
    sys.stdout = fsock
    print errors
    sys.stdout = saveout
    fsock.close()


# sql connection establish
def sql_connect():
    # mysql database connection
    user = 'root'
    password = 'Abhinav@7'
    database = 'login_authentication'
    connect_to = 'localhost'        # this will change in case of online authentication

    # this connects to the database and further queries can be made inside the sql database
    db = mysql.connect(connect_to, user, password, database)
    return db


def validate_database():        # method for validating whether the database is configured properly
    # define a cursor to the database
    global valid_database_flag      # always declare a variable 'global' when using from outer scope
    db = sql_connect()
    cursor = db.cursor()
    # sql query
    try:
        rows = str(cursor.execute(show_tables))
    except:     # need to specify the particular exception
        logs('not connected to the database')

    if rows != '0':
        valid_database_flag = True
    else:
        logs('Database Empty')
    return db, cursor


def sql_query(exec_cmd, pwd):
    global user_exist_flag, pwd_correct_flag
    db, cursor = validate_database()
    # print exec_cmd, pwd
    if valid_database_flag:
        try:
            assert isinstance(exec_cmd, object)
            rows = cursor.execute(exec_cmd)
        except:
            logs('Invalid SQL command')
        else:
            if str(rows) != '0':
                user_exist_flag = True
                data = cursor.fetchone()
                if pwd == data[0]:
                    pwd_correct_flag = True
                else:
                    popup.popup_widget(invalid_pwd_popup)
                    pwd_correct_flag = False
            else:
                popup.popup_widget(invalid_email_popup)
                user_exist_flag = False         # if this is not set false here then it will allow to login with
                # invalid email id after first login was successful
    else:
        popup.popup_widget(database_empty_popup)
    db.close()
    return pwd_correct_flag and user_exist_flag


class RootWidget(BoxLayout):
    def __init__(self, **kwargs):
        super(RootWidget, self).__init__(**kwargs)

        with self.canvas.before:
            pass

    def authenticate(self, *args):          # query to sql server for login credentials authentication
        global table_name, field_name, field_value, column_name
        table_name = 'user_credentials'
	column_name = 'password'
        # label = self.ids['label1']
        # label.color = [random.random() for i in xrange(3)] + [1]
        if valid_pwd_flag and valid_email_flag:
            field_name = 'email'
            field_value = args[0]
            flag = sql_query(select_row_from_table.format(column_name, table_name, field_name, field_value), str(args[1]))   # check if email-id exist
            if flag:
                popup.popup_widget('login successful')
        elif valid_username_flag and valid_pwd_flag:
            field_name = 'username'
            field_value = args[0]
            flag = sql_query(select_row_from_table.format(column_name, table_name, field_name, field_value),
                         str(args[1]))  # check if email-id exist
            if flag:
                popup.popup_widget('login successful')        # here it will be redirected to the main application ui
        else:
            popup.popup_widget(incorrect_input_popup)

    def validate_text_input(self, *args):   # method for validating the text input provided in username and password
        global valid_email_flag, valid_pwd_flag, valid_username_flag
        # print "validating input"
        email_label = self.ids['email_label']
        pwd_label = self.ids['pwd_label']

        if args[1] == 'e':
            email_match = email_pattern.match(args[0])
            username_match = username_pattern.match(args[0])
            if email_match:
                email_label.text = 'correct email'
                valid_email_flag = True
                valid_username_flag = False
            elif username_match:
                email_label.text = 'correct username'
                valid_username_flag = True
                valid_email_flag = False
            else:
                email_label.text = 'not a valid email'
                valid_email_flag = False
                valid_username_flag = False
        else:
            pwd_match = pwd_pattern.match(args[0])
            if args[0] < 8:
                pwd_label.text = 'too short, less than 8 characters not allowed'
                valid_pwd_flag = False
            elif pwd_match:
                pwd_label.text = 'valid'
                valid_pwd_flag = True
            else:
                pwd_label.text = 'invalid password'
                valid_pwd_flag = False


class LoginScreenApp(App):
    def build(self):         # the inbuilt method which you need to override in order to return your custom widget tree
        return RootWidget()         # this is the place where you return the widget tree that you constructed for app

    def on_start(self):         # start profiling of the python code
        self.profile = cProfile.Profile()
        self.profile.enable()

    def on_stop(self):          # stop profiling of the python code
        self.profile.disable()
        self.profile.dump_stats('login.profile')    # dump the statistics into a file
    #     it will be saved in the current project directory

    # def build_settings(self, settings):       # for building settings for the app
    #     jsondata = [{'type': "title",
    #                  'title': 'Login'
    #                  },
    #                 {"type": 'options',
    #                  "title": "My first key",
    #                  "desc": "Description of my first key",
    #                  "section": "section1",
    #                  "key": "key1",
    #                  "options": ["value1", "value2", "another value"]
    #                  },
    #                 ]
    #     settings.add_json_panel('Login',
    #                             self.config, data=jsondata)


if __name__ == '__main__':
    LoginScreenApp().run()
