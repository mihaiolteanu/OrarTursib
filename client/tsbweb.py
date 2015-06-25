import sys
import persistence
import logging
if sys.version_info.major == 3:
    import urllib.request as request
elif sys.version_info.major == 2:
    import urllib2 as request
from kivy.network.urlrequest import UrlRequest

web_bus_network = "http://tsbserver.herokuapp.com/busnetwork"
web_update_string = "http://tsbserver.herokuapp.com/update"

def request_bus_network():
    try:
        response = request.urlopen(web_bus_network)
        persistence.save_bus_network(response.read())
    except Exception as e:
        logging.error("tsbapp - {}".format(e))

def request_update_string():
    try:
        response = request.urlopen(web_update_string)
        response_str = response.read().decode('utf-8')
        # Withot the replace, the string would look like '"update_string_sample"'
        return response_str.replace("\"", "")
    except Exception as e:
        logging.error("tsbapp - {}".format(e))
        return ""
