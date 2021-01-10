import json

class RequestEncoder(json.JSONEncoder):    
    def default(self, o):
        if isinstance(o, Request):
            request = {}
            request['name'] = o.name
            request['request'] = {}

            request['request']['url'] = o.fuzzed_url
            request['request']['method'] = o.method
            if o.header:
                request['request']['header'] = o.header
            
            if o.body:
                request['request']['body'] = o.body
            
            if o.description:
                request['request']['description'] = o.description
            
            return request
        return super().default(o)



class Request(object):
    def __init__(self, name, path, host, scheme, method, header: dict=None, body: dict=None, description: dict=None, parameters: []=None):
        self.name = name
        self.path = path
        self.host = host
        self.scheme = scheme
        self.method = method
        self.header = header
        self.body = body
        self.description = description
        self.parameters = parameters
        self.fuzz_value = 'alsdkfjalsdfjasldfjkalskdjflaksjdf'

        self.path_parameters = []
        self.body_parameters = []
        self.query_parameters = []

        self.unfuzzed_url = self.create_url()
        self.fuzzed_url = self.create_url()

        # self.unfuzzed_body = self.create_body()
        # self.fuzzed_body = self.create_body()

        # self.unfuzzed_query = self.create_query()
        # self.fuzzed_query = self.create_query()

        self._set_params()
        self.fuzz_path_params()
        self.fuzz_query_params()

    def __repr__(self):
        return "{!r}".format(self.__dict__)

    def _set_params(self):
        if not self.parameters:
            return
        for param in self.parameters:
            if param['in'] == 'path':
                self.path_parameters.append(param)
            elif param['in'] == 'body':
                self.body_parameters.append(param)
            elif param['in'] == 'query':
                self.query_parameters.append(param)
            else:
                raise Exception(f"Not sure what {param['in']} parameter is.")

    def fuzz_path_params(self):
        if len(self.path_parameters) == 0:
            self.fuzzed_url = self.unfuzzed_url
        else:
            for param in self.path_parameters:
                text = "{" + param['name'] + "}"
                self.fuzzed_url = self.fuzzed_url.replace(text, self.fuzz_value)
    
    def fuzz_query_params(self):
        if len(self.query_parameters) == 0:
            return
        self.fuzzed_url += "?"

        num_params = len(self.query_parameters)

        for i,param in enumerate(self.query_parameters):
            self.fuzzed_url += param['name'] + "=" + self.fuzz_value
            if i < num_params - 1:
                self.fuzzed_url += "&"
        
        

    def create_url(self):
        return self.scheme + "://" + self.host + self.path
