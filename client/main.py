import kivy
from kivy.app import App
from kivy.uix.button import Button, Label
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelHeader
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.listview import ListView, ListItemButton
from kivy.adapters.listadapter import ListAdapter
from kivy.properties import ObjectProperty, ListProperty
from kivy.core.window import Window
from scrollable import ScrollableLabel

import data

# Keep track of the root object.
tsb_app = None

class TsbApp(App):
    tp = TabbedPanel()
    def build(self):
        global tsb_app; tsb_app = self
        self._check_bus_network()
        self._init_tabs()
        return self.tp

    def _check_bus_network(self):
        if not data.bus_network_exists():
            data.request_bus_network()

    # Setup the initial content of the tabs.
    def _init_tabs(self):
        self._setup_buses()
        self._setup_favorites()
        self._setup_search()

    def _setup_buses(self):
        self.tp.default_tab.text = "Buses"
        self.tp.default_tab.content = BusesList()

    def _setup_favorites(self):
        tp_favorites = TabbedPanelHeader(text="Favorites",
                                         content=Label(text="You don't have any favorite routes yet"))
        self.tp.add_widget(tp_favorites)
        #self.show_favorites()

    def _setup_search(self):
        tp_search = TabbedPanelHeader(text="Search")
        tp_search.content = Label(text="You can search for routes here")
        self.tp.add_widget(tp_search)

    ######################################################
    # Methods to clear and set the content of the buses tab.
    #######################################################
    # The buses tab initially contains a list of all the available buses.
    # The user can select and bus and the content will change to a list 
    # of all the stations for that particular bus. The user can cancel 
    # the selection and return to the initial list, or she can select a
    # station name and be presented with the timetable for that station.
    # At every step, the bus number and/or station name are recorded 
    # and used to show the user the current selection as well as to know
    # where to return to in case the user cancels the selection.
    @property
    def selected_bus(self):
        return self._selected_bus
    @selected_bus.setter
    def selected_bus(self, bus_number):
        self._selected_bus = bus_number

    @property
    def selected_station(self):
        return self._selected_station
    @selected_station.setter
    def selected_station(self, station_name):
        self._selected_station = station_name

    # Used to diferentiate between the direct and reverse
    # routes after a station name is selected from the bus
    # station names.
    @property
    def selected_direction(self):
        return self._selected_direction
    @selected_direction.setter
    def selected_direction(self, route):
        self._selected_direction = route

    @property
    def buses_tab_content(self):
        return self.tp.default_tab.content

    def show_buses(self):
        self.buses_tab_content.clear_widgets()
        self.buses_tab_content.add_widget(BusesList())

    def show_stations(self):
        self.buses_tab_content.clear_widgets()
        self.buses_tab_content.add_widget(StationsList(self.selected_bus))

    def show_timetable(self):
        self.buses_tab_content.clear_widgets()
        self.buses_tab_content.add_widget(TimetableList(self.selected_bus, self.selected_station))

    #######################################
    # Methods for the favorites tab.
    #######################################
    @property
    def favorites_content(self):
        return self.tp.tp_favorites
    def show_favorites(self):
        favorites = data.get_favorites()
        if not favorites:
            return
        favorites_text = ""
        for fav in favorites:
            favorites_text = favorites_text + " " + fav['bus']
            tp_favorites.content = Label(text=favorites_text)    


class BusesList(BoxLayout):
    def __init__(self, **kwargs):
        super(BusesList, self).__init__(**kwargs)
        self.orientation = "vertical"
        self.add_widget(ListView(
            adapter=ListAdapter(data=data.buses(), cls=BusButton)))


class BusButton(ListItemButton):
    def __init__(self, **kwargs):
        super(BusButton, self).__init__(**kwargs)
        self.size_hint_y = None
        self.height = "40dp"
        self.on_press = self.show_stations

    def show_stations(self):
        tsb_app.selected_bus = self.text
        tsb_app.show_stations()


