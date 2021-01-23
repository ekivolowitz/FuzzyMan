from flask import Blueprint, request, current_app, jsonify, render_template, redirect, make_response
from fuzzyman.api.controller import convert_file
api = Blueprint('api', __name__)


@api.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@api.route('/convert', methods=['POST'])
def conv_file():
    try:
        return convert_file()
    except:
        if request.args.get('api'):
            return jsonify({"status" : "Failed to create collection. Please ensure the file is valid and try again."})
        else:
            return render_template('index.html'), 400