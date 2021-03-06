import os
import json

def get_network():
    """
    Return the bus network info from local storage.
    """
    path = os.path.dirname(__file__)
    path = os.path.join(path, "bus_network.json")
    json_file = open(path, 'r')
    return json.loads(json_file.read())

def get_network_update():
    return get_network()['update']

def save_network(bus_network_info):
    """
    Saves a copy of the bus network info to local storage for later retrieval.
    """
    bus_network_json = json.dumps(bus_network_info)
    with open("bus_network.json", 'w') as f:
        f.write(bus_network_json)

