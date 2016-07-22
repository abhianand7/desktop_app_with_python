import kivy

kivy.require('1.9.1')

from kivy.uix.popup import Popup
from kivy.uix.label import Label

# method for displaying popups
def popup_widget(var):
    popup = Popup(title='Login',
                  content=Label(text=var),
                  size_hint=(None, None),
                  size=(300, 300))
    popup.open()