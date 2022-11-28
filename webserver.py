import asyncio
from flask import Flask, Response, render_template, request, jsonify, send_file
from flask_cors import CORS
from blackbird import findUsername
import logging
import requests

app = Flask(__name__, static_folder='templates/static')
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
CORS(app, resources={r"/*": {"origins": "*"}})
loop = asyncio.get_event_loop()
logging.getLogger('werkzeug').disabled = True


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/search/username' ,methods=["POST"])
def searchUsername():
    content = request.get_json()
    username = content['username']
    interfaceType = 'web'
    results = loop.run_until_complete(findUsername(username, interfaceType))
    return jsonify(results)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9797)