class StationsList(BoxLayout):
    def __init__(self, selected_bus, **kwargs):
        super(StationsList, self).__init__(**kwargs)
        self.orientation = "vertical"

        box_layout = BoxLayout(orientation="vertical")
        # Display the selected bus at the top of the page.
        box_layout.add_widget(MyLabel(text="[b]{}[/b]".format(selected_bus)))

        droute = ListView(adapter=ListAdapter(data=data.droute_names(tsb_app.selected_bus), 
                                              cls=StationButtonDirect))
        rroute = ListView(adapter=ListAdapter(data=data.rroute_names(tsb_app.selected_bus), 
                                              cls=StationButtonReverse))

        # Make it possible to select the route (direct or reverse).
        route_panel = TabbedPanel(default_tab_text="Direct", 
                                  default_tab_content=droute)
        route_panel.add_widget(TabbedPanelHeader(text="Reverse", 
                                                 content=rroute))
        box_layout.add_widget(route_panel)

        self.add_widget(box_layout)
        Window.bind(on_keyboard=self.on_back_button)

    def on_back_button(self, window, key, *args):
        if key == 27:
            self.show_buses()
            return True
        return False

    def show_buses(self):
        tsb_app.show_buses()

class StationButtonDirect(ListItemButton):
    def __init__(self, **kwargs):
        super(StationButtonDirect, self).__init__(**kwargs)
        self.size_hint_y = None
        self.height = "40dp"
        self.on_press = self.show_timetable
    
    def show_timetable(self):
        tsb_app.selected_station = self.text
        tsb_app.selected_direction = "droute"
        tsb_app.show_timetable()

class StationButtonReverse(ListItemButton):
    def __init__(self, **kwargs):
        super(StationButtonReverse, self).__init__(**kwargs)
        self.size_hint_y = None
        self.height = "40dp"
        self.on_press = self.show_timetable
    
    def show_timetable(self):
        tsb_app.selected_station = self.text
        tsb_app.selected_direction = "rroute"
        tsb_app.show_timetable()

        
class TimetableList(BoxLayout):
    def __init__(self, selected_bus, selected_station, **kwargs):
        super(TimetableList, self).__init__(**kwargs)
        self.orientation = "vertical"
        box_layout = BoxLayout(orientation="vertical")

        # Display the bus and station name at the top of the page.
        box_layout.add_widget(MyLabel(text="[b]{}[/b]".format(selected_bus)))
        box_layout.add_widget(MyLabel(text="[b]{}[/b]".format(selected_station)))
        box_layout.add_widget(ScrollableLabel(text=self.timetable(), 
                                              markup=True))

        self.add_widget(box_layout)
        Window.bind(on_keyboard=self.on_back_button)


    def timetable(self):
        ttable = data.timetable(tsb_app.selected_bus,
                                  tsb_app.selected_station,
                                  tsb_app.selected_direction)
        formated = "  [b]Weekdays[/b]:\n {} \n [b]Saturday[/b]:\n {} \n [b]Sunday[/b]:\n {}".format(
            ", ".join(ttable['weekdays']),
            ", ".join(ttable['saturday']),
            ", ".join(ttable['sunday']))
        return formated

    def on_back_button(self, window, key, *args):
        if key == 27:
            self.show_stations()
            return True
        return False

    def show_stations(self):
        tsb_app.show_stations()

# Standard label to be used throughout the application.
class MyLabel(Label):
    def __init__(self, **kwargs):
        super(MyLabel, self).__init__(**kwargs)
        self.size_hint_y = None
        self.height = "40dp"
        self.markup = True

# Standard button to be used throughout the application.
class MyButton(Button):
    def __init__(self, **kwargs):
        super(Button, self).__init__(**kwargs)
        self.size_hint_y = None
        self.height = "50dp"
    

if __name__ == '__main__':
    TsbApp().run()
