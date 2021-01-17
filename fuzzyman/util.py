from prance import ResolvingParser
from flask import url_for, redirect, flash
METHODS = ['get', 'post', 'put', 'patch', 'delete', 'copy', 'head', 'options', 'link', 'unlink', 'purge', 'lock', 'unlock', 'propfind', 'view']

def build_response(func):
    def wrapper(*args, **kwargs):
        try:
            response = func(*args, **kwargs)
        except Exception as e:
            flash(str(e))
            return redirect(url_for('api.index'))
        return response
    return wrapper


def u_is_valid_path(func):
    def wrapper(*args, **kwargs):
        if kwargs.get('spec') is None or kwargs.get('path') is None:
            raise Exception(f"Invalid spec or path provided. Must have a value")
        spec=kwargs['spec']
        path=kwargs['path']
        if path not in get_paths(spec):
            raise Exception(f"Path {path} not in paths openapi spec.")
        return func(*args, **kwargs)
    return wrapper

def u_is_valid_method(func):
    def wrapper(*args, **kwargs):
        method = kwargs.get('method')
        if not method:
            raise Exception(f"Method must be provided.")
        if type(method) is not str:
            raise Exception(f"Method must be a string.")
        if method.lower() not in METHODS:
            raise Exception(f"Method must be one of (case insensitive): {METHODS}")
        return func(*args, **kwargs)
    return wrapper

@u_is_valid_path
def get_method_from_path(spec=None, path=None):
    ''' Returns the methods supported for a given path
    '''
    return spec['paths'][path].keys()

@u_is_valid_path
@u_is_valid_method
def get_parameters_for_path(spec=None, path=None, method=None):
    ''' Returns the parameters field.
    '''    
    return spec['paths'][path][method].get('parameters', None)

@u_is_valid_path
@u_is_valid_method
def get_path_parameters_for_path(spec, path, method):
    pass

def get_paths(spec: dict):
    ''' Returns the paths provided in the spec
    '''
    return spec['paths'].keys()

def get_host(parser: ResolvingParser):
    ''' Returns the hostname provided in the spec
    '''
    return parser.specification['host']

def get_schemes(parser: ResolvingParser):
    ''' Provides the protocol for the provided spec
    '''
    return parser.specification['schemes']