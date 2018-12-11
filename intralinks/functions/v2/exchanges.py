"""
For educational purpose only
"""

from intralinks.utils.data import get_node_as_list, get_node_as_item, filter_dict, entity_to_dict
import intralinks.functions.entities
import json

def get_exchanges(api_client, brand_id=None, user_id=None, is_manager=None):
    response = api_client.get(
        '/v2/workspaces',
        params={
            'brandId':brand_id,
            'userId':user_id,
            'addUserRight':('T' if is_manager else 'F') if is_manager is not None else None
        },
        api_version=2
    )
    
    response.assert_status_code(200)
    response.assert_content_type('application/json')
    response.assert_no_errors()
    
    data = response.data()
    
    return get_node_as_list(data, 'workspace')

def get_exchange(api_client, exchange_id):
    response = api_client.get(
        '/v2/workspaces/{}'.format(exchange_id),
        api_version=2
    )
    
    response.assert_status_code(200)
    response.assert_content_type('application/json')
    response.assert_no_errors()
    
    data = response.data()

    return get_node_as_item(data, 'workspace')

def create_exchange(api_client, exchange, suppress_welcome_alert=True):
    exchange_data = {'name' if k == 'workspaceName' else k:v for k,v in entity_to_dict(exchange).items()}
    exchange_data['suppressWelcomeAlert'] = suppress_welcome_alert

    response = api_client.create(
        '/v2/workspaces',
        data=json.dumps({'workspaces': [exchange_data]}),
        headers={'Content-Type':'application/json'},
        api_version=2
    )
    
    response.assert_status_code(201)
    response.assert_content_type('application/json')
    response.assert_no_errors()
    
    data = response.data()
    
    return get_node_as_item(data, 'WorkspacePartial')

def update_exchange(api_client, exchange, is_phase_updated=False):
    data = entity_to_dict(exchange)
    exchange_id = data['id']

    if is_phase_updated:
        data = filter_dict(data, remove_fields=['id', 'parentTemplateId', 'actions', 'securityLevel', 'type', 'pvpEnabled', 'htmlViewEnabled', 'location'])
    else:
        data = filter_dict(data, remove_fields=['id', 'parentTemplateId', 'phase', 'actions', 'securityLevel', 'type', 'pvpEnabled', 'htmlViewEnabled', 'location'])

    data['name'] = data.pop('workspaceName')

    response = api_client.update(
        '/v2/workspaces/{}'.format(exchange_id), 
        data=json.dumps(data),
        headers={'Content-Type':'application/json'},
        api_version=2
    )

    response.assert_status_code(202)
    response.assert_content_type('application/json')
    response.assert_no_errors()

    data = response.data()

    return data

def get_exchange_settings(api_client, exchange_id):
    response = api_client.get(
        '/v2/workspaces/{}/settings'.format(exchange_id),
        api_version=2
    )
    
    response.assert_status_code(200)
    response.assert_content_type('application/json')
    response.assert_no_errors()
    
    data = response.data()

    return get_node_as_list(data, 'workspaceSettings')

def update_exchange_settings(api_client, exchange_id, settings):
    response = api_client.update(
        '/v2/workspaces/{}/settings'.format(exchange_id), 
        data=json.dumps({'workspaceSettings': settings}), 
        headers={'Content-Type': 'application/json'},
        api_version=2
    )
    
    response.assert_status_code(201)
    response.assert_content_type('application/json')
    response.assert_no_errors()
    
    data = response.data()
    
    if 'status' not in data:
        raise Exception(response.url, response.text)
    
    status = data['status']
    
    return status