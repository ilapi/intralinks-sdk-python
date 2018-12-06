"""
For educational purpose only
"""

from intralinks.utils.data import get_node_as_list, get_node_as_item, entity_to_dict, filter_dict
import json

def get_exchange_members(api_client, exchange_id):
    response = api_client.get(
        '/v2/workspaces/{}/users'.format(exchange_id),
        api_version=2
    )
    
    response.assert_status_code(200)
    response.assert_content_type('application/json')
    response.assert_no_errors()
    
    data = response.data()
    
    return get_node_as_list(data, 'users')

def create_exchange_member(api_client, exchange_id, exchange_member=None, alert=None):
    exchange_member_data = entity_to_dict(exchange_member)

    user_data = entity_to_dict(exchange_member_data.pop('user', dict()))
    exchange_member_data.update(user_data)
    
    exchange_member_data = filter_dict(exchange_member_data, remove_fields={'languagePref', 'unauthenticatedDocumentAccess'})

    exchange_member_data['sendAlert'] = alert is not None

    if alert is None:
        exchange_member_data['sendAlert'] = False

    else:
        exchange_member_data['sendAlert'] = True

        alert_data = entity_to_dict(alert)
        alert_data['saveAlertSettings'] = True

        exchange_member_data['welcomeAlertDetails'] = alert_data
    
    response = api_client.create(
        '/v2/workspaces/{}/users'.format(exchange_id),
        data=json.dumps({'users':[exchange_member_data]}), 
        headers={'Content-Type':'application/json'},
        api_version=2
    )
    
    response.assert_status_code(201)
    response.assert_content_type('application/json')
    response.assert_no_errors()
    
    data = response.data()
    
    return get_node_as_item(data, ['userPartials'])

def update_exchange_member(api_client, exchange_id, exchange_member, add_groups=None, remove_groups=None):
    raise Exception()

def delete_exchange_member(api_client, exchange_id, id=None, version=None):
    response = api_client.delete(
        '/v2/workspaces/{}/users'.format(exchange_id),
        data=json.dumps({'users':[{'id':id, 'version':version}]}),
        headers={'Content-Type':'application/json'},
        api_version=2
    )
    
    response.assert_status_code(202)
    response.assert_content_type('application/json')
    response.assert_no_errors()
    
    data = response.data()
    
    return data
    
def delete_exchange_members(api_client, exchange_id, exchange_members):
    raise Exception()

def get_removed_exchange_members(api_client, exchange_id):
    raise Exception()
    

