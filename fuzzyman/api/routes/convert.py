from flask import Blueprint, request, current_app, jsonify
from prance import ResolvingParser
from werkzeug.utils import secure_filename
from fuzzyman.util import (
    get_host,
    get_method_from_path,
    get_parameters_for_path,
    get_path_parameters_for_path,
    get_paths,
    get_schemes
)
from fuzzyman.request import Request
from fuzzyman.collection import Collection

import uuid
import json
import base64
import os

api = Blueprint('api', __name__)

ALLOWED_EXTENSIONS = {'yml', 'yaml'}
def allowed_file(filename):
    ext = filename.rsplit('.', 1)[1].lower()
    if '.' in filename and ext in ALLOWED_EXTENSIONS:
        return filename, ext
    raise Exception(f"Invalid filename or extension")
           



@api.route('/convert', methods=['POST'])
def convert_file():

    file = request.files['file']

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

    c = Collection()

    for path in paths:
        methods = get_method_from_path(spec=parser.specification, path=path)
        for method in methods:
            parameters = get_parameters_for_path(spec=parser.specification, path=path, method=method)
            c.item.append(Request(f"{method.upper()} - {path}", path, host, schemes[0], method, parameters=parameters))

    return json.dumps(json.loads(str(c)))