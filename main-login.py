import kivy

# version = kivy.__version__

kivy.require("1.9.1")

# internal imports
# import random
import cProfile     # for profiling the python code
import re
import sys
import time

# imports from kivy package
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button

# custom imports
import popup
import sql_connect
import log
import sql_query
import json_parser
import home

# determine the platform, whether it is linux, windows or mac
platform = sys.platform

# json Filename
server_credentials = 'sql_server.json'
sql_commands = 'sql_commands.json'


# regex patterns
email_pattern = re.compile('[a-z0-9_\.]+@{1}[a-z]+\.{1}[a-z]+$')
pwd_pattern = re.compile('[a-zA-Z0-9@\$]{8,}')
username_pattern = re.compile('[a-z0-9\._]{4,20}')

# flags used in this program
valid_email_flag = False
valid_pwd_flag = False
valid_username_flag = False
# user_exist_flag = False
# pwd_correct_flag = False

# popup widget for prompt when user enters invalid email and password
incorrect_input_popup = 'invalid email or password\n please try again'
database_empty_popup = 'User does not exit'
invalid_email_popup = 'user does not exist \n register first'
invalid_pwd_popup = 'Incorrect Password'

show_tables = "SHOW TABLES"
select_row_from_table = "SELECT {0} FROM {1} WHERE {2}='{3}'"


def process_login(cmd, column_name, field_name, field_value, pwd):
    user_exist_flag = False
    pwd_correct_flag = False
    db, cursor, valid_database_flag = sql_connect.validate_database(
        json_parser.parse_json(server_credentials, 'server', 'user', 'password', 'database', 'login_db')
    )
    cursor, rows = sql_query.query_sql(cmd, column_name, json_parser.parse_json(server_credentials, 'table', 'login_db'),
                                       field_name, field_value, db, cursor, valid_database_flag, 4)
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
        user_exist_flag = False  # if this is not set false here then it will allow to login with
        # invalid email id after first login was successful
    db.close()
    return pwd_correct_flag and user_exist_flag


class RootWidget(BoxLayout):
    def __init__(self, **kwargs):
        super(RootWidget, self).__init__(**kwargs)

        with self.canvas.before:
            pass

    def authenticate(self, *args):          # query to sql server for login credentials authentication
        column_name = 'password'
        # label = self.ids['label1']
        # label.color = [random.random() for i in xrange(3)] + [1]
        cmd = select_row_from_table
        if valid_pwd_flag and valid_email_flag:
            field_name = 'email'
            field_value = args[0]
            flag = process_login(cmd, column_name, field_name, field_value, args[1])
            if flag:
                start = time.time()
                popup.popup_widget('login successful')
                if time.time() - start >= 3:
                    pass
        elif valid_username_flag and valid_pwd_flag:
            field_name = 'username'
            field_value = args[0]
            flag = process_login(cmd, column_name, field_name, field_value, args[1])
            # flag = sql_query(select_row_from_table.format(column_name, table_name, field_name, field_value),
            #              str(args[1]))  # check if email-id exist
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
