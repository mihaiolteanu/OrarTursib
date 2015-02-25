import tsbparse
import utils
import os
import json


def bus_network():
    """
    :return: The Tursib bus network containing all the bus names, routes and timetables.
    """
    return _get_bus_network_local()


def news():
    """
    :return: list of ['news_date', 'news_content'] (list of lists)
    """
    result = []
    links = tsbparse.news_page_links(utils.html_retrieve("www.tursib.ro"))
    for link in links:
        result.append(tsbparse.news_page_content(utils.html_retrieve(link)))
    return result


def check_for_updates():
    """
    Get a newer version of bus info if available.
    """
    latest_update = _tursib_version()
    local_update = _local_version()
    # Download and save to local storage if a different version is available.
    if latest_update != local_update:
        bus_network_info = _bus_network_www_download()
        _save_bus_network_local(bus_network_info)


def _tursib_version():
    """
    :return: string containing the last update text
    """
    return tsbparse.update_string(utils.html_retrieve("www.tursib.ro/trasee"))


def _local_version():
    """
    :return: Local version string of the bus network info.
    """
    bus_network_local = _get_bus_network_local()
    return bus_network_local['updatestring']


def _get_bus_network_local():
    """
    :return: Return the bus network info from local storage.
    """
    path = os.path.dirname(__file__)
    path = os.path.join(path, "bus_network.json")
    json_file = open(path, 'r')
    return json.loads(json_file.read())


def _save_bus_network_local(bus_network_info):
    """
    Saves a copy of the bus network info to local storage for later retrieval.
    :return: nothing
    """
    bus_network_json = json.dumps(bus_network_info)
    f = open("bus_network.json", 'w')
    f.write(bus_network_json)
    f.close()


def bus_network_www_download():
    """
    Build the list with all tursib info.
    """
    busesinfo = tsbparse.buses_info(utils.html_retrieve("www.tursib.ro/trasee"))

    result = {}
    buses = {}
    bus_name_and_stations = []
    for bus in busesinfo:
        bus_link = bus['link']
        station_name_and_timetable = []
        bus_stations = tsbparse.bus_stations(utils.html_retrieve(bus_link))
        for station in bus_stations:
            station_name_and_timetable.append({'stationname': station['name']})
            # Mind the separator between direct and reverse routes
            if station['name'] == '*':
                continue
            station_link = station['link']
            station_name_and_timetable.append({'timetable': tsbparse.station_timetable(utils.html_retrieve(station_link))})

        bus_name_and_stations.append({'busname': bus['name'], 'stations': station_name_and_timetable})
        buses[bus['number']] = list(bus_name_and_stations)
        bus_name_and_stations.clear()

    result = {}
    result['busnumbers'] = buses
    result['updatestring'] = tsbparse.update_string(utils.html_retrieve("www.tursib.ro/trasee"))
    return result

t = bus_network_www_download()
encoded = json.dumps(t)

f = open("output.json", 'w')
f.write(encoded)
f.close()