# This is the goto module for the application. All the 
# information regarding the updates or the bus network
# is serviced through this module.

import persistence
import tsbweb
import logging

_bus_network = {}

# Only returns true if the bus network information
# has already been downloaded from the web on the 
# local device.
def bus_network_exists():
    return persistence.bus_network_file_exists()

# Request a new download of the bus network from 
# the web. This should be called the very first time
# the app is running after installation. Can also
# be called in case an update is needed.
def request_bus_network():
    tsbweb.request_bus_network()

# Return the bus network in one single dictionary.
# Returns a local cached value if the function was 
# already called before.
def bus_network():
    global _bus_network
    if _bus_network:
        return _bus_network
    try:
         _bus_network = persistence.get_bus_network()
         return _bus_network
    except:
        try:
            tsbweb.request_bus_network()
            return persistence.get_bus_network()
        except:
            # Gotta try again later, somehow.
            pass

# Returns all the buses names.
def buses():
    result = []
    try:
        buses = bus_network()['buses']
        for bus in buses:
            result.append(bus['name'])
        return result
    except Exception as e:
        return {"nothing to see here!"}

# Return the last update string, if available.
def update():
    try:
        return bus_network()['update']
    except:
        return ""
        

# Return all the info for the bus with this name.
def _bus_info(bus_name):
    buses = bus_network()['buses']
    for idx, bus in enumerate(buses):
        if bus['name'] == bus_name:
            return buses[idx]
    return []

# Return all the info for the given station name on this route.
def _station_info(route, station_name):
    for idx, station in enumerate(route):
        if station['name'] == station_name:
            return route[idx]
    return []

# Direct route names for the given bus.
def droute_names(bus_name):
    return _route_names(bus_name, "droute")

# Reverse route names for the given bus.
def rroute_names(bus_name):
    return _route_names(bus_name, "rroute")

# Return a list of all station names for the given bus.
def _route_names(bus_name, direction):
    result = []
    bus = _bus_info(bus_name)
    for station in bus[direction]:
        result.append(station['name'])
    return result

# Returns the timetable for the given unique station.
def timetable(bus_name, station_name, direction):
    bus = _bus_info(bus_name)
    if not bus:
        logging.error("tsbapp - \"{}\" bus name does not exist".format(bus_name))
        return []
    station = _station_info(bus[direction], station_name)
    if not station:
        logging.error("tsbapp - \"{}\" station name does not exist".format(station_name))
        return []
    return station['timetable']
