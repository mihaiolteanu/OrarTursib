import data
import persistence
from flask import Flask
from flask.ext import restful
from flask import jsonify

app = Flask(__name__)
api = restful.Api(app)

class Update(restful.Resource):
    def get(self):
        return persistence.get_network_update()

class BusNewtork(restful.Resource):
    def get(self):
        return persistence.get_network()

@app.route('/')
def home():
    return "<h3>Tursib web service</h3>"

@app.route('/updatebusnetwork')
def update_bus_network():
    """
    Get a newer version of bus info if available.
    Run this periodically.
    """
    # Download and save to local storage if a different version is available.
    if _new_version_available():
        network = data.bus_network()
        persistence.save_network(network)      
        return "bus network updated"
    else:
        return "everything is already up to date"

def _new_version_available():
    return _tursib_version() != _local_version()

def _tursib_version():
    return data.update()

def _local_version():
    return persistence.get_network_update()

api.add_resource(Update, '/update')
api.add_resource(BusNewtork, '/busnetwork')

if __name__ == '__main__':
    app.run(debug=True)
