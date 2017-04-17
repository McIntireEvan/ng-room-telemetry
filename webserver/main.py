#!/usr/bin/env python

from flask import Flask, render_template
from flask_socketio import SocketIO
from network_utils import get_networks

app = Flask(__name__)
socketio = SocketIO(app)

setup=False

@app.route("/")
def homepage():
	if setup:
		return render_template('connect.html', networks=["Test", "Test2", "Test3"])
	else:
		return render_template('dashboard/home.html', sensors=[{'id':'a', 'name':'Living Room', 'current': {'temp': 78, 'gas': True, 'occupancy': 2}}, {'id':'asdsdad', 'name':'Bedroom'}])

@app.route("/sensors/<>")

@app.route('/api/post/temp', methods=['POST'])
def api_temperature():
	pass

@app.route('/api/post/occupancy', methods=['POST'])
def api_occupancy():
	pass

@app.route('/api/post/gas', methods=['POST'])
def api_gas():
	pass

@socketio.on('connect')
def connect_handle():
	print("User connected")

if __name__ == "__main__":
	socketio.run(app)
