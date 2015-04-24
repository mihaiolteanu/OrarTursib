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

class HelloApp(App):
    pass

class BusButton(ListItemButton):
    def list_bus_stations(self, instance):
        print("list bus stations " + instance.text)

class MainMenu(TabbedPanel):
    bus_tab_content = ObjectProperty()
    def show_the_buses(self, instance):
        #self.bus_tab_content.item_strings = ["Yo!", "bro!"]
        #self.bus_tab_content.adapter.data.clear()
        del self.bus_tab_content.adapter.data[:]
        self.bus_tab_content.adapter.data.extend(["5", "6", "7"])
        self.bus_tab_content._trigger_reset_populate()
        print(instance.text)

if __name__ == '__main__':
    HelloApp().run()

