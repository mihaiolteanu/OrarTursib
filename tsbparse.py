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
    """
    Extracts the news content from a html page.
    :param html_news_page: html page such as http://tursib.ro/news/show/x, where x is the news ID
    :return: [12 Feb 2015, 'Incepand cu data de 16.02.2015, se inchide circulatia pe str. ...]
    """
    bs = BeautifulSoup(html_news_page)
    result = {'publishdate': None, 'newscontent': None}

    try:
        title = bs.title.string
    except AttributeError:
        # Not an html page.
        return result

    # Not a news html page.
    if not "Anunturi" in title:
        return result;

    all_divs = bs.find_all('div', {'class': 'section'})

    if not all_divs:
        return result

    for div in all_divs:
        if div.find('div', {'class': 'continut'}):
            try:
                result['publishdate'] = div.h2.text
            except AttributeError:
                # No header containing the date the news was published exists.
                result['publishdate'] = None

            try:
                result['newscontent'] = utils.remove_non_ascii(div.div.text)
            except AttributeError:
                # No news body containing the actual news exists on the current html page.
                result['newscontent'] = None

    return result


def news_page_links(tursib_ro):
    """
    Returns the links to the latest news (usually three) posted by Tursib on their official page.
    :param tursib_ro: html page from www.tursib.ro
    :return ['http://tursib.ro/news/show/160', 'http://tursib.ro/news/show/159', 'http://tursib.ro/news/show/158']
    """
    bs = BeautifulSoup(tursib_ro)

    return [p.a['href']
            for p in bs.find_all('p', {'class': 'more'})
            if p.text == "Detalii"]


def update_string(tursib_ro_trasee):
    """
    Extract the date of the last update to the busses routes and timetables.
    :param tursib_ro_trasee: html page from www.tursib.ro/trasee containing a tag of the form:
    <h2 style="color:#900;">Program de circulatie incepand cu data de 15 septembrie 2014</h2>
    :return: text of the h2 tag
    """
    bs = BeautifulSoup(tursib_ro_trasee)
    result = [h2.text for h2 in bs.find_all("h2", {"style": "color:#900;"})]
    if result:
        return result[0]


