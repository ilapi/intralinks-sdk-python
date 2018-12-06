import collections
import pickle

class ApiLogger:
    def log_get(response, base_url, relative_url, params, cookies, headers, stream):
        pass
    def log_delete(response, base_url, relative_url, params, cookies, headers):
        pass    
    def log_post(response, base_url, relative_url, params, data, cookies, headers):
        pass

class ApiLogger1(ApiLogger):
    def __init__(self, maxlen=10):
        self.last_responses = collections.deque(maxlen=maxlen)

    def log_get(self, response, base_url, relative_url, params, cookies, headers, stream):
        self.last_responses.append(response)

    def log_delete(self, response, base_url, relative_url, params, cookies, headers):
        self.last_responses.append(response)

    def log_post(self, response, base_url, relative_url, params, data, cookies, headers):
        self.last_responses.append(response)

class ApiLogger2(ApiLogger):
    def __init__(self, root):
        self.root = root

    def log_get(self, response, base_url, relative_url, params, cookies, headers, stream):
        with open('', 'wb') as fp:
            pickle.dump({
                    'method':'get',
                    'response':response, 
                    'base_url':base_url, 
                    'relative_url':relative_url, 
                    'params':params, 
                    'cookies':cookies, 
                    'headers':headers, 
                    'stream':stream
                }, fp
            )

    def log_delete(self, response, base_url, relative_url, params, cookies, headers):
        with open('', 'wb') as fp:
            pickle.dump({
                    'method':'delete',
                    'response':response, 
                    'base_url':base_url, 
                    'relative_url':relative_url, 
                    'params':params, 
                    'cookies':cookies, 
                    'headers':headers
                }, fp
            )

    def log_post(self, response, base_url, relative_url, params, data, cookies, headers):
        with open('', 'wb') as fp:
            pickle.dump({
                    'method':'post',
                    'response':response, 
                    'base_url':base_url, 
                    'relative_url':relative_url, 
                    'params':params, 
                    'data':data,
                    'cookies':cookies, 
                    'headers':headers
                }, fp
            )