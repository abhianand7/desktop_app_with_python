import kivy

kivy.require('1.9.1')

# Internal Imports
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.uix.button import Button
import datetime


# custom imports
import popup
import json_parser
import sql_connect
import sql_query

# Flags
valid_date_flag = False
valid_state_flag = False
valid_district_flag = False
valid_taluka_flag = False
valid_village_flag = False
valid_search_input = False

# parse information for data required from the json file
sql_server_file = 'sql_server.json'
sql_command_file = 'sql_commands.json'


def sql_process(*args):
    host, user, password = json_parser.parse_json(sql_server_file, 'host', 'user', 'password', 'server')
    database = json_parser.parse_json(sql_server_file, 'database', 'login_db')
    db, cursor, flag = sql_connect.validate_database(host, user, password, database)
    if flag:
        cursor, rows = sql_query.query_sql(args)
        if str(rows) != 0:
            return cursor.fetchall()
        else:
            return None

class TabWidget(TabbedPanel):
    def __init__(self, **kwargs):
        super(TabWidget, self).__init__(**kwargs)

        with self.canvas:
            pass

    def validate_date(self, *args):
        pass

    def validate_state(self, *args):
        pass

    def validate_district(self, *args):
        pass

    def validate_taluka(self, *args):
        pass

    def validate_pincode(self, *args):
        cmd = json_parser.parse_json(sql_command_file, 'show_records_with_value', 'commands')
        table_name = json_parser.parse_json(sql_server_file, 'table', 'all_india_db')
        data = sql_process(cmd, table_name, 'pincode', args[0])
        if data:
            pass
        else:
            popup.popup_widget('Invalid Pincode\nPlease try again')

    def search(self, *args):
        pass


class HomeScreenApp(App):
    def build(self):
        return TabWidget()

if __name__ == '__main__':
    HomeScreenApp().run()
