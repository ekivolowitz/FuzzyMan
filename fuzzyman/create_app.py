from flask import Flask
from flask_cors import CORS

def create_app():
    ''' Follows the pattern here: https://flask.palletsprojects.com/en/1.1.x/patterns/appfactories/
    '''
    app = Flask(__name__, template_folder='templates', static_folder='static')
    app.config['UPLOAD_FOLDER'] = 'uploads'
    from fuzzyman.api.routes.convert import api
    app.register_blueprint(api)

    return app
