from flask import request, current_app, jsonify, render_template, redirect, make_response
from prance import ResolvingParser
from werkzeug.utils import secure_filename
from fuzzyman.util import (
    get_host,
    get_method_from_path,
    get_parameters_for_path,
    get_path_parameters_for_path,
    get_paths,
    get_schemes,
    build_response
)
from fuzzyman.request import Request
from fuzzyman.collection import Collection

import uuid
import json
import base64
import os
import requests


ALLOWED_EXTENSIONS = {'yml', 'yaml'}
def allowed_file(filename):
    try:
        ext = filename.rsplit('.', 1)[1].lower()
        if '.' in filename and ext in ALLOWED_EXTENSIONS:
            return filename, ext
    except:
        pass
    raise Exception(f"Invalid filename or extension")

# @build_response
def convert_file():
    try:
        file = request.files['file']
    except:
        raise Exception("Must include a file.")

    API = False
    if request.args.get('api'):
        API = True
    
    num_trials = request.args.get('num_trials')
    if num_trials:
        try:
            num_trials = int(num_trials)
        except:
            num_trials = 5
    else:
        num_trials = 5


    if file.filename == '':
        raise Exception("Invalid file")

    f_name, ext = allowed_file(file.filename)

    random_file_name = f"{f_name}-{uuid.uuid4().hex}.{ext}"

    filename = secure_filename(random_file_name)

    file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))

    try:
        parser = ResolvingParser(current_app.config['UPLOAD_FOLDER'] + f"/{filename}", strict=False)
    except:
        raise Exception("Failed to parse openapi upload. Please verify it is valid and try again.")

    paths = get_paths(parser.specification)
    host = get_host(parser)
    schemes = get_schemes(parser)

    c = Collection(name=f_name + " fuzzed")

    for path in paths:
        methods = get_method_from_path(spec=parser.specification, path=path)
        for method in methods:
            parameters = get_parameters_for_path(spec=parser.specification, path=path, method=method)
            for _ in range(num_trials):
                c.item.append(Request(f"{method.upper()} - {path} {_}", path, host, schemes[0], method, parameters=parameters))

    data = json.dumps(json.loads(str(c)))

    if API and os.getenv('POSTMAN_API_KEY'):
        resp = requests.request(
            'POST',
            'https://api.getpostman.com/collections',
            headers={
                'X-Api-Key' : os.getenv('POSTMAN_API_KEY'),
                'Content-Type' : 'application/json'
            },
            data=data
        )
        return {
            "status" : "Created a collection for you."
        }

    response = make_response(render_template('index.html', data=data))

    return response