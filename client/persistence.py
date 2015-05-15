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

