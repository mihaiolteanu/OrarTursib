import urllib.parse
import requests
import datetime
import os

# Retrieve html page from web.
base = "http://www.tursib.ro"
def htmlget(address):
    path = urllib.parse.urljoin(base, address)
    resp = requests.get(path)
    return resp.text

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
