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


"""
def request_bus_network():
    logging.info("tsbapp - request_bus_network()")
    req = UrlRequest(tsbserver + "busnetwork", 
                     on_success=retrieve_bus_network,
                     on_error=retrieve_fail)

def retrieve_bus_network(req, result):
    logging.info("tsbapp - retrieve_bus_network()")
    persistence.save_bus_network(result)
    
def retrieve_fail(req, error):
    logging.error("tsbapp - {}".format(error))
"""
