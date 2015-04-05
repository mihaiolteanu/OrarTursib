

def bus_network():
    """:return: The Tursib bus network containing all the bus names, routes and timetables."""
    return _get_bus_network_local()

def check_for_updates():
    """Get a newer version of bus info if available."""
    latest_update = _tursib_version()
    local_update = _local_version()
    # Download and save to local storage if a different version is available.
    if latest_update != local_update:
        bus_network_info = _bus_network_www_download()
        _save_bus_network_local(bus_network_info)


def _tursib_version():
    """:return: string containing the last update text"""
    return tsbparse.update_string(htmlget("trasee"))


def _local_version():
    """:return: Local version string of the bus network info."""
    bus_network_local = _get_bus_network_local()
    return bus_network_local['updatestring']


def _get_bus_network_local():
    """:return: Return the bus network info from local storage."""
    path = os.path.dirname(__file__)
    path = os.path.join(path, "bus_network.json")
    json_file = open(path, 'r')
    return json.loads(json_file.read())


def _save_bus_network_local(bus_network_info):
    """Saves a copy of the bus network info to local storage for later retrieval."""
    bus_network_json = json.dumps(bus_network_info)
    f = open("bus_network.json", 'w')
    f.write(bus_network_json)
    f.close()
