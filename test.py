from openapi_parser.parser.loader import OpenApiParser
from prance import ResolvingParser
from fuzzyman.request import Request
from fuzzyman.collection import Collection
import json

METHODS = ['get', 'post', 'put', 'patch', 'delete', 'copy', 'head', 'options', 'link', 'unlink', 'purge', 'lock', 'unlock', 'propfind', 'view']

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

def main():
    parser = ResolvingParser('petstore.yaml', strict=False)
    paths = get_paths(parser.specification)
    host = get_host(parser)
    schemes = get_schemes(parser)

    c = Collection()

    # print(f"Host: {host}")
    # print(f"Schemes: {schemes}")
    for path in paths:
        methods = get_method_from_path(spec=parser.specification, path=path)
        # print(f"Path: {path} | Methods: {','.join(methods)}")
        for method in methods:
            parameters = get_parameters_for_path(spec=parser.specification, path=path, method=method)
            c.item.append(Request(f"{method.upper()} - {path}", path, host, schemes[0], method, parameters=parameters))

    print(c)

if __name__ == '__main__':
    main()