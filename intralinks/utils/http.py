import http.client
import logging
import urllib.parse
import IPython.core.display

def enable_http_log():
    """
    From: https://stackoverflow.com/questions/10588644/how-can-i-see-the-entire-http-request-thats-being-sent-by-my-python-application
    """
    http.client.HTTPConnection.debuglevel = 1

    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)

    requests_log = logging.getLogger("requests.packages.urllib3")
    requests_log.setLevel(logging.DEBUG)
    requests_log.propagate = True

def analyze_last_response(response):  
    u = urllib.parse.urlparse(response.request.url)
    q = urllib.parse.parse_qs(u.query)

    b = {}

    if response.request.headers.get('content-type', default=None) == 'application/x-www-form-urlencoded':
        b = urllib.parse.parse_qs(urllib.parse.unquote(response.request.body))
    elif response.request.headers.get('content-type', default=None) == 'application/json':
        b = {'<body>': response.request.body}
    
    data = {
        'request_url': response.request.url,
        'request_server': u.netloc,
        'request_path': u.path,
        'request_query_params': [(k, q[k][0] if isinstance(q[k], list) and len(q[k]) == 1 else q[k]) for k in sorted(q.keys())],
        'request_body': [(k, b[k][0] if isinstance(b[k], list) and len(b[k]) == 1 else b[k]) for k in sorted(b.keys())],
        'request_method': response.request.method,
        'status_code': response.status_code,
        'response_content_type': response.headers.get('content-type', None),
        'request_content_type': response.request.headers.get('content-type', ''),
        'request_cookie': response.request.headers.get('cookie', ''),
        'request_authorization': response.request.headers.get('authorization', ''),
        'response_content': response.text,
    }
    
    return data
    
def print_last_response(response):
    data = analyze_last_response(response)
    
    data['txt_request_query_params'] = '\n'.join(['- {}: {}'.format(p[0], p[1]) for p in data['request_query_params']])
    data['txt_request_body'] = '\n'.join(['- {}: {}'.format(p[0], p[1]) for p in data['request_body']])
    
    print('''
*** General ***

- Request URL: {request_url}
- Request Server: {request_server}
- Request Path: {request_path}
- Request Method: {request_method}

---------------------------------------

*** Query String Parameters ***

{txt_request_query_params}

---------------------------------------

*** Request Headers ***

- Content-Type: {request_content_type}
- Cookie: {request_cookie}
- Authorization: {request_authorization}

---------------------------------------

*** Request Body ***

{txt_request_body}

---------------------------------------

*** Response ***

- Status Code: {status_code}
- Content-Type: {response_content_type}
- Content

{response_content}
'''.strip().format(**data))

def html_escape(s):
    return s.replace('<', '&lt;').replace('>', '&gt;').replace('\n', '<br>').replace(' ', '&nbsp;')

def display_last_response(response):
    data = analyze_last_response(response)
    
    data = data.copy()
    
    data['html_request_query_params'] = '\n'.join(['<li><span style="color:blue">{}:</span> {}'.format(p[0], html_escape(p[1])) for p in data['request_query_params']])
    data['html_request_body'] = '\n'.join(['<li><span style="color:blue">{}:</span> {}'.format(p[0], html_escape(p[1])) for p in data['request_body']])

    data['response_content'] = html_escape(data['response_content'])
    
    display(IPython.core.display.HTML('''
<p style="font-weight:bold">General</p>

<ul>
<li><span style="color:blue">Request URL:</span> {request_url}
<li><span style="color:blue">Request Server:</span> {request_server}
<li><span style="color:blue">Request Path:</span> {request_path}
<li><span style="color:blue">Request Method:</span> {request_method}
</ul>

<p style="font-weight:bold">Query String Parameters</p>

<ul>
{html_request_query_params}
</ul>

<p style="font-weight:bold">Request Headers</p>

<ul>
<li><span style="color:blue">Content-Type:</span> {request_content_type}
<li><span style="color:blue">Cookie:</span> {request_cookie}
<li><span style="color:blue">Authorization:</span> {request_authorization}
</ul>

<p style="font-weight:bold">Request Body</p>

<ul>
{html_request_body}
</ul>

<p style="font-weight:bold">Response</p>

<ul>
<li><span style="color:blue">Status Code:</span> {status_code}
<li><span style="color:blue">Content-Type:</span> {response_content_type}
<li><span style="color:blue">Content:</span> 
</ul>

<p>{response_content}</p>

'''.strip().format(**data)))