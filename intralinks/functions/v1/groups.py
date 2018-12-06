"""
For educational purpose only
"""

from intralinks.utils.data import get_node_as_list, entity_to_dict
from intralinks.utils.xml import to_xml
import intralinks.functions.v1.exchange_members
import intralinks.functions.entities

def get_groups(api_client, exchange_id):
    response = api_client.get(
        '/v1/services/workspaces/workspaceGroups', 
        params={
            'workspaceId':exchange_id
        },
        api_version=1
    )

    response.assert_status_code(200)
    response.assert_content_type('text/xml')
    response.assert_no_errors()

    data = response.data()

    return get_node_as_list(data, ('workspaceGroups', 'workspaceGroup'))

def get_groups_and_members(api_client, exchange_id):
    response = api_client.get(
        '/v1/services/workspaces/workspaceGroups', 
        params={
            'workspaceId':exchange_id, 
            'includeWorkspaceGroupMembers':True
        },
        api_version=1
    )

    response.assert_status_code(200)
    response.assert_content_type('text/xml')
    response.assert_no_errors()

    data = response.data()

    return (get_node_as_list(data, ('workspaceGroups', 'workspaceGroup')), get_node_as_list(data, ('workspaceGroupMembers', 'workspaceGroupMember')))

def create_group(api_client, exchange_id, group):  
    group_data = entity_to_dict(group)

    response = api_client.create(
        '/v1/services/workspaces/workspaceGroups', 
        params={
            'workspaceId':exchange_id
        }, 
        data={'xml':to_xml(group_data, ['workspaceGroup', 'workspaceGroups', 'workspaceGroupCreateRequest'])},
        api_version=1
    )
    
    response.assert_status_code(200)
    response.assert_content_type('text/xml')
    response.assert_no_errors()

    data = response.data()
    
    return data['workspaceGroups']['workspaceGroupPartial']

def create_groups(api_client, exchange_id, groups):  
    # '5-2-5', 'Multiple Workspace Group creation is not supported'
    raise Exception('Multiple Workspace Group creation is not supported')

def update_group(api_client, exchange_id, group, remove_group_members=None, add_group_members=None):
    data = [
        '<workspaceGroupUpdateRequest>',
        to_xml(group, ['workspaceGroup'])
    ]

    if remove_group_members is not None and len(remove_group_members) > 0:
        data.append(to_xml(remove_group_members, ['workspaceUser', 'removeWorkspaceUsers']))

    if add_group_members is not None and len(add_group_members) > 0:
        data.append(to_xml(add_group_members, ['workspaceUser', 'addWorkspaceUsers']))
    
    data.append('</workspaceGroupUpdateRequest>')

    response = api_client.update(
        '/v1/services/workspaces/workspaceGroups', 
        params={
            'workspaceId':exchange_id,
            'workspaceGroupId':group['id']
        }, 
        data={'xml':''.join(data)},
        api_version=1
    )
    
    response.assert_status_code(200)
    response.assert_content_type('text/xml')
    response.assert_no_errors()

    data = response.data()
    
    return data['workspaceGroups']['workspaceGroupPartial']

def delete_group(api_client, exchange_id, id, version, remove_users=False):   
    groups = [{'id':id, 'version':version}]

    return delete_groups(api_client, exchange_id, groups, remove_users)

# '5-2-13', 'You tried to delete more groups than the currently allowed at one time.'

def delete_groups(api_client, exchange_id, groups, remove_users=False): 
    deleted_groups = [
        {
            'id':g['id'], 
            'version':g['version'], 
            'type':'WORKSPACEGROUP'
        } for g in groups
    ]
     
    response = api_client.delete(
        '/v1/services/workspaces/workspaceGroups', 
        params={
            'workspaceId':exchange_id,
            'removeUsers':remove_users
        }, 
        data={'xml':to_xml(deleted_groups, ['entityId', 'workspaceGroupDeleteRequest'])},
        api_version=1
    )
    
    response.assert_status_code(200)
    response.assert_content_type('text/xml')
    response.assert_no_errors()

    data = response.data()
    
    return data

def add_member_to_group(api_client, exchange_id, group, exchange_member):
    return intralinks.functions.v1.exchange_members.update_exchange_member(
        api_client, 
        exchange_id, 
        exchange_member, 
        add_groups=[group]
    )

def remove_member_from_group(api_client, exchange_id, group, exchange_member):  
    return intralinks.functions.v1.exchange_members.update_exchange_member(
        api_client, 
        exchange_id, 
        exchange_member, 
        remove_groups=[group]
    )