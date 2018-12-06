"""
For educational purpose only
"""

from intralinks.utils.data import get_node_as_item
import json

def get_splash(api_client, exchange_id):
    response = api_client.get(
        '/v2/workspaces/{}/splash'.format(exchange_id),
        api_version=2
    )
    
    response.assert_status_code(200)
    response.assert_content_type('application/json')
    response.assert_no_errors()
    
    data = response.data()
    
    return get_node_as_item(data, 'splash')

def enter_exchange(api_client, exchange_id, accept_splash=False):
    response = api_client.create(
        '/v2/workspaces/{}/splash'.format(exchange_id), 
        data=json.dumps({'acceptSplash': accept_splash}), 
        headers={'Content-Type': 'application/json'},
        api_version=2
    )
    
    response.assert_status_code(201)
    response.assert_content_type('application/json')
    response.assert_no_errors()
    
    data = response.data()
    
    return get_node_as_item(data, 'state')

def delete_exchange_entry(api_client, exchange_id):
    raise Exception()
