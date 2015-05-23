# Features:
# - get the complete tursib bus network in a single dictionary.
# - get a string specifing the latest update to the bus network 
#   available on tursib. This string is also included in the complete
#   tursib bus network response as a dictionary entry.
# This layer depends on the parser layer and does not do any
# html parsing on its own. It merely puts together the web scrapping
# done by the parser. It also invokes the layer responsible for 
# downloading the html content from the web. The pages thus 
# retrieved are passed on to the parser layer which returns lists 
# and dictionaries. These often contain additional links which must 
# be again given to the html downloader and the resulting pages given 
# to the parser.

import tsbparser as parser
from utils import htmlget as htmlget
#from tests.utils_mock import htmlget as htmlget

def update():
    """
    String containing the last tursib update info.
    """
    tursib_ro_trasee = htmlget("trasee")
    return parser.update_string(tursib_ro_trasee)

def bus_network():
    """
    Build the list with all tursib info.
    """
    tursib_ro_trasee = htmlget("trasee")
    buseslist = parser.buses_list(tursib_ro_trasee)
    buses = []
    for bus in buseslist:
        tursib_ro_traseu_x = htmlget(bus['link'])
        stations = parser.bus_stations(tursib_ro_traseu_x)
        buses.append({"name": "{} - {}".format(bus['number'], bus['name']), 
                      "droute": _get_direct_stations(stations), 
                      "rroute": _get_reverse_stations(stations)})
    return {"buses": buses,"update": update()}

def _get_direct_stations(stations):
    return _get_station_name_and_timetable(stations['directroutes'])

def _get_reverse_stations(stations):
    return _get_station_name_and_timetable(stations['reverseroutes'])

def _get_station_name_and_timetable(station_name_link):
    result = []
    for station in station_name_link:
        tursib_ro_traseu_statie = htmlget(station['link'])
        timetable = parser.station_timetable(tursib_ro_traseu_statie)
        result.append({'name': station['name'], 'timetable': timetable})
    return result

"""
import json
t = bus_network()
encoded = json.dumps(t)
f = open("output.json", 'w')
f.write(encoded)
f.close()
"""