def buses_info(tursib_ro_trasee_html):
    """
    Returns a list containing all the tursib buses in circulation.
    :param tursib_ro_trasee_html: html page from www.tursib.ro/trasee
    :return [... {'number': '15', 'name': 'Valea Aurie - Gara', 'link': 'http://tursib.ro/traseu/15'},
    {'number': '16', 'name': 'Valea Aurie - Terezian', 'link': 'http://tursib.ro/traseu/16'} ...]
    """
    result = []
    bs = BeautifulSoup(tursib_ro_trasee_html)

    # All routes are contained in <table> tags immediately following h3 tags.
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
    The direct and reverse routes are separated by a *.
    :param tursib_ro_traseu_x: html page from www.tursib.ro/traseu/x, where x is the bus number
    :return [{'link': 'http://tursib.ro/traseu/11/program?statie=0&dir=dus', 'name': 'CEDONIA'},
    {'link': 'http://tursib.ro/traseu/11/program?statie=1&dir=dus', 'name': 'COMPLEX LUPTEI'}, ...]
    """
    result = []
    bs = BeautifulSoup(tursib_ro_traseu_x)

    # Each bus has one direct route and one reverse route. These usually do not contain the same station names.
    all_stations = bs.find_all('table', {'class': 'statii'})
    direct_routes = all_stations[0].find_all('a', {'class': 'statie-link'})
    reverse_routes = all_stations[1].find_all('a', {'class': 'statie-link'})

    # Add both direct and reverse routes to the same list.
    for route in direct_routes:
        station_link = route['href']
        station_name = route.text
        result.append({'name': station_name, 'link': station_link})

    # Mark the boundary between the direct and the reverse routes.
    result.append({"name": "*"})

    for route in reverse_routes:
        station_link = route['href']
        station_name = route.text
        result.append({'name': station_name, 'link': station_link})

    return result


def station_timetable(html_page):
    """
    Returns the complete timetable for a single bus station.
    :param html_page: a html page from http://tursib.ro/traseu/1/program?statie=x&dir=y
    :return: {'saturday': [['p0', '06:04'], ['p1', '06:34'], ['p0', '07:04'],...],
              'weekdays': [['p0', '05:26'], ['p1', '05:40'], ['p0', '05:50'],...],
              'sunday': [['p0', '06:10'], ['p1', '06:34'], ['p0', '07:04'],...],
              'comment': ['La orele marcate cu p0\xa0 se circulã pânã la VIILE SIBIULUI 1'..]}
    Observation: the 'comment' is empty if only p0 is available
    """

    # The timetable is divided in three parts: Weekdays (Luni - Vineri), Saturday (Sambata) and Sunday (Duminica)
    weekdays_timetable = _timetable(_timetable_html_snippet(html_page, "Luni"))
    # Rewind the file iterator.
    html_page.seek(0)

    saturday_timetable = _timetable(_timetable_html_snippet(html_page, "Sambata"))
    html_page.seek(0)

    sunday_timetable = _timetable(_timetable_html_snippet(html_page, "Duminica"))
    html_page.seek(0)

    # Not all departure hours have the exact same route. These are highlighted on tursib.ro and given an explanation.
    class_comment = _timetable_comment(html_page)
    html_page.seek(0)

    return {"weekdays": remove_single_time_class(weekdays_timetable),
            "saturday": remove_single_time_class(saturday_timetable),
            "sunday": remove_single_time_class(sunday_timetable),
            "comment": class_comment}


def _timetable_html_snippet(html_page, day):
    """
    Extract the html snipped containing the timetable info for the day mentioned.
    :param html_page: html from http://tursib.ro/traseu/1/program?statie=x&dir=y
    :param day: one of "Luni - Vineri", "Sambata" or "Duminica"
    :return: bs4.element.Tag object containing the timetable for the specified day
    """
    bs = BeautifulSoup(html_page)

    result = [h3.next_sibling.next_sibling  # First next_sibling is an empty tag
              for h3 in bs.find_all("h3")
              if day in h3.text]

    if result:
        return result[0]
    return None


def _timetable(bs_timetable):
    """
    Extract the timetable info from a html snipped containing that info.
    :param bs_timetable: bs4.element.Tag (BeautifulSoup) containing bus timetable information in html format
    :return: [{'class': 'p0', 'time': '06:47'}, {'class': 'p0', 'time': '07:15'}, {'class': 'p0', 'time': '07:51'}...]
    Observation: Most of the time only p0 is present for all departures.
    """
    result = []
    for departure in bs_timetable.find_all('div'):
        if departure.has_attr('class'):
            # Get the p0 or p1, in the above example; p is always present so we don't need it.
            departure_class = departure['class'][1]
            departure_time = departure.text
            result.append([departure_class, departure_time])

    return result


def remove_single_time_class(bus_timetable):
    """
    Removes the time class from a list if it's the only time class available.
    :param bus_timetable: [['p0', '06:47'], ['p0', '07:15'], ['p0', '07:51'], ['p0', '08:30'], ['p0', '09:10']...]
    :return: if bus_timetable contains only 'p0', for example, return ['06:47', '07:15', '07:51', '08:30', '09:10'...],
    otherwise, return the original list
    """
    result = []
    time_class = [p[0] for p in bus_timetable]
    all_identical = all(p == time_class[0] for p in time_class)
    if all_identical:
        # Remove the time class.
        result = [p[1] for p in bus_timetable]
    else:
        # Don't modify anything.
        result = bus_timetable

    return result


def _timetable_comment(html_page):
    """
    Extracts the comment from a html page with timetables.
    The comment might not be pressent if there is just one routing class.
    :param html_page: html page from http://tursib.ro/traseu/1/program?statie=x&dir=y
    :return: Comment regarding the routes if more than one departure class is available (i.e. p0 and p1)
    """
    result = []
    bs = BeautifulSoup(html_page)
    
    description = [div for div in bs.find_all('div', {'style': 'float:left'})
                   if "La orele marcate cu" in div.text]

    # No such tag present in the current bus page.
    if not description:
        return

    # Build the returning strings
    for descr in description:
        text = "La orele marcate cu "
        departure_class = descr.next_sibling['class'][1]
        text = text + departure_class
        route = descr.next_sibling.next_sibling.text
        text = text + route
        result.append(text)
        
    return result


news_160 = open(r'D:\Projects\Python\Lib\tsb\samples\news_160.htm')
tursib_ro = open(r'D:\Projects\Python\Lib\tsb\samples\tursib_ro.htm')
trasee = open(r'D:\Projects\Python\Lib\tsb\samples\tursib_ro_trasee.htm')
tr1CEC = open(r'D:\Projects\Python\Lib\tsb\samples\TRASEUL 1 - CEC.htm')
tr11_Conti = open(r'D:\Projects\Python\Lib\tsb\samples\TRASEUL 11 - SC CONTINENTAL.htm')
tr11 = open(r'D:\Projects\Python\Lib\tsb\samples\TRASEUL 11.htm')