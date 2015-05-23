import kivy
from kivy.app import App
from kivy.uix.button import Button, Label
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelHeader
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.listview import ListView, ListItemButton
from kivy.adapters.listadapter import ListAdapter
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
from scrollable import ScrollableLabel
import data

# Keep track of the root object.
tsb_app = None

class TsbApp(App):
    content = BoxLayout(orientation="vertical")
    ## Keep track of where we are in the app.
    selected_bus = None
    selected_station = None
    # Diferentiate between the direct and reverse routes.
    selected_direction = "droute"

    def build(self):
        global tsb_app; tsb_app = self
        self._set_background_color()
        self._check_bus_network()
        self.show_buses()
        return self.content

    def _set_background_color(self):
        """
        http://kivy.org/docs/guide/widgets.html#adding-a-background-to-a-layout
        """
        with self.content.canvas.before:
            Color(0.35, 0.35, 0.35, 1)
            self.content.rect = Rectangle(size=self.content.size,
                                          pos=self.content.pos)
        def update_rect(instance, value):
            instance.rect.pos = instance.pos
            instance.rect.size = instance.size
        self.content.bind(pos=update_rect, size=update_rect)        

    def _check_bus_network(self):
        if not data.bus_network_exists():
            data.request_bus_network()

    def show_buses(self):
        self.content.clear_widgets()
        self.content.add_widget(MyLabel(text="[b]{}[/b]".format("Orar Tursib")))
        self.content.add_widget(BusesList())

    def show_stations(self):
        self.content.clear_widgets()
        self.content.add_widget(StationsList(self.selected_bus))

    def show_timetable(self):
        self.content.clear_widgets()
        self.content.add_widget(TimetableList(self.selected_bus, self.selected_station, self.selected_direction))


# Standard button to be used throughout the application.
class MyButton(Button):
    def __init__(self, **kwargs):
        super(Button, self).__init__(**kwargs)
        self.size_hint_y = None
        self.height = "50dp"


class BusesList(BoxLayout):
    def __init__(self, **kwargs):
        super(BusesList, self).__init__(**kwargs)
        self.orientation = "vertical"
        # Try to retrieve the buses list.
        buses_list = data.bus_names()
        if not buses_list:
            tsb_app.content.add_widget(ScrollableLabel(text="""Baza de date cu autobuze nu a putut fi gasita.
Va rugam verificati accesul la internet si reporniti aplicatia."""))
        else:
            self.add_widget(ListView(
                adapter=ListAdapter(data=buses_list, cls=BusButton)))
        Window.bind(on_keyboard=self.on_back_button)

    # Rebind the back button to exit the application.
    def on_back_button(self, window, key, *args):
        if key == 27:
            App.get_running_app().stop()
            return True
        return False


class BusButton(ListItemButton, MyButton):
    def __init__(self, **kwargs):
        super(BusButton, self).__init__(**kwargs)
        self.on_press = self.show_stations

    def show_stations(self):
        tsb_app.selected_bus = self.text
        tsb_app.show_stations()


class StationsList(BoxLayout):
    def __init__(self, selected_bus, **kwargs):
        super(StationsList, self).__init__(**kwargs)
        self.selected_bus = selected_bus
        self.orientation = "vertical"
        self.show_stations()
        Window.bind(on_keyboard=self.on_back_button)

    def show_stations(self):
        self.clear_widgets()
        box_layout = BoxLayout(orientation="vertical")
        # Display the selected bus at the top of the page.
        box_layout.add_widget(MyLabel(text="[b]{}[/b]".format(self.selected_bus)))

        d_btn_state = "normal"
        r_btn_state = "normal"
        # Station names depending on the direct/reverse selection.
        route_names = None
        if tsb_app.selected_direction == "droute":
            route_names = data.droute_names(self.selected_bus)
            d_btn_state = "down"
        elif tsb_app.selected_direction == "rroute":
            route_names = data.rroute_names(self.selected_bus)
            r_btn_state = "down"

        # Make it possible to select the route (direct or reverse).
        box_layout.add_widget(self.selection_buttons(d_btn_state, r_btn_state))

        # Display routes as a list.
        route = ListView(adapter=ListAdapter(data=route_names, 
                                             cls=StationButton))     
        box_layout.add_widget(route)
        self.add_widget(box_layout)

    def selection_buttons(self, d_btn_state, r_btn_state):
        direct_btn = MyButton(text="Dus", on_press=self.direct_selected, state=d_btn_state)
        reverse_btn = MyButton(text="Intors", on_press=self.reverse_selected, state=r_btn_state)
        selection_btns = BoxLayout(size_hint_y=None, height="50dp")
        selection_btns.add_widget(direct_btn)
        selection_btns.add_widget(reverse_btn)
        return selection_btns

    # Direct route selected by user.
    def direct_selected(self, instance):
        tsb_app.selected_direction = "droute"
        self.show_stations()

    # Reverse route selected by user.
    def reverse_selected(self, instance):
        tsb_app.selected_direction = "rroute"
        self.show_stations()

    def on_back_button(self, window, key, *args):
        if key == 27:
            self.show_buses()
            return True
        return False

    def show_buses(self):
        tsb_app.show_buses()

class StationButton(ListItemButton, MyButton):
    def __init__(self, **kwargs):
        super(StationButton, self).__init__(**kwargs)
        self.on_press = self.show_timetable
    
    def show_timetable(self):
        tsb_app.selected_station = self.text
        tsb_app.show_timetable()

        
class TimetableList(BoxLayout):
    def __init__(self, bus, station, direction, **kwargs):
        super(TimetableList, self).__init__(**kwargs)
        self.orientation = "vertical"
        self.bus = bus
        self.station = station
        self.direction = direction
        box_layout = BoxLayout(orientation="vertical")

        # Display the bus and station name at the top of the page.
        box_layout.add_widget(MyLabel(text="[b]{}[/b]".format(self.bus)))
        box_layout.add_widget(MyLabel(text="[b]{}[/b]".format(self.station)))
        box_layout.add_widget(ScrollableLabel(text=self.timetable(), 
                                              markup=True))

        self.add_widget(box_layout)
        Window.bind(on_keyboard=self.on_back_button)

    def timetable(self):
        return data.formated_timetable(self.bus, self.station, self.direction)

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
        self.font_size = "17sp"
        # Wrap text around if greater than the label width
        # https://groups.google.com/forum/#!topic/kivy-users/RvIvhe0tQm8
        self.bind(size=self.setter('text_size')) 
        self.halign = "center"
        self.valign = "middle"

if __name__ == '__main__':
    TsbApp().run()
