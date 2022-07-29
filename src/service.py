import asyncio
import logging

import requests
from flask import (Blueprint, Flask, Response, current_app, jsonify,
                   render_template, request)
from flask_cors import CORS

from src.core import BlackBird

blueprint = Blueprint('base', __name__, template_folder='../templates')
loop = asyncio.get_event_loop()


@blueprint.route('/')
def home():
    return render_template('index.html')


@blueprint.route('/search/username', methods=['POST'])
def find_user_name():
    blackbird: BlackBird = current_app.config['CORE']
    username = request.get_json()['username']
    results = loop.run_until_complete(blackbird.find_user_name(username))
    return jsonify(results)


@blueprint.route('/image', methods=['GET'])
def get_image():
    url = request.args.get('url')
    bin_image = requests.get(url).content
    return Response(bin_image, mimetype='image/gif')


class Webserver:
    def __init__(self, blackbird: BlackBird):
        self.app = Flask(__name__, static_folder='../templates/static')

        # Installing configurations
        self.app.config['CORS_HEADERS'] = 'Content-Type'
        self.app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
        self.app.config['CORE'] = blackbird

        self.app.register_blueprint(blueprint)
        # Add CORS middleware
        CORS(self.app, resources={r'/*': {'origins': '*'}})

        # Disable `werkzeug` logging
        logging.getLogger('werkzeug').disabled = True

    def run(self, ip: str = '0.0.0.0', port: int = 9797):
        self.app.run(ip, port)
