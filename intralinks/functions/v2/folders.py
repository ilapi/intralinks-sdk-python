"""
For educational purpose only
"""

from intralinks.utils.data import get_node_as_list, get_node_as_item, filter_dict, entity_to_dict
from intralinks.utils.booleans import convert_to_bool
import intralinks.functions.entities
import json

def get_folders(api_client, exchange_id):
    response = api_client.get(
        '/v2/workspaces/{}/folders'.format(exchange_id),
        api_version=2
    )
    
    response.check(200, 'application/json')
    
    data = response.data()
    
    l = get_node_as_list(data, 'folder')

    convert_to_bool(l, 'hasNote')

    return l

def create_folder(api_client, exchange_id, folder):
    l = create_folders(api_client, exchange_id, [folder])
    return l[0] if len(l) > 0 else None
    
def create_folders(api_client, exchange_id, folders):
    folders_data = [{'folder':entity_to_dict(f)} for f in folders]
    
    response = api_client.create(
        '/v2/workspaces/{}/folders'.format(exchange_id),
        data=json.dumps({'folders':folders_data}), 
        headers={'Content-Type':'application/json'},
        api_version=2
    )
    
    response.check(201, 'application/json')
    
    data = response.data()
    
    l = get_node_as_list(data, 'folderPartial')

    convert_to_bool(l, 'hasNote')

    return l
    
def update_folder(api_client, exchange_id, folder):
    folder_data = entity_to_dict(folder)
    folder_data = filter_dict(folder_data, remove_fields={'isEmailin', 'versionNumber', 'isFavorite', 'lastModifiedBy', 'lastModifiedOn', 'createdBy', 'createdOn', 'hasChildFolders', 'orderNumber', 'indexNumber'})
    
    response = api_client.update(
        '/v2/workspaces/{}/folders'.format(exchange_id),
        data=json.dumps({'folders':[folder_data]}), 
        headers={'Content-Type':'application/json'},
        api_version=2
    )
    
    response.check(202, 'application/json')
    
    data = response.data()
    
    result = get_node_as_item(data, 'folderPartial')
    
    if 'hasNote' in result and result['hasNote'] in {'T', 'F'}:
        result['hasNote'] = result['hasNote'] == 'T'

    return result

def delete_folder(api_client, exchange_id, folder, delete_folder_contents=True):
    response = api_client.delete(
        '/v2/workspaces/{}/folders/{}'.format(exchange_id, folder['id']),
        params={
            'version':folder['version'], 
            'deleteFolderContents': 'true' if delete_folder_contents else 'false'
        },
        api_version=2
    )
    
    response.check(202, 'application/json')
    
    data = response.data()
    
    return data

def delete_folders(api_client, exchange_id, folders):
    """
        Not documented
    """
    folder_data = [{'id':f['id'], 'version':f['version']} for f in folders]

    response = api_client.delete(
        '/v2/workspaces/{}/folders'.format(exchange_id),
        data=json.dumps({'folders':folder_data}),
        headers={'Content-Type':'application/json'},
        api_version=2
    )
    
    response.check(202, 'application/json')
    
    data = response.data()
    
    return data