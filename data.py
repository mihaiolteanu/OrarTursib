# Features:
# - get the complete tursib bus network in a single dictionary.
# - get the latest tursib news in a single list.
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

import tsbparse
#from utils import htmlget as htmlget
from tests.utils_mock import htmlget as htmlget

def news():
    """:return: [{'publishdate': '...', 'newscontent': '...'}, {'publishdate':...}]"""
    result = []
    # Get the http links to the latest news from the tursib official page.
    links = tsbparse.news_links(htmlget("tursib_ro"))
    for link in links:
        content = tsbparse.news_content(htmlget(link))
        result.append(content)
    # Return the content of all the latest news found.
    return result

def update():
    return tsbparse.update_string(htmlget("trasee"))

def bus_network():
    """Build the list with all tursib info."""
    buseslist = tsbparse.buses_list(htmlget("trasee"))
    buses = {}
    bus_name_and_stations = []
    for bus in buseslist:
        # Contains a list of all the stations names and links for this bus.
        stations = tsbparse.bus_stations(htmlget(bus['link']))
        direct_and_reverse = _get_direct_and_reverse_stations(stations)
        bus_name_and_stations.append({'name': bus['name'], "stations": direct_and_reverse})
        buses[bus['number']] = list(bus_name_and_stations)
        bus_name_and_stations.clear()
    return {"bus": buses,"update": update()}

def _get_station_name_and_timetable(station_name_link):
    result = []
    for station in station_name_link:
        timetable = tsbparse.station_timetable(htmlget(station['link']))
        result.append({'name': station['name'], 'timetable': timetable})
    return result

def _get_direct_and_reverse_stations(stations):
    direct = _get_station_name_and_timetable(stations['directroutes'])
    reverse = _get_station_name_and_timetable(stations['reverseroutes'])
    return {"direct": direct, "reverse": reverse}

t = bus_network()
encoded = json.dumps(t)
f = open("output.json", 'w')
f.write(encoded)
f.close()

#res = news()
#print(res)
