#!/usr/bin/env python
import time
import json
import subprocess
from flask import Flask, render_template, request
from flask_socketio import SocketIO, send, emit
from network_utils import get_networks

app = Flask(__name__)
socketio = SocketIO(app)

setup=False

sensors = []
temp_warn = 80
temp_alert = 100

@app.route("/")
def homepage():
	if setup:
		return render_template('connect.html', networks=get_networks())
	else:
		return render_template('dashboard/home.html', sensors=[{'id':'a', 'name':'Living Room', 'current': {'temp': 78, 'gas': True, 'occupancy': 2}}, {'id':'asdsdad', 'name':'Bedroom'}], broadcasting=True)

@app.route("/configure")
def configure():
	pass

@app.route("/sensors/<sensor>")
def sensors_page(sensor):
	return render_template('dashboard/sensor.html', sensor={'id':'a', 'name':'Living Room', 'current': {'temp': 78, 'gas': True, 'occupancy': 2}})

@app.route('/api/post/temp', methods=['POST'])
def api_temperature():
	jsond = request.get_json()
	index = addIfNot(jsond['id'])

	sensors[index]['current']['temp'] = jsond['data']
	sensors[index]['data']['temp'].append({'time': time.time() * 1000, 'data': jsond['data']})

	socketio.emit('temp-data', jsond)
	return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

@app.route('/api/post/occupancy', methods=['POST'])
def api_occupancy():
	jsond = request.get_json()
	index = addIfNot(jsond['id'])

	sensors[index]['current']['occupancy'] = jsond['data']
	sensors[index]['data']['occupancy'].append({'time': time.time() * 1000, 'data': jsond['data']})

	socketio.emit('occupancy-data', jsond)
	return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

@app.route('/api/post/gas', methods=['POST'])
def api_gas():
	jsond = request.get_json()

	sensors[index]['current']['gas'] = jsond['data']

	return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

@socketio.on('request-temp-data')
def connect_handle(id):
	socketio.emit('temp-data-dump', sensors[getIndex(id)]['data']['temp'])

def getIndex(id):
	for i in xrange(0, len(sensors)):
		if(id == sensors[i]['id']):
			return i
	return -1

def addIfNot(id):
	f = False
	for i in xrange(0, len(sensors)):
		if(id == sensors[i]['id']):
			return i
	sensors.append({
		'id': id,
		'current': {
			'temp': 0,
			'occupancy': 0,
			'gas': True
		},
		'data': {
			'temp': [],
			'occupancy': []
		}
	})
	return len(sensors) - 1

def warnings():
	warnings = []
	for i in xrange(0, len(sensors)):
		if (sensors[i].current.temp >= temp_warn) and (sensors[i].current.temp < temp_alert):
			warnings.append(sensors[i])
	return warnings

def alerts():
	alerts = []
	for i in xrange(0, len(sensors)):
		if sensors[i].current.temp > temp_alert:
			alerts.append(sensors[i])
	return alerts

def enable_ap():
	p1 = subprocess.Popen(["./setup/enable_ap.sh"])

if __name__ == "__main__":
	enable_ap()
	socketio.run(app)
