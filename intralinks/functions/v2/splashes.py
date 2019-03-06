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
    
    response.check(200, 'application/json')
    
    data = response.data()
    
    return get_node_as_item(data, 'splash')

def enter_exchange(api_client, exchange_id, accept_splash=False, one_time_password=False):

    enter_content = {'acceptSplash': accept_splash}

    if one_time_password:
        enter_content['oneTimePassword'] = one_time_password

    response = api_client.create(
        '/v2/workspaces/{}/splash'.format(exchange_id), 
        data=json.dumps(enter_content), 
        headers={'Content-Type': 'application/json'},
        api_version=2
    )
    
    response.check(201, 'application/json')
    
    data = response.data()
    
    return get_node_as_item(data, 'state')

def delete_exchange_entry(api_client, exchange_id):
    raise Exception()
