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
from kivy.properties import ObjectProperty

class TsbApp(App):
    pass

class BusButton(ListItemButton):
    def list_bus_stations(self, instance):
        print("list bus stations " + instance.text)

class StationButton(ListItemButton):
    pass

class MainMenu(TabbedPanel):
    bus_tab_content = ObjectProperty()

    def show_the_buses(self, instance):
        self.clear_widgets()
        stations_list = Factory.StationsList()
        # Python2.7 workaround; see page 39 from "Creating Apps in Kivy"
        del stations_list.lst.adapter.data[:]
        stations_list.lst.adapter.data.extend(["station 1", "station 2", "station 3"])
        stations_list.lst._trigger_reset_populate()
        self.add_widget(stations_list)

if __name__ == '__main__':
    TsbApp().run()

