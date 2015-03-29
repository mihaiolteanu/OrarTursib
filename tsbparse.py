# Provides functions to retrieve all the necessary information from tursib.ro regarding bus routes,
# bus numbers and names, bus timetables, latest updates and latest news.
# This info is web-scraped from html pages from tursib.ro. Please consult these html
# pages for a better understanding of the algorithms implemented to extract the needed data.
# The parsing is made somewhat harder by the fact that the routes are sometimes not identical at different departure
# times. These different routes are what I call "routing classes". For an example of those, see
# http://www.tursib.ro/traseu/1, for example.

from bs4 import BeautifulSoup
import utils


def news_page_content(html_news_page):
    """Extracts the news content from a html page.
    :param html_news_page: html page such as http://tursib.ro/news/show/160, where 160 is the news ID
    :return: [12 Feb 2015, 'Incepand cu data de 16.02.2015, se inchide circulatia pe str. ...]"""
    bs = BeautifulSoup(html_news_page)
    result = {'publishdate': None, 'newscontent': None}  
    all_divs = bs.find_all('div', {'class': 'section'})
    for div in all_divs:
        if div.find('div', {'class': 'continut'}):
            try:
                result['publishdate'] = div.h2.text
                result['newscontent'] = utils.remove_non_ascii(div.div.text)
            except AttributeError:
                # No such tags exist, so probably this is not a news page.
                pass

    return result


def news_page_links(tursib_ro):
    """Returns the links to the latest news (usually three) posted by Tursib on their official page.
    :param tursib_ro: html page from www.tursib.ro
    :return ['http://tursib.ro/news/show/160', 'http://tursib.ro/news/show/159', 'http://tursib.ro/news/show/158']"""
    bs = BeautifulSoup(tursib_ro)
    return [p.a['href']
            for p in bs.find_all('p', {'class': 'more'})
            if p.text == "Detalii"]


def update_string(tursib_ro_trasee):
    """
    Extract the string of the last update to the busses routes and timetables.
    :param tursib_ro_trasee: html page from www.tursib.ro/trasee containing a tag of the form:
    <h2 style="color:#900;">Program de circulatie incepand cu data de 15 septembrie 2014</h2>
    :return: text of the h2 tag
    """
    bs = BeautifulSoup(tursib_ro_trasee)
    result = [h2.text for h2 in bs.find_all("h2", {"style": "color:#900;"})]
    if result:
        return result[0]
    else:
        return ""


def buses_info(tursib_ro_trasee_html):
    """Returns a list containing all the tursib buses in circulation.
    :param tursib_ro_trasee_html: html page from www.tursib.ro/trasee
    :return [... {'number': '15', 'name': 'Valea Aurie - Gara', 'link': 'http://tursib.ro/traseu/15'},
    {'number': '16', 'name': 'Valea Aurie - Terezian', 'link': 'http://tursib.ro/traseu/16'} ...]"""
    result = []
    bs = BeautifulSoup(tursib_ro_trasee_html)
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
    """Returns a list of direct and reverse routes containing the station name and link.
    :param tursib_ro_traseu_x: html page from www.tursib.ro/traseu/x, where x is the bus number"""
    result = {"directroutes": [], "reverseroutes": []}
    bs = BeautifulSoup(tursib_ro_traseu_x)
    # Each bus has one direct route and one reverse route. These usually do not contain the same station names.
    all_stations = bs.find_all('table', {'class': 'statii'})
    if not len(all_stations) == 2:
        # Posibly not a page containing stations.
        return result
    result["directroutes"] = _parse_bus_stations_route(all_stations, 0)
    result["reverseroutes"] = _parse_bus_stations_route(all_stations, 1)
    return result


def _parse_bus_stations_route(all_stations, direction):
    """Parse a html snippet containing bus station info.
    :all_stations html code containing all direct and reverse routes for a single bus
    :param direction: 0 for direct routes, 1 for reverse routes
    :return [{'link': 'http://tursib.ro/traseu/11/program?statie=0&dir=dus', 'name': 'CEDONIA'}, ...]"""
    result = []
    routes = all_stations[direction].find_all('a', {'class': 'statie-link'})
    for route in routes:
        station_name = route.text
        station_link = route['href']
        result.append({'name': station_name, 'link': station_link})
    return result


def station_timetable(tursib_ro_traseu_statie):
    """Returns the station timetable for the given bus.
    result: {'sunday': ['07:26', '19:26'], 
             'saturday': ['07:26', '19:26'], 
             'weekdays': ['07:26', '08:31', '15:26', '16:31', '17:41', '23:26']}"""
    result = {"weekdays": [], "saturday": [], "sunday": []}
    bs = BeautifulSoup(tursib_ro_traseu_statie)
    plecari = [div.find_all('div') 
        for div in bs.find_all('div', {'class': 'plecari'})]
    if len(plecari) < 3:
        # Probably not a page containing the station timetable.
        return result
    # [:-1] - the last div element serves only for formatting the page. 
    result['weekdays'] = [div.text for div in plecari[0][:-1]]
    result['saturday'] = [div.text for div in plecari[1][:-1]]
    result['sunday'] = [div.text for div in plecari[2][:-1]]
    return result
    


import urllib.request
# Retrieve html page from web.
def html_retrieve(address):
    # Check if address is an url.
    return urllib.request.urlopen(address).read()


def onthefly_testing():
    import os
    dir_name = os.path.join(os.path.dirname('__file__'), 'tests/samples')
    # http://stackoverflow.com/questions/12468179/unicodedecodeerror-utf8-codec-cant-decode-byte-0x9c
    with open(os.path.join(dir_name, "news_160.htm"), "r",encoding='utf-8', errors='ignore') as news_160, \
         open(os.path.join(dir_name, "tursib_ro.htm"), "r",encoding='utf-8', errors='ignore') as tursib_ro, \
         open(os.path.join(dir_name, "tursib_ro_trasee.htm"), "r",encoding='utf-8', errors='ignore') as tursib_ro_trasee, \
         open(os.path.join(dir_name, "tursib_ro_traseu_11.htm"), "r",encoding='utf-8', errors='ignore') as tursib_ro_traseu_11, \
         open(os.path.join(dir_name, "tursib_ro_traseu_11_Conti.htm"), "r",encoding='utf-8', errors='ignore') as tursib_ro_traseu_11_Conti, \
         open(os.path.join(dir_name, "tursib_ro_traseu_112_Bosch.htm"), "r",encoding='utf-8', errors='ignore') as tursib_ro_traseu_112_Bosch, \
         open(os.path.join(dir_name, "dummy_file.txt"), "r",encoding='utf-8', errors='ignore') as dummy_file:

        #print (news_page_content(news_160))
        #print (news_page_content(dummy_file))
        #print (news_page_links(tursib_ro))
        #print (update_string(tursib_ro_trasee))
        #print (buses_info(tursib_ro_trasee))
        res = station_timetable(tursib_ro_traseu_112_Bosch)
        #res = station_timetable(tursib_ro_traseu_11_Conti)
        print(res)

onthefly_testing()
