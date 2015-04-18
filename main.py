import data
import persistence
from flask import Flask
from flask.ext import restful
from flask import jsonify

app = Flask(__name__)
api = restful.Api(app)

class News(restful.Resource):
    def get(self):
        ret = {"news": persistence.get_news()}
        return jsonify(ret)

class Update(restful.Resource):
    def get(self):
        return persistence.get_network()['update']

class BusNewtork(restful.Resource):
    def get(self):
        ret = {"busnetwork": persistence.get_network()}
        return jsonify(ret)

@app.route('/')
def home():
    return "<h3>Tursib web service</h3>"

@app.route('/update_bus_network')
def update_bus_network():
    """Get a newer version of bus info if available.
    Run this periodically."""
    # Download and save to local storage if a different version is available.
    if _new_version_available():
        network = data.bus_network()
        persistence.save_network(network)      

def _new_version_available():
    if _tursib_version() != _local_version():
        return True
    return False

def _tursib_version():
    """:return: string containing the last update text"""
    return data.bus_network_latest_update()

def _local_version():
    """:return: Local version string of the bus network info."""
    network = persistence.get_network()
    return network['updatestring']


api.add_resource(News, '/news')
api.add_resource(Update, '/update')
api.add_resource(BusNewtork, '/busnetwork')

if __name__ == '__main__':
    app.run(debug=True)
