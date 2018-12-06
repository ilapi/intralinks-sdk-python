"""
For educational purpose only
"""

import intralinks.api.v2
import time
import urllib.parse

def login(api_client, email, password, end_other_sessions=False):
    timestamp = time.time()

    response = api_client.create(
        '/v2/oauth/token', 
        data={
            'grant_type':'client_credentials',
            'client_id':api_client.config.client_id,
            'client_secret':api_client.config.client_secret,
            'endOtherSessions':'true' if end_other_sessions else 'false',
            'email':email,
            'password':password
        },
        authenticated=False,
        api_version=2
    )
    
    response.assert_status_code(200)
    response.assert_content_type('application/json')
    
    data = response.data()
    
    if 'access_token' not in data:
        raise Exception(response.url, response.text)
    
    api_client.session = intralinks.api.v2.Session()
    api_client.session.access_token = data['access_token']
    api_client.session.timestamp = timestamp
    api_client.session.email = email
    
    return api_client.session.access_token

def build_oauth_url(api_client, state, end_other_sessions=False):
    oauth_url = urllib.parse.urlencode({
        'client_id':api_client.config.client_id, 
        'state':state, 
        'scope':'ilservices', 
        'endOtherSessions':'true' if end_other_sessions else 'false'
    })

    return api_client.base_url + '/v2/oauth/authorize?' + oauth_url

def validate_oauth_code(api_client, code):
    timestamp = time.time()

    response = api_client.create(
        '/v2/oauth/token', 
        data={
            'grant_type':'authorization_code',
            'client_id':api_client.config.client_id,
            'client_secret':api_client.config.client_secret,
            'endOtherSessions':'true',
            'code':code
        },
        authenticated=False,
        api_version=2
    )
    
    response.assert_status_code(200)
    response.assert_content_type('application/json')
    
    data = response.data()
    
    if 'access_token' not in data:
        raise Exception(response.url, response.text)
    
    api_client.session = intralinks.api.v2.Session()
    api_client.session.access_token = data['access_token']
    api_client.session.timestamp = timestamp
    
    return api_client.session.access_token

def logout(api_client):
    response = api_client.update(
        '/v2/oauth/revoke', 
        data={
            'token':api_client.session.access_token,
            'client_id':api_client.config.client_id,
            'client_secret':api_client.config.client_secret
        },
        api_version=2
    )
    
    response.assert_status_code(200)
    response.assert_content_type('application/json')
    
    data = response.data()

    return data