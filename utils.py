import urllib.parse
import urllib.request
import logging
import datetime
import os

# Tursib official website with all the needed info.
base = "http://www.tursib.ro"

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# The function accepts relative addresses and 
# merely apends these to the base address. It 
# then returns the content of the page found 
# at the address thus constructed.
def htmlget(address):
    path = urllib.parse.urljoin(base, address)
    req = urllib.request.Request(path)
    try:
        response = urllib.request.urlopen(req)
        return response.read()
    except urllib.error.HTTPError as e:
        logger.info("{} could not be found".format(path))
        return (path, e)



path, res = htmlget(base + "/abc")
print(path)
print(res)

logger.debug("what uuup")
