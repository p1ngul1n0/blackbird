import asyncio
import json
from flask import Flask, Response, render_template, request, jsonify, send_file
from flask_cors import CORS
from blackbird import findUsername, DEFAULT_SEARCH_DATA_FILE_LOCATION
import logging
import requests

app = Flask(__name__, static_folder='templates/static')
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
CORS(app, resources={r"/*": {"origins": "*"}})
loop = asyncio.get_event_loop()
logging.getLogger('werkzeug').disabled = True

file = open(DEFAULT_SEARCH_DATA_FILE_LOCATION)
searchData = json.load(file)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/search/username', methods=["POST"])
def searchUsername():
    content = request.get_json()
    username = content['username']
    interfaceType = 'web'
    results = loop.run_until_complete(
        findUsername(username, interfaceType, searchData))
    return jsonify(results)


@app.route('/image', methods=["GET"])
def getImage():
    url = request.args.get('url')
    try:
        imageBinary = requests.get(url).content
        return Response(imageBinary, mimetype='image/gif')
    except:
        return Response(status=500)


app.run(host='0.0.0.0', port=9797)
