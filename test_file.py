# import pickle
# import csv
#
# csv_file_with_address = '/home/ubuntu/PycharmProjects/Jasper_App/all_india_data_for_geocode.csv'
#
#
# def csv_reader(csv_file):
#     csvfile = open(csv_file, 'rb')
#     dialect = csv.Sniffer().sniff(csvfile.read(1024))
#     csvfile.seek(0)
#     reader = csv.reader(csvfile, dialect)
#     return reader
#
#
# def get_row_from_address(csv_file):
#     reader = csv_reader(csv_file)
#     for row in reader:
#         yield row
#
# gen = get_row_from_address(csv_file_with_address)
#
# print gen.next()
#
# gen_pickle = pickle.dumps(gen)
#
# g2 = pickle.loads(gen_pickle)
#
# print g2.next()
import kivy
import popup
from kivy.uix.gridlayout import GridLayout
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.checkbox import CheckBox


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


class CheckboxWidget(GridLayout):
    pass


class CustomApp(App):
    def build(self):
        return popup.custom_popup_widget(CheckboxWidget())


if __name__ == '__main__':
    CustomApp().run()