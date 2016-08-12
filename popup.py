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


# checkbox widget
class CheckboxWidget(GridLayout):
    Builder.load_string(kv)

    def func(self, *args):
        checkbox1 = self.ids['checkbox1']
        checkbox1.text = args[0]
        checkbox2 = self.ids['checkbox2']
        checkbox2.text = args[1]


# method for displaying popups
def popup_widget(var):
    popup = Popup(title='Login',
                  content=Label(text=var),
                  size_hint=(None, None),
                  size=(300, 300))
    popup.open()
    return popup


def popup_dismiss(popup):
    popup.dismiss()
    return None


def popup_with_checkbox(*args):
    popup = Popup(title='select',
                  content=CheckboxWidget(),
                  size_hint=(None, None),
                  size=(200, 500))
    popup.open()
