import json
import os
import logging
from kivy.storage.jsonstore import JsonStore

def save_bus_network(bus_network):
    data = json.loads(bus_network.decode()) if not isinstance(bus_network, dict) else bus_network
    with open(_bus_network_file(), "w") as f:
        f.write(json.dumps(data))

def get_bus_network():
    with open(_bus_network_file(), "r") as f:
        return json.load(f)

# Save the json file in the same folder as the main application. 
# There is also the possibility of using the kivy user_data_dir.
# This would save the file on different locations depending on 
# the device the app is running. But the code is a little more
# complicated, as the path is only available throught the main 
# app object.
def _bus_network_file():
    return "bus_network.json"

def bus_network_file_exists():
    return os.path.exists(_bus_network_file())

def add_to_favorites(bus_name, station_name, direction):
    store = _favorites_store()
    unique_id = bus_name + station_name + direction
    store.put(unique_id, bus=bus_name, station=station_name, dr=direction)

def remove_from_favorites(bus_name, station_name, direction):
    store = _favorites_store()
    unique_id = bus_name + station_name + direction
    store.delete(unique_id)

def get_favorites():
    result = []
    store = _favorites_store()
    for key in store.keys():
        result.append(store[key])
    return result

def _favorites_store():
    return JsonStore("favorites.json")
