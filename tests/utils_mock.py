import datetime
import os

# Path to html local samples taken from tursib.ro
samples_path = os.path.join(os.path.dirname('__file__'), "tests/samples")

def htmlget(address):
    """Return local previously saved files instead of returning them from web.
    :param address: tursib real address
    :return: local html file"""
    f = ""
    if address == "tursib_ro": 
        f = "tursib_ro.htm"
    elif address == "trasee": 
        f = "tursib_ro_trasee.htm"
    # Requests of the form: http://tursib.ro/traseu/11/program?statie=1&dir=dus
    elif "traseu" in address and "program?statie=" in address:
        f = "tursib_ro_traseu_11_Conti.htm"
    # Requests of the form: http://tursib.ro/traseu/11/ (notice the similarity with the previous case).
    elif "traseu" in address:
        f = "tursib_ro_traseu_11.htm"
    elif "news/show/" in address:
        f = "news_160.htm"

    with open(os.path.join(samples_path, f), "r",encoding='utf-8', errors='ignore') as f:
        result = f.read()
    return result    

