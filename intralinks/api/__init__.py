import requests

import intralinks.utils.xml
import intralinks.utils.data
import intralinks.api.logger

class ApiClient:
    def __init__(self, config=None, session=None, verify_ssl=True):
        self.config = config
        self.session = session
        self.logger = intralinks.api.logger.ApiLogger1()
        self.verify_ssl = verify_ssl

    def is_v1(self):
        return self.config is not None and isinstance(self.config, intralinks.api.v1.Config)

    def is_v2(self):
        return self.config is not None and isinstance(self.config, intralinks.api.v2.Config)

    def get_http_elements_v1(self, method, params=None):
        http_method = {'GET':requests.get, 'DELETE':requests.post, 'CREATE':requests.post, 'UPDATE':requests.post}[method]
        http_params = {'method':method, 'httpStatus':'F'} 

        if hasattr(self.config, 'client'):
            http_params['client'] = self.config.client
        
        if params is not None:
            convert = lambda v: ('T' if v else 'F') if isinstance(v, bool) else v
            http_params.update({k:convert(v) for (k, v) in params.items() if v is not None})

        return http_method, http_params
    
    def get_http_elements_v2(self, method, params):
        http_method = {'GET':requests.get, 'DELETE':requests.delete, 'CREATE':requests.post, 'UPDATE':requests.put}[method]
        http_params = None if params is None else {k:v for (k, v) in params.items() if v is not None}

        return http_method, http_params
    
    def get_http_elements(self, method, params, headers, authenticated, api_version):
        http_headers = headers if headers else dict()
        http_cookies = dict()

        if authenticated:
            self.session.apply(http_headers, http_cookies)

        if api_version == 1:
            http_method, http_params = self.get_http_elements_v1(method, params)

        elif api_version == 2:
            http_method, http_params = self.get_http_elements_v2(method, params)
            
        else:
            raise Exception()
        
        return http_method, http_params, http_cookies, http_headers

    def get(self, relative_url, params=None, stream=False, api_version=None):
        http_method, http_params, http_cookies, http_headers = self.get_http_elements('GET', params, headers=None, authenticated=True, api_version=api_version)

        response = http_method(
            self.config.base_url + relative_url, 
            params=http_params, 
            cookies=http_cookies,
            headers=http_headers,
            stream=stream,
            verify=self.verify_ssl
        )

        if self.logger:
            self.logger.log_get(response, self.config.base_url, relative_url, http_params, http_cookies, http_headers, stream)
        
        self.last_response = response

        return ApiResponse(response)

    def create(self, relative_url, params=None, data=None, files=None, headers=None, authenticated=True, api_version=None): # NOSONAR
        http_method, http_params, http_cookies, http_headers = self.get_http_elements('CREATE', params, headers, authenticated=authenticated, api_version=api_version)

        response = http_method(
            self.config.base_url + relative_url, 
            params=http_params, 
            data=data,
            files=files,
            cookies=http_cookies,
            headers=http_headers,
            verify=self.verify_ssl
        )
            
        if self.logger:
            self.logger.log_post(response, self.config.base_url, relative_url, http_params, data, http_cookies, http_headers)

        self.last_response = response

        return ApiResponse(response)

    def update(self, relative_url, params=None, data=None, files=None, headers=None, authenticated=True, api_version=None): # NOSONAR
        http_method, http_params, http_cookies, http_headers = self.get_http_elements('UPDATE', params, headers, authenticated=authenticated, api_version=api_version)

        response = http_method(
            self.config.base_url + relative_url, 
            params=http_params, 
            data=data,
            files=files,
            cookies=http_cookies,
            headers=http_headers,
            verify=self.verify_ssl
        )

        if self.logger:
            self.logger.log_post(response, self.config.base_url, relative_url, http_params, data, http_cookies, http_headers)

        self.last_response = response

        return ApiResponse(response)
    
    def delete(self, relative_url, params=None, data=None, headers=None, api_version=None):
        http_method, http_params, http_cookies, http_headers = self.get_http_elements('DELETE', params, headers, authenticated=True, api_version=api_version)

        response = http_method(
            self.config.base_url + relative_url, 
            params=http_params, 
            data=data,
            cookies=http_cookies,
            headers=http_headers,
            verify=self.verify_ssl
        )

        if self.logger:
            self.logger.log_delete(response, self.config.base_url, relative_url, http_params, http_cookies, http_headers)

        self.last_response = response

        return ApiResponse(response)

class ApiResponse:
    def __init__(self, response):
        self.response = response
        self._data = None
    
    def data(self):
        if self._data is not None:
            return self._data

        elif self.content_type() == 'application/json':
            self._data = self.response.json()

        elif self.content_type() == 'text/xml':
            self._data = intralinks.utils.xml.from_xml(self.response.content)

        elif self.content_type() == 'text/html':
            self._data = {'error':self.response.text}

        else:
            self._data = self.response.text
        
        return self._data
    
    def dump(self, fp):
        for chunk in self.response.iter_content(chunk_size=1024): 
            if chunk: 
                fp.write(chunk)
    
    def status_code(self):
        return self.response.status_code
    
    def content_type(self):
        return self.response.headers.get('Content-Type', '').split(';')[0]

    def _get_error(self, d):
        error = None

        if 'errors' in d:
            error = intralinks.utils.data.get_node_as_list(d, 'errors')[0]

        elif 'error' in d:
            error = intralinks.utils.data.get_node_as_list(d, 'error')[0]
        
        elif 'fault' in d:
            error = d['fault']
        
        return error

    def _raise_error(self):
        d = self.data()

        code = None
        subcode = None
        message = None

        error = self._get_error(d)
        
        if error:
            if 'code' in error:
                code = error['code']

            if 'message' in error:
                message = error['message']
            elif 'description' in error:
                message = error['description']
            elif 'faultstring' in error:
                message = error['faultstring']

            if 'subCode' in error:
                subcode = error['subCode']
            elif 'subcode' in error:
                subcode = error['subcode']

        raise ApiException(code, subcode, message, self.response)

    def assert_status_code(self, expected_status_code):
        if isinstance(expected_status_code, int):
            expected_status_code = {expected_status_code}

        if self.status_code() not in expected_status_code:
            self._raise_error()
    
    def assert_content_type(self, expected_content_type):
        if isinstance(expected_content_type, str):
            expected_content_type = {expected_content_type}

        if self.content_type() not in expected_content_type:
            raise Exception(
                self.response.url, 
                self.response.status_code, 
                self.response.headers['Content-Type'], 
                self.response.text
            )
    
    def assert_no_errors(self, expected_code=None):
        d = self.data()

        if self._get_error(d):
            self._raise_error()

        if expected_code is not None and d['status']['code'] != expected_code:
            raise Exception(
                self.response.url, 
                self.response.status_code, 
                self.response.headers['Content-Type'], 
                self.response.text,
                d
            )  

    def assert_ok(self, expected_status_code, expected_content_type):
        self.assert_status_code(expected_status_code) 
        self.assert_content_type(expected_content_type)
        self.assert_no_errors()         

class ApiException(Exception):
    def __init__(self, code=None, subcode=None, message=None, request=None):
        self.code = code
        self.subcode = subcode
        self.message = message
        self.request = request

    def is_user_unknown(self):
        return self.subcode == '3-1'

    def is_user_already_a_member(self):
        return self.subcode == '5-1-1'
    
    # '1-1-3-2', "User's current session is invalid.This may be due to session timeout or concurrent login "
