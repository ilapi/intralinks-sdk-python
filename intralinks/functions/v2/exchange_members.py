"""
For educational purpose only
"""

from intralinks.utils.data import get_node_as_list, get_node_as_item, entity_to_dict, filter_dict
from intralinks.utils.booleans import convert_to_bool
import json

def get_exchange_members(api_client, exchange_id):
    response = api_client.get(
        '/v2/workspaces/{}/users'.format(exchange_id),
        api_version=2
    )
    
    response.check(200, 'application/json')
    
    data = response.data()
    
    l = get_node_as_list(data, 'users')

    # Fix because the V2 API does not return 'unauthenticatedDocumentAccess' as a boolean
    convert_to_bool(l, 'unauthenticatedDocumentAccess')

    return l

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
    
    response.check(201, 'application/json')
    
    data = response.data()
    
    return get_node_as_item(data, ['userPartials'])

def update_exchange_member(api_client, exchange_id, exchange_member):
    exchange_member_data = entity_to_dict(exchange_member)

    user_data = entity_to_dict(exchange_member_data.pop('user', dict()))
    exchange_member_data.update(user_data)
    
    exchange_member_data = filter_dict(exchange_member_data, remove_fields={'userId', 'emailId', 'firstName', 'lastName', 'title', 'organization', 'officePhone', 'languagePref'})
  
    # Fix because the V2 API does not return 'unauthenticatedDocumentAccess' as a boolean
    if 'unauthenticatedDocumentAccess' in exchange_member_data and exchange_member_data['unauthenticatedDocumentAccess'] in {'T', 'F'}:
        exchange_member_data['unauthenticatedDocumentAccess'] = exchange_member_data['unauthenticatedDocumentAccess'] == 'T'

    response = api_client.update(
        '/v2/workspaces/{}/users'.format(exchange_id),
        data=json.dumps({'users':[exchange_member_data]}), 
        headers={'Content-Type':'application/json'},
        api_version=2
    )
    
    response.check(202, 'application/json')
    
    data = response.data()
    
    return get_node_as_item(data, ['userPartials'])

def delete_exchange_member(api_client, exchange_id, id=None, version=None):
    response = api_client.delete(
        '/v2/workspaces/{}/users'.format(exchange_id),
        data=json.dumps({'users':[{'id':id, 'version':version}]}),
        headers={'Content-Type':'application/json'},
        api_version=2
    )
    
    response.check(202, 'application/json')
    
    data = response.data()
    
    return data
    
def delete_exchange_members(api_client, exchange_id, exchange_members):
    raise Exception()

def get_removed_exchange_members(api_client, exchange_id):
    raise Exception()
    

