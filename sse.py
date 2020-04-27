import datetime
from flask import Flask, render_template, request, jsonify
from flask_sse import sse
import string
import random

activeHosts={}

app = Flask(__name__)
app.config["REDIS_URL"] = "redis://localhost"
app.register_blueprint(sse, url_prefix='/stream')

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/host')
def host_page():
    letters = string.ascii_uppercase + '0123456789'
    code =  ''.join(random.choice(letters) for i in range(10))
    activeHosts[code] = request.remote_addr
    data = {}
    data['code'] = code
    data['host'] = activeHosts[code]
    return render_template("host.html", data=data)

@app.route('/join')
def join_page():
    return render_template("join.html")

@app.route('/room/<code>', methods=['GET'])
def check_for_room(code):
    return jsonify(code in activeHosts)

@app.route('/answering/<roomCode>')
def answer_page(roomCode):
    return render_template("answering.html", roomCode=roomCode)

@app.route('/ping', methods=['POST'])
def publish_hello():
    data = request.get_json()
    sse.publish({"message": "Hello!"}, type='greeting', channel=data.get("code"))
    return "Message sent!"