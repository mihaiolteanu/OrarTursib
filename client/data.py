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

def buses():
    result = []
    try:
        buses = bus_network()['bus']
        for bus in buses:
            # TODO buses[bus][0]['name'] should be [bus]['name'] - change it in server side.
            name_and_number = "{} - {}".format(bus, buses[bus][0]['name'])
            result.append(name_and_number)
        return result
        #return sorted(buses.keys())
    except Exception as e:
        return {"nothing to see here!"}


