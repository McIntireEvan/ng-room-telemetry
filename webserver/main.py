#!/usr/bin/env python

from flask import Flask, render_template
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app)

@app.route("/")
def hello():
	return render_template('index.html')

@socketio.on('connect')
def connect_handle():
	print("User connected")

if __name__ == "__main__":
	socketio.run(app)
