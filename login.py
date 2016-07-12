import kivy

# version = kivy.__version__

kivy.require("1.9.1")


from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button

import random

import cProfile     # for profiling the python code

import re

# class CustomDropDown(DropDown):
#     pass
email_pattern = re.compile('[a-z0-9_\.]+@{1}[a-z]+\.{1}[a-z]+$')
pwd_pattern = re.compile('[a-zA-Z0-9@\$]{8,}')

valid_input_flag = False


class RootWidget(BoxLayout):
    def __init__(self, **kwargs):
        super(RootWidget, self).__init__(**kwargs)

        with self.canvas.before:
            pass

    def authenticate(self, *args):          # query to sql server for login credentials authentication
        label = self.ids['label1']
        label.color = [random.random() for i in xrange(3)] + [1]
        # email_input = self.ids['text_input_email']
        # pwd_input = self.ids['text_input_pwd']
        # if (email_input.text and pwd_input.text):
        #     print email_input.text, pwd_input.text
        # print (len(args), type(args), args[0], args[1])     # arguments passed to args are stored as tuple
        # pass

    def validate_text_input(self, *args):   # method for validating the text input provided in username and password
        # print args[0], str(args[0]), type(str(args[0]))
        email_label = self.ids['email_label']
        pwd_label = self.ids['pwd_label']

        if args[1] == 'e':
            email_match = email_pattern.match(args[0])
            if email_match:
                email_label.text = 'correct email'
            else:
                email_label.text = 'not a valid email'
        else:
            pwd_match = pwd_pattern.match(args[0])
            if args[0] < 8:
                pwd_label.text = 'too short, less than 8 characters not allowed'
            elif pwd_match:
                pwd_label.text = 'valid'
            else:
                pwd_label.text = 'invalid password'


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

