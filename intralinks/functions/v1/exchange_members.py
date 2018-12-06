"""
For educational purpose only
"""

from intralinks.utils.xml import to_xml
from intralinks.utils.data import get_node_as_list, get_node_as_item, entity_to_dict

def get_exchange_members(api_client, exchange_id):
    response = api_client.get(
        '/v1/services/workspaces/workspaceUsers', 
        params={
            'workspaceId':exchange_id
        },
        api_version=1
    )

    response.assert_status_code(200)
    response.assert_content_type('text/xml')
    response.assert_no_errors()

    data = response.data()

    return get_node_as_list(data, ('workspaceUsers', 'workspaceUser'))

def get_removed_exchange_members(api_client, exchange_id):
    response = api_client.get(
        '/services/workspaces/smartfolders/items', 
        params={
            'workspaceId':exchange_id,
            'smartfolderId':51,
            'entityType':'WORKSPACEUSER'
        },
        api_version=1
    )

    response.assert_status_code(200)
    response.assert_content_type('text/xml')
    response.assert_no_errors()

    data = response.data()

    return get_node_as_list(data, ('workspaceUsers', 'workspaceUser'))

def create_exchange_member(api_client, exchange_id, exchange_member=None, groups=None):
    exchange_member_data = entity_to_dict(exchange_member)

    user_data = entity_to_dict(exchange_member_data.pop('user', dict()))
    exchange_member_data.update(user_data)

    data = {'workspaceUsers':{'workspaceUser':exchange_member_data}}

    if groups is not None and len(groups) > 0:
        data['workspaceGroups'] = {'workspaceUserGroup':[]}
        
        for g in groups:
            data['workspaceGroups']['workspaceUserGroup'] = {
                'emailIds':{'emailId':exchange_member_data['user']},
                'workspaceGroupId':g['id']
            }

    response = api_client.create(
        '/v1/services/workspaces/workspaceUsers', 
        params={
            'workspaceId':exchange_id
        }, 
        data={'xml':to_xml(data, ['workspaceUserCreateRequest'])},
        api_version=1
    )
    
    response.assert_status_code(200)
    response.assert_content_type('text/xml')
    response.assert_no_errors()

    data = response.data()
    
    return get_node_as_item(data, ['workspaceUserPartials', 'workspaceUserPartial'])

def update_exchange_member(api_client, exchange_id, exchange_member, add_groups=None, remove_groups=None):
    keys = ['userId', 'id', 'firstName', 'lastName', 'organization', 'version', 'roleType', 'keyContact', 'qnaCoordinator', 'qnaAttributes']

    data = {k:exchange_member[k] for k in keys if k in exchange_member}

    for k in keys:
        if k not in data:
            data[k] = ''
    
    xml_data = {'workspaceUsers':{'workspaceUser':data}}

    if add_groups is not None and len(add_groups) > 0:
        xml_data['addWorkspaceGroups'] = [{'workspaceGroupId':g['id']} for g in add_groups]

    if remove_groups is not None and len(remove_groups) > 0:
        xml_data['removeWorkspaceGroups'] = [{'workspaceGroupId':g['id']} for g in remove_groups]

    response = api_client.update(
        '/v1/services/workspaces/workspaceUsers', 
        params={
            'workspaceId':exchange_id,
            'workspaceUserId':exchange_member['id']
        }, 
        data={'xml':to_xml(xml_data, 'workspaceUserUpdateRequest')},
        api_version=1
    )
    
    data = response.data()
    
    return data

def delete_exchange_member(api_client, exchange_id, id, version):
    return delete_exchange_members(api_client, exchange_id, [{'id':id, 'version':version}])

def delete_exchange_members(api_client, exchange_id, exchange_members):   
    deleted_exchange_members = [
        {
            'id':m['id'], 
            'version':m['version'], 
            'type':'WORKSPACEUSER'
        } for m in exchange_members
    ]

    response = api_client.delete(
        '/v1/services/workspaces/workspaceUsers', 
        params={
            'workspaceId':exchange_id
        }, 
        data={'xml':to_xml(deleted_exchange_members, ['entityId', 'workspaceUserDeleteRequest'])},
        api_version=1
    )
    
    response.assert_status_code(200)
    response.assert_content_type('text/xml')
    response.assert_no_errors()

    data = response.data()
    
    return data