from flask import Blueprint, request, current_app, jsonify, render_template, redirect, make_response
from fuzzyman.api.controller import convert_file
api = Blueprint('api', __name__)


@api.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@api.route('/convert', methods=['POST'])
def conv_file():
    return convert_file()