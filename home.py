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
import sql_connect

# Flags
valid_date_flag = False
valid_state_flag = False
valid_district_flag = False
valid_taluka_flag = False
valid_village_flag = False
valid_search_input = False


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
        pass

    def search(self, *args):
        pass

class HomeScreenApp(App):
    def build(self):
        return TabWidget()

if __name__ == '__main__':
    HomeScreenApp().run()
