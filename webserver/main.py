#!/usr/bin/env python

from flask import Flask, render_template
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app)

setup=True

@app.route("/")
def homepage():
	if setup:
		return render_template('connect.html', networks=["Test", "Test2", "Test3"])
	else:
		return render_template('connect.html', networks=[])

@socketio.on('connect')
def connect_handle():
	print("User connected")

if __name__ == "__main__":
	socketio.run(app)
