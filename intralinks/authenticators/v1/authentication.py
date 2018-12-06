"""
For educational purpose only
"""

import intralinks.api.v1
from intralinks.utils.xml import to_xml
import time

class SecureIdRequiredException(Exception):
    pass

class AlreadyLoggedInException(Exception):
    pass

def login(api_client, email, password):
    """
    How to allow concurrent login?
    """

    timestamp = time.time()

    response = api_client.create(
        '/v1/ILCGLServices/session', 
        data={
            'xml':to_xml({
                'email':email, 
                'password':password, 
                'apiKey':api_client.config.api_key
            }, 'createSession')
        },
        authenticated=False,
        api_version=1
    )

    response.assert_status_code(200)
    response.assert_content_type('text/xml')

    data = response.data()

    if api_client.session is None:
        api_client.session = intralinks.api.v1.Session()

    try:
        response.assert_no_errors(200)

        api_client.session.session_id = data['ssoSessionId']
        api_client.session.timestamp = timestamp
        api_client.session.email = email
        api_client.password = None
        api_client.session.is_secureid_required = False
        api_client.session.is_already_logged_in = False

    except Exception as e:
        status = data['status']

        if 'subcode' in status:
            if status['subcode'] == '011': # secure id required
                api_client.session.email = email
                api_client.session.password = password
                api_client.session.is_secureid_required = True

                raise SecureIdRequiredException()

            elif status['subcode'] == '018': # concurrent login
                api_client.session.email = email
                api_client.session.password = password
                api_client.session.is_already_logged_in = True

                raise AlreadyLoggedInException()
        
        raise e

    return data

def special_login(api_client, email, password, secure_id=None, end_other_sessions=False):
    timestamp = time.time()

    response = api_client.create(
        '/services/logon', 
        data={
            'xml':to_xml({
                'username':email, 
                'password':password, 
                'securID':secure_id,
                'continueMultiLogon':end_other_sessions
            }, 'logonRequest')
        },
        authenticated=False,
        api_version=1
    )
        
    response.assert_status_code(200)
    response.assert_content_type('text/xml')
    response.assert_no_errors()
    
    data = response.data()

    if api_client.session is None:
        api_client.session = intralinks.api.v1.Session()

    api_client.session.session_id = data['sessionId']
    api_client.session.timestamp = timestamp
    
    return data

def logout(api_client):
    response = api_client.delete(
        '/services/session',
        api_version=1
    )

    data = response.data()

    return data

def get_flags(api_client):
    response = api_client.get(
        '/services/flags',
        api_version=1
    )

    response.assert_status_code(200)
    response.assert_content_type('text/xml')
    response.assert_no_errors()

    data = response.data()

    return data['flags']
