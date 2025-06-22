from flask import Flask, request, jsonify
from blackbird import verifyUsername, initiate
import src.config as config
from rich.console import Console
import traceback
from src.modules.utils.userAgent import getRandomUserAgent

app = Flask(__name__)


# Configurações obrigatórias
config.console = Console()
config.filter = None
config.no_nsfw = None
config.dump = None
config.verbose = None
config.proxy = None
config.timeout = 10
config.ai = None
config.aiModel = None
config.pdf = None
config.json = None
config.csv = None
config.max_concurrent_requests = 30


def adapt_result(item, username):
    return {
        "ids": {
            meta.get("name"): meta.get("value")
            for meta in (item.get("metadata") or [])
            if meta.get("name") is not None
        },
        "site_name": item.get("name", ""),
        "status": "Claimed" if item.get("status") == "FOUND" else "Available",
        "tags": [item.get("category")] if item.get("category") else [],
        "url": item.get("url", ""),
        "username": username
    }


@app.route('/api/v2/username', methods=['POST'])
def lookup():
    data = request.get_json()
    username = data.get('query')
    if not username:
        return jsonify({'error': 'Username is required'}), 400

    try:
        config.currentUser = username
        config.userAgent = getRandomUserAgent(config)

        results = verifyUsername(username, config)

        if not results:
            return jsonify({'error': 'An error occurred'}), 500

        if len(results) == 0:
            return jsonify({'error': 'No accounts found'}), 404
        
        accounts = [adapt_result(item, username) for item in results]


        return jsonify({
            'accounts': accounts,
        })
    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5000)