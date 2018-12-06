"""
For educational purpose only
"""

from intralinks.utils.data import get_node_as_list, entity_to_dict
from intralinks.utils.xml import to_xml
import intralinks.functions.entities

def get_exchanges(api_client, brand_id=None, user_id=None, is_manager=None):
    response = api_client.get(
        '/services/workspaces',
        params={
            'brandId':brand_id,
            'userId':user_id,
            'addUserRight':is_manager
        },
        api_version=1
    )
    
    response.assert_status_code(200)
    response.assert_content_type('text/xml')
    response.assert_no_errors()

    data = response.data()

    return get_node_as_list(data, 'workspace')

def get_exchange(api_client, exchange_id):
    response = api_client.get(
        '/services/workspaces',
        params={
            'workspaceId':exchange_id
        },
        api_version=1
    )

    response.assert_status_code(200)
    response.assert_content_type('text/xml')
    response.assert_no_errors()

    data = response.data()

    return get_node_as_list(data, 'workspace')[0]

def get_exchange_settings(api_client, exchange_id):
    response = api_client.get(
        '/v1/services/workspaces/workspaceSettings',
        params={
            'workspaceId':exchange_id
        },
        api_version=1
    )
    
    response.assert_status_code(200)
    response.assert_content_type('text/xml')
    response.assert_no_errors()

    data = response.data()

    return get_node_as_list(data, ('workspaceSettings', 'workspaceSetting'))

def create_exchange(api_client, exchange, suppress_welcome_alert=True):
    exchange_data = {'name' if k == 'workspaceName' else k:v for k,v in entity_to_dict(exchange).items()}
    exchange_data['suppressWelcomeAlert'] = suppress_welcome_alert

    response = api_client.create(
        '/services/workspaces', 
        data={'xml':to_xml(exchange_data, ['workspacesToCreate', 'workspaceCreateRequest'])},
        api_version=1
    )

    response.assert_status_code(200)
    response.assert_content_type('text/xml')
    response.assert_no_errors()

    data = response.data()

    return data['workspacePartial']

def update_exchange(api_client, exchange, is_phase_updated=False):  
    if is_phase_updated:
        data = {k:v for k,v in exchange.items() if k in {'workspaceName', 'phase', 'host', 'version', 'id', 'description'}}
    else:
        # if phase has not been updated and phase is posted to server, then error: <message>Phase updation failed</message><subcode>6-22</subcode>
        data = {k:v for k,v in exchange.items() if k in {'workspaceName', 'host', 'version', 'id', 'description'}}

    response = api_client.update(
        '/services/workspaces', 
        params={'workspaceId':exchange['id']},
        data={'xml':to_xml(data, ['workspace', 'workspaceUpdateRequest'])},
        api_version=1
    )

    response.assert_status_code(200)
    response.assert_content_type('text/xml')
    response.assert_no_errors()

    data = response.data()

    return data

def update_exchange_settings(api_client, exchange_id, settings):
    response = api_client.update(
        '/v1/services/workspaces/workspaceSettings', 
        params={
            'workspaceId':exchange_id
        },
        data={'xml':to_xml(settings, ['workspaceSetting', 'workspaceSettings', 'workspaceSettingsUpdateRequest'])},
        api_version=1
    )

    response.assert_status_code(200)
    response.assert_content_type('text/xml')
    response.assert_no_errors()

    data = response.data()

    return data
















