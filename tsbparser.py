# Provides functions to retrieve all the necessary information from 
# html pages retrieved from tursib.ro regarding bus routes,
# bus numbers and names, bus timetables and latest updates.
# This info is web-scraped from html pages from tursib.ro. 
# Please consult these html pages for a better understanding of the 
# algorithms implemented to extract the needed data.

from bs4 import BeautifulSoup
import utils

## The function parameter to all the functions is a html string.
## The name of the parameter indicates the source of the string, 
## that is, tursib_ro_trasee is a html page from www.tursib.ro/trasee.
## Each function returns either a list or a dictionary.

def update_string(tursib_ro_trasee):
    """
    Extract the string of the last update to the busses routes and timetables.
    """
    bs = BeautifulSoup(tursib_ro_trasee)
    result = [h2.text for h2 in bs.find_all("h2", {"style": "color:#900;"})]
    if result:
        return result[0]
    else:
        return ""


def buses_list(tursib_ro_trasee_html):
    """
    Returns a list containing all the tursib buses in circulation,
    in the form of bus number, bus name and the link to a html page
    containing further info for the bus, like the station names.
    """
    result = []
    bs = BeautifulSoup(tursib_ro_trasee_html)
    # The buses are grouped in four major categories: main,secondary,
    # professional and touristic routes, respectively. Each of these 
    # categories has his own html table starting with a h3 header 
    # specifying the route category. 
    routes_tables = [h3.next_sibling for h3 in bs.find_all("h3")
                     if "Trasee" in h3.text]
    # Strip html tags and build the list of bus numbers and names.
    for table in routes_tables:
        td_tags = table.find_all('td', {'class': 'denumire'})
        for td in td_tags:
            bus_link = td.find('a')['href']
            bus_number = bus_link.split('/')[-1]
            bus_name = td.find('strong').text
            result.append({'number': bus_number, 'name': bus_name, 'link': bus_link})
    return result


def bus_stations(tursib_ro_traseu_x):
    """
    Returns a list of direct and reverse routes containing the station name and link.
    """
    result = {"directroutes": [], "reverseroutes": []}
    bs = BeautifulSoup(tursib_ro_traseu_x)
    # Each bus has one direct route and one reverse route. These usually do not contain the same station names.
    all_stations = bs.find_all('table', {'class': 'statii'})
    if not len(all_stations) == 2:
        # Posibly not a page containing stations.
        return result
    result["directroutes"] = _bus_stations_route(all_stations, 0)
    result["reverseroutes"] = _bus_stations_route(all_stations, 1)
    return result


def _bus_stations_route(all_stations, direction):
    """
    Parse a html snippet containing bus station info.
    :all_stations html code containing all direct and reverse routes for a single bus
    :param direction: 0 for direct routes, 1 for reverse routes
    """
    result = []
    routes = all_stations[direction].find_all('a', {'class': 'statie-link'})
    for route in routes:
        station_name = route.text
        station_link = route['href']
        result.append({'name': station_name, 'link': station_link})
    return result


def station_timetable(tursib_ro_traseu_statie):
    """
    Returns the complete station timetable for the given bus.
    Each stations usually has 3 timetables, one for the weekdays,
    one for saturday and one for sunday, but there are exceptions:
    - buses 116 and 118 have only two timetables for each stations (no saturday).
    - bus 22 has only one timetable, covering all the days of the week.
    """
    # Every element consists of a list of two elements,
    # the timetable name (i.e. day) and the timetable hours.
    result = []
    bs = BeautifulSoup(tursib_ro_traseu_statie)
    timetables = [div.find_all('div') 
               for div in bs.find_all('div', {'class': 'plecari'})]
    timetables_count = len(timetables)
    if timetables_count == 0:
        # Probably not a page containing the station timetable.
        return result
    # Only one timetable covering the whole week.
    if timetables_count == 1:
        result.append(['Luni - Duminica', [div.text for div in timetables[0][:-1]]])
        return result
    # Only two timetables, covering the weekdays and saturday.
    if timetables_count == 2:
        result.append(['Luni - Vineri', [div.text for div in timetables[0][:-1]]])
        result.append(['Sambata', [div.text for div in timetables[1][:-1]]])
        return result
    # Normal timetables, but some buses have an extra table for additional
    # information containing the string "La orele marcate cu". This extra
    # table is ignored here, but must be taken into acount.
    if timetables_count == 3 or timetables_count == 4:
        result.append(['Luni - Vineri', [div.text for div in timetables[0][:-1]]])
        result.append(['Sambata', [div.text for div in timetables[1][:-1]]])
        result.append(['Duminica', [div.text for div in timetables[2][:-1]]])
    # Either return normal timetables or else return an empty result.
    return result


# Functions for manual testing.
import os

# Path to the html sample files.
dir_name = os.path.join(os.path.dirname('__file__'), 'tests/samples')

def _file_open(file_name):
    # http://stackoverflow.com/questions/12468179/unicodedecodeerror-utf8-codec-cant-decode-byte-0x9c
    return open(os.path.join(dir_name, file_name), "r",encoding='utf-8', errors='ignore')

def tsbparser_test():
    """
    Open different sample html files taken from tursib.ro
    and print the results of parsing them with this module functions.
    """
    with _file_open("news_160.htm") as news_160, \
         _file_open("tursib_ro.htm") as tursib_ro, \
         _file_open("tursib_ro_trasee.htm") as tursib_ro_trasee, \
         _file_open("tursib_ro_traseu_11.htm") as tursib_ro_traseu_11, \
         _file_open("tursib_ro_traseu_11_Conti.htm") as tursib_ro_traseu_11_Conti, \
         _file_open("tursib_ro_traseu_112_Bosch.htm") as tursib_ro_traseu_112_Bosch, \
         _file_open("tursib_ro_traseu_116_Valea_Aurie.htm") as tursib_ro_traseu_116_Valea_Aurie, \         
         _file_open("dummy_file.txt") as dummy_file:

        #print (news_content(news_160.read()))
        #print (news_links(tursib_ro))
        #print (update_string(tursib_ro_trasee))
        #print (buses_info(tursib_ro_trasee))
        #res = station_timetable(tursib_ro_traseu_112_Bosch)
        #res = station_timetable(tursib_ro_traseu_11_Conti)
        res = station_timetable(tursib_ro_traseu_116_Valea_Aurie)
        print(res)
        #pass

if __name__ == "__main__":
    tsbparser_test()
