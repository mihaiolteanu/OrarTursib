#import urllib.request
import datetime
import os

# Retrieve html page from web.
# def html_retrieve(address):
#     # Check if address is an url.
#     #parts = urlparse(address)
#     #if parts.netloc:
#         return urllib.request.urlopen(address).read()


# Path to html local samples taken from tursib.ro
samples_path = os.path.join(os.path.dirname(__file__), r"samples")


def html_retrieve(address):
    """
    Return local previously saved files instead of returning them from web.
    :param address: tursib real address
    :return: local html file
    """
    if address == "www.tursib.ro":
        return open(os.path.join(samples_path, "tursib_ro.htm"))

    if address == "www.tursib.ro/trasee":
        return open(os.path.join(samples_path, "tursib_ro_trasee_minimal.htm"))

    # Requests of the form: http://tursib.ro/traseu/11/program?statie=1&dir=dus
    if "tursib.ro/traseu/" in address and "program?statie=" in address:
        return open(os.path.join(samples_path, "TRASEUL 11 - SC CONTINENTAL.htm"))

    # Requests of the form: http://tursib.ro/traseu/11/ (notice the similarity with the previous case).
    if "tursib.ro/traseu/" in address:
        return open(os.path.join(samples_path, "TRASEUL 11.htm"))

    if "http://tursib.ro/news/show/" in address:
        return open(os.path.join(samples_path, "news_160.htm"))


def remove_non_ascii(s):
    return "".join(i for i in s if ord(i)<126 and ord(i)>31)

# Months names in Romanian
months_name_ro = {
    'ianuarie': 1,
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
    'decembrie': 12
}


def get_file(name, path):
    """ Returns all files with the given extension from the path specified.
    :param name: file extension (".json", ".txt", ".xml", etc.)
    :param path: absolute path to search in
    :return: list of files with the given extension
    """
    result = []
    for file in os.listdir(path):
        if file.endswith(extension):
            result.append(file)
    return result