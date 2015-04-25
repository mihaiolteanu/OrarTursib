import kivy
from kivy.app import App
from kivy.uix.button import Label
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.listview import ListView
from kivy.uix.listview import ListItemButton
from kivy.uix.gridlayout import GridLayout
from kivy.uix.modalview import ModalView
from kivy.lang import Builder
from kivy.factory import Factory
from kivy.properties import ObjectProperty, ListProperty

class TsbApp(App):
    pass

class BusButton(ListItemButton):
    pass

class StationButton(ListItemButton):
    pass

class MainMenu(TabbedPanel):
    bus_tab_content = ObjectProperty()
    bus_number = ""

    def __init__(self, **kwargs):
        super(MainMenu, self).__init__(**kwargs)
        self.show_the_buses()
        print("initialized")


    def show_the_buses(self):
        print("press the buses tab")
        bus_list = Factory.BusList()
        self._replace_with(bus_list, ["bus 1", "bus 2", "bus 3", "bus 4", "bus 5"])

    def show_the_stations(self, instance):
        self.clear_widgets()
        stations_list = Factory.StationsList()
        stations_list.bus_number_name = instance.text
        self.bus_number = instance.text
        self._replace_with(stations_list, ["station 1", "station 2", "station 3"])

    def show_the_timetable(self, instance):
        print(self.bus_number + " " + instance.text)

    def _replace_with(self, widget, data):
        # Python2.7 workaround; see page 39 from "Creating Apps in Kivy"
        del widget.lst.adapter.data[:]
        widget.lst.adapter.data.extend(data)
        widget.lst._trigger_reset_populate()
        self.add_widget(widget)

if __name__ == '__main__':
    TsbApp().run()

