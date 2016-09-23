import kivy

kivy.require('1.9.1')

from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.checkbox import CheckBox
from kivy.app import App
from kivy.lang import Builder


kv = '''
<CheckboxWidget>
    cols: 2
    Checkbox:
        on_checkbox_active: pass
    Label:
        id: checkbox1
        text: ''
    Checkbox:
        on_checkbox_active: pass
    Label:
        id: checkbox2
        text: ''
'''


# method for displaying popups
def popup_widget(var):
    popup = Popup(title='Login',
                  content=Label(text=var),
                  size_hint=(None, None),
                  size=(300, 300))
    popup.open()
    return popup


# method for displaying popups with custom widget as content instead of just text
def custom_popup_widget(widget):
    popup = Popup(title='Login',
                  content=widget,
                  size_hint=(None, None),
                  size=(300, 300))
    popup.open()
    return popup


def popup_dismiss(popup):
    popup.dismiss()
    return None
