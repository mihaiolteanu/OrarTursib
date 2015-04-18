import urllib
import datetime
import os

# Retrieve html page from web.
base = "http://www.tursib.ro"
def htmlget(address):
    absolute = urllib.parse.urljoin(base, address)
    return urllib.request.urlopen(absolute).read()

def remove_non_ascii(s):
    return "".join(i for i in s if ord(i)<126 and ord(i)>31)

# Months names in Romanian
months_name_ro = {
    'ianuarie': 1, # January
    'februarie': 2,
    'martie': 3,
    'aprilie': 4,
    'mai': 5,
    'iunie': 6,
    'iulie': 7,
    'august': 8,
    'septembrie': 9,
    'octombrie': 10,
    'noiembrie': 11,
    'decembrie': 12 # December
}
