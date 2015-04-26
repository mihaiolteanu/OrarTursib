import kivy
from kivy.app import App
from kivy.uix.button import Label
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelHeader
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.listview import ListView
from kivy.uix.listview import ListItemButton
from kivy.adapters.listadapter import ListAdapter
from kivy.uix.gridlayout import GridLayout
from kivy.uix.modalview import ModalView
from kivy.properties import ObjectProperty, ListProperty

# Keep track of the root object.
tsb_app = None

class TsbApp(App):
    tp = None
    def build(self):
        # This is the root object.
        global tsb_app
        tsb_app = self

        # The app consists of a single tabbed panel.
        self.tp = TabbedPanel()

        self.show_bus_list()

        tp_favorites = TabbedPanelHeader(text="Favorites")
        tp_favorites.content = Label(text="Track your most used routes")
        tp_search = TabbedPanelHeader(text="Search")
        tp_search.content = Label(text="You can search for routes here")
        self.tp.add_widget(tp_favorites)
        self.tp.add_widget(tp_search)
        return self.tp

    def show_bus_list(self):
        print("the default text is: " + self.tp.default_tab.text)
        self.tp.default_tab.text = "Buses"
        self.tp.default_tab.content = BusesList()        

class BusesList(BoxLayout):
    def __init__(self, **kwargs):
        super(BusesList, self).__init__(**kwargs)
        self.orientation = "vertical"
        list_view = ListView()
        list_view.adapter = ListAdapter(data=["12", "23", "34"], cls=BusButton)
        self.add_widget(list_view)

class StationsList(BoxLayout):
    def __init__(self, **kwargs):
        super(StationsList, self).__init__(**kwargs)
        self.orientation = "vertical"
        list_view = ListView()
        list_view.adapter = ListAdapter(data=["station 12", "station 23", "station 34"], cls=StationButton)
        self.add_widget(list_view)

class TimetableList(BoxLayout):
    def __init__(self, **kwargs):
        super(TimetableList, self).__init__(**kwargs)
        self.orientation = "vertical"
        list_view = ListView()
        list_view.adapter = ListAdapter(data=["timetable 12", "timetable 23", "timetable 34"], cls=StationButton)
        self.add_widget(list_view)


class BusButton(ListItemButton):
    def __init__(self, **kwargs):
        super(BusButton, self).__init__(**kwargs)
        self.size_hint_y = None
        self.height = "40dp"
        self.on_press = self.show_the_stations

    def show_the_stations(self):
        tsb_app.tp.default_tab.content.clear_widgets()
        tsb_app.tp.default_tab.content.add_widget(StationsList())


class StationButton(ListItemButton):
    def __init__(self, **kwargs):
        super(StationButton, self).__init__(**kwargs)
        self.on_press = self.show_the_timetable
    
    def show_the_timetable(self):
        tsb_app.tp.default_tab.content.clear_widgets()
        tsb_app.tp.default_tab.content.add_widget(TimetableList())

if __name__ == '__main__':
    TsbApp().run()

