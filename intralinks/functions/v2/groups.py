"""
For educational purpose only
"""

from intralinks.utils.data import get_node_as_list, get_node_as_item, filter_dict, entity_to_dict
import json
import intralinks.functions.entities

def get_groups(api_client, exchange_id):
    response = api_client.get(
        '/v2/workspaces/{}/groups'.format(exchange_id),
        api_version=2
    )
    
    response.check(200, 'application/json')
    
    data = response.data()
    
    return get_node_as_list(data, 'groups')

def get_groups_and_members(api_client, exchange_id):
    response = api_client.get(
        '/v2/workspaces/{}/groups'.format(exchange_id), 
        params={'includeWorkspaceGroupMembers':'true'},
        api_version=2
    )
    
    response.check(200, 'application/json')

    data = response.data()
    
    return (
        get_node_as_list(data, 'groups'), 
        get_node_as_list(data, 'workspaceGroupMembers')
    )

def create_group(api_client, exchange_id, group):
    group_data = entity_to_dict(group)
    
    response = api_client.create(
        '/v2/workspaces/{}/groups'.format(exchange_id), 
        data=json.dumps(group_data), 
        headers={'Content-Type':'application/json'},
        api_version=2
    )
    
    response.check(201, 'application/json')
    
    data = response.data()
    
    return get_node_as_item(data, 'groupPartials')

def create_groups(api_client, exchange_id, groups):
    response = api_client.create(
        '/v2/workspaces/{}/groups'.format(exchange_id), 
        data=json.dumps(new_groups), 
        headers={'Content-Type':'application/json'},
        api_version=2
    )
    
    response.check(201, 'application/json')

    data = response.data()
    
    return get_node_as_list(data, ['workspaceGroups', 'workspaceGroupPartial'])

def create_group_member(api_client, exchange_id, group_id, exchange_member_id):
    new_user = {'workspaceUserId': exchange_member_id}
    
    response = api_client.create(
        '/v2/workspaces/{}/groups/{}/users'.format(exchange_id, group_id), 
        data=json.dumps({'users':[new_user]}), 
        headers={'Content-Type':'application/json'},
        api_version=2
    )
    
    response.check(202, 'application/json')
    
    data = response.data()
    
    return data

def delete_group(api_client, exchange_id, id, version, remove_users=False):   
    response = api_client.delete(
        '/v2/workspaces/{}/groups'.format(exchange_id),
        params={
            'removeUsers':remove_users
        },
        data=json.dumps({'groups':[{'id':id, 'version':version}]}),
        headers={'Content-Type':'application/json'},
        api_version=2
    )
    
    response.check(202, 'application/json')
    
    data = response.data()
    
    return data

def delete_groups(api_client, exchange_id, groups, remove_users=False): 
    raise Exception()

def delete_group_member(api_client, exchange_id, group, exchange_member):
    raise Exception()

def update_group(api_client, exchange_id, group, remove_group_members=None, add_group_members=None):
    group_data = entity_to_dict(group)

    group_id = group_data['id']

    group_data = filter_dict(group_data, remove_fields={'id', 'groupMemberCount', 'lastModifiedOn', 'lastModifiedBy', 'createdOn', 'createdBy'})
    
    response = api_client.update(
        '/v2/workspaces/{}/groups/{}'.format(exchange_id, group_id), 
        data=json.dumps(group_data), 
        headers={'Content-Type':'application/json'},
        api_version=2
    )
    
    response.check(202, 'application/json')
    
    data = response.data()
    
    return get_node_as_item(data, 'groupPartials')